"""Espace d'administration (/admin) : gestion du contenu du site EGC Ingénierie."""
from __future__ import annotations

import csv
import io
import os
import re
import secrets
import sqlite3
import threading
import time
from datetime import datetime
from functools import wraps
from pathlib import Path

import click
from flask import Blueprint, Response, abort, flash, redirect, render_template, request, session, url_for
from PIL import Image, ImageOps
from werkzeug.security import check_password_hash, generate_password_hash

import data
import db
from db import PARTNERS_DIR, REALISATIONS_DIR, get_db
# --- PATCH : compatibilité scrypt sur macOS / Python 3.9 ---
import hashlib as _hashlib

if not hasattr(_hashlib, "scrypt"):
    import werkzeug.security as _ws

    def _hash_internal_fallback(method, salt, password):
        return (
            "pbkdf2:sha256",
            _hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                260000,
            ),
        )

    _ws._hash_internal = _hash_internal_fallback
# --- FIN PATCH ---

bp = Blueprint("admin", __name__, url_prefix="/admin")

Image.MAX_IMAGE_PIXELS = 40_000_000  # protection contre les images "bombes"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
MIN_PASSWORD = 10

STATUSES = {
    "nouveau": ("Nouveau", "bg-cyan-100 text-cyan-800"),
    "en_cours": ("En cours", "bg-amber-100 text-amber-800"),
    "traite": ("Traité", "bg-green-100 text-green-800"),
    "archive": ("Archivé", "bg-slate-200 text-slate-700"),
}
DOMAINS = [(r["slug"], r["title"]) for r in data.REALISATIONS]
DOMAIN_SLUGS = {s for s, _ in DOMAINS}
LOT_LABELS = dict(data.LOTS)
PAGE_SIZE = 20
_DUMMY_HASH = generate_password_hash("not-a-real-password")

# --------------------------------------------------------------------------- #
# Sécurité : session, CSRF, limitation des tentatives, en-têtes
# --------------------------------------------------------------------------- #

_attempts: dict[str, list[float]] = {}
_lock = threading.Lock()
LOGIN_MAX, LOGIN_WINDOW = 6, 900  # 6 échecs / 15 min / IP


def client_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr or "?").split(",")[0].strip()


def _recent_failures(ip: str) -> list[float]:
    now = time.time()
    return [t for t in _attempts.get(ip, []) if now - t < LOGIN_WINDOW]


def safe_next(target: str | None) -> str:
    if target and target.startswith("/admin") and "//" not in target and "\\" not in target:
        return target
    return url_for("admin.dashboard")


@bp.before_request
def guard():
    if request.endpoint != "admin.login" and not session.get("admin_id"):
        return redirect(url_for("admin.login", next=request.full_path.rstrip("?") if request.method == "GET" else None))
    if request.method == "POST" and not secrets.compare_digest(request.form.get("_csrf", ""), session.get("csrf", "-")):
        abort(400)


@bp.context_processor
def admin_context():
    new = 0
    if session.get("admin_id"):
        new = get_db().execute("SELECT COUNT(*) FROM quote_requests WHERE status='nouveau'").fetchone()[0]
    return {"new_count": new}


@bp.after_request
def secure_headers(resp):
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Robots-Tag"] = "noindex, nofollow"
    resp.headers["Referrer-Policy"] = "same-origin"
    return resp


def valid_int(value, default=1) -> int:
    try:
        return max(int(value), 1)
    except (TypeError, ValueError):
        return default


# --------------------------------------------------------------------------- #
# Images
# --------------------------------------------------------------------------- #


def save_image(file, dest: Path, *, logo: bool = False) -> str:
    """Valide, redimensionne et enregistre une image envoyée ; renvoie le nom du fichier."""
    raw = file.read()
    if not raw:
        raise ValueError("Le fichier est vide.")
    try:
        im = Image.open(io.BytesIO(raw))
        fmt = im.format
        im.load()
    except Exception:  # noqa: BLE001 - tout échec de lecture = image invalide
        raise ValueError("Image illisible. Formats acceptés : JPG, PNG, WebP.") from None
    if fmt not in {"JPEG", "PNG", "WEBP"}:
        raise ValueError("Format non accepté. Utilisez JPG, PNG ou WebP.")

    im = ImageOps.exif_transpose(im)
    dest.mkdir(parents=True, exist_ok=True)
    name = f"u-{secrets.token_hex(8)}"
    if logo:
        im = im.convert("RGBA")
        im.thumbnail((480, 240))
        name += ".png"
        im.save(dest / name, "PNG", optimize=True)
    else:
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[3])
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((1600, 1600))
        name += ".jpg"
        im.save(dest / name, "JPEG", quality=85, optimize=True, progressive=True)
    return name


def remove_upload(folder: Path, name: str) -> None:
    """Supprime un fichier envoyé via l'admin (jamais ceux livrés avec le site)."""
    if name and name.startswith("u-") and "/" not in name and "\\" not in name:
        (folder / name).unlink(missing_ok=True)


# --------------------------------------------------------------------------- #
# Ordre des éléments
# --------------------------------------------------------------------------- #


def move_item(table: str, item_id: int, direction: str, group_col: str | None = None) -> None:
    """Échange un élément avec son voisin ; renumérote proprement la liste (noms de tables fixes)."""
    conn = get_db()
    group_sql = f", {group_col} AS g" if group_col else ""
    items = conn.execute(f"SELECT id{group_sql} FROM {table} ORDER BY position, id").fetchall()
    me = next((r for r in items if r["id"] == item_id), None)
    if me is None:
        return
    peers = [r["id"] for r in items if not group_col or r["g"] == me["g"]]
    i = peers.index(item_id)
    j = i - 1 if direction == "up" else i + 1
    if 0 <= j < len(peers):
        peers[i], peers[j] = peers[j], peers[i]
        for pos, pid in enumerate(peers, start=1):
            conn.execute(f"UPDATE {table} SET position=? WHERE id=?", (pos, pid))
        conn.commit()


def next_position(table: str, where: str = "1=1", params: tuple = ()) -> int:
    row = get_db().execute(f"SELECT COALESCE(MAX(position),0)+1 AS n FROM {table} WHERE {where}", params).fetchone()
    return row["n"]


# --------------------------------------------------------------------------- #
# Connexion / déconnexion / compte
# --------------------------------------------------------------------------- #


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))
    has_admin = get_db().execute("SELECT COUNT(*) FROM admins").fetchone()[0] > 0

    if request.method == "POST":
        ip = client_ip()
        with _lock:
            blocked = len(_recent_failures(ip)) >= LOGIN_MAX
        if blocked:
            flash("Trop de tentatives. Réessayez dans quelques minutes.", "err")
            return render_template("admin/login.html", has_admin=has_admin), 429

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        row = get_db().execute("SELECT * FROM admins WHERE username=?", (username,)).fetchone()
        ok = check_password_hash(row["password_hash"] if row else _DUMMY_HASH, password)
        if row and ok:
            with _lock:
                _attempts.pop(ip, None)
            next_url = safe_next(request.args.get("next"))
            session.clear()  # nouvelle session après connexion
            session["csrf"] = secrets.token_urlsafe(32)
            session["admin_id"], session["admin_name"] = row["id"], row["username"]
            session.permanent = True
            return redirect(next_url)
        with _lock:
            _attempts[ip] = _recent_failures(ip) + [time.time()]
        flash("Identifiant ou mot de passe incorrect.", "err")
    return render_template("admin/login.html", has_admin=has_admin)


@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@bp.route("/compte", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        row = get_db().execute("SELECT * FROM admins WHERE id=?", (session["admin_id"],)).fetchone()
        current, new, confirm = (request.form.get(k, "") for k in ("current", "new", "confirm"))
        if not check_password_hash(row["password_hash"], current):
            flash("Le mot de passe actuel est incorrect.", "err")
        elif len(new) < MIN_PASSWORD:
            flash(f"Le nouveau mot de passe doit contenir au moins {MIN_PASSWORD} caractères.", "err")
        elif new != confirm:
            flash("La confirmation ne correspond pas au nouveau mot de passe.", "err")
        else:
            get_db().execute("UPDATE admins SET password_hash=? WHERE id=?", (generate_password_hash(new), row["id"]))
            get_db().commit()
            flash("Mot de passe modifié.", "ok")
            return redirect(url_for("admin.account"))
    return render_template("admin/account.html")


# --------------------------------------------------------------------------- #
# Tableau de bord
# --------------------------------------------------------------------------- #


@bp.get("/")
def dashboard():
    conn = get_db()
    count = lambda sql: conn.execute(sql).fetchone()[0]  # noqa: E731
    stats = {
        "nouveau": count("SELECT COUNT(*) FROM quote_requests WHERE status='nouveau'"),
        "devis": count("SELECT COUNT(*) FROM quote_requests"),
        "projets": count("SELECT COUNT(*) FROM projects WHERE visible=1"),
        "partenaires": count("SELECT COUNT(*) FROM partners WHERE visible=1"),
        "faq": count("SELECT COUNT(*) FROM faq WHERE visible=1"),
    }
    latest = conn.execute("SELECT * FROM quote_requests ORDER BY id DESC LIMIT 5").fetchall()
    return render_template("admin/dashboard.html", stats=stats, latest=latest, statuses=STATUSES, lot_labels=LOT_LABELS)


# --------------------------------------------------------------------------- #
# Demandes de devis
# --------------------------------------------------------------------------- #


def _quote_filter() -> tuple[str, list]:
    q, st = request.args.get("q", "").strip(), request.args.get("statut", "")
    where, params = ["1=1"], []
    if st in STATUSES:
        where.append("status=?")
        params.append(st)
    if q:
        where.append("(name LIKE ? OR company LIKE ? OR email LIKE ? OR phone LIKE ? OR message LIKE ?)")
        params += [f"%{q}%"] * 5
    return " AND ".join(where), params


@bp.get("/devis")
def quotes():
    where, params = _quote_filter()
    conn = get_db()
    total = conn.execute(f"SELECT COUNT(*) FROM quote_requests WHERE {where}", params).fetchone()[0]
    pages = max((total + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    page = min(valid_int(request.args.get("page")), pages)
    rows = conn.execute(
        f"SELECT * FROM quote_requests WHERE {where} ORDER BY id DESC LIMIT ? OFFSET ?",
        params + [PAGE_SIZE, (page - 1) * PAGE_SIZE],
    ).fetchall()
    return render_template(
        "admin/quotes.html", rows=rows, total=total, page=page, pages=pages, statuses=STATUSES,
        lot_labels=LOT_LABELS, q=request.args.get("q", ""), statut=request.args.get("statut", ""),
        args={k: v for k, v in request.args.items() if k in ("q", "statut")},
    )


@bp.get("/devis/export.csv")
def quotes_export():
    where, params = _quote_filter()
    rows = get_db().execute(f"SELECT * FROM quote_requests WHERE {where} ORDER BY id DESC", params).fetchall()

    def safe(v) -> str:  # neutralise l'injection de formules dans Excel
        v = "" if v is None else str(v)
        return "'" + v if v[:1] in ("=", "+", "-", "@") else v

    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";")
    w.writerow(["ID", "Date", "Statut", "Nom", "Société", "E-mail", "Téléphone", "Lots", "Message", "Note interne"])
    for r in rows:
        lots = ", ".join(LOT_LABELS.get(x, x) for x in r["lots"].split(",") if x)
        w.writerow([r["id"], r["created_at"], STATUSES.get(r["status"], (r["status"],))[0], *map(safe, (
            r["name"], r["company"], r["email"], r["phone"], lots, r["message"], r["note"]))])
    name = f"demandes-devis-{datetime.now():%Y%m%d}.csv"
    return Response("\ufeff" + buf.getvalue(), mimetype="text/csv; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{name}"'})


@bp.get("/devis/<int:qid>")
def quote_detail(qid: int):
    row = get_db().execute("SELECT * FROM quote_requests WHERE id=?", (qid,)).fetchone()
    if row is None:
        abort(404)
    lots = [LOT_LABELS.get(x, x) for x in row["lots"].split(",") if x]
    return render_template("admin/quote_detail.html", r=row, lots=lots, statuses=STATUSES)


@bp.post("/devis/<int:qid>/maj")
def quote_update(qid: int):
    status = request.form.get("status", "")
    if status not in STATUSES:
        abort(400)
    get_db().execute("UPDATE quote_requests SET status=?, note=? WHERE id=?",
                     (status, request.form.get("note", "").strip()[:2000], qid))
    get_db().commit()
    flash("Demande mise à jour.", "ok")
    return redirect(url_for("admin.quote_detail", qid=qid))


@bp.post("/devis/<int:qid>/supprimer")
def quote_delete(qid: int):
    get_db().execute("DELETE FROM quote_requests WHERE id=?", (qid,))
    get_db().commit()
    flash("Demande supprimée.", "ok")
    return redirect(url_for("admin.quotes"))


# --------------------------------------------------------------------------- #
# Réalisations (projets par domaine)
# --------------------------------------------------------------------------- #


@bp.get("/realisations")
def projects():
    rows = get_db().execute("SELECT * FROM projects ORDER BY position, id").fetchall()
    grouped = {slug: [r for r in rows if r["domain"] == slug] for slug, _ in DOMAINS}
    return render_template("admin/projects.html", grouped=grouped, domains=DOMAINS)


def _project_form(pid: int | None):
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone() if pid else None
    if pid and row is None:
        abort(404)
    values = dict(row) if row else {"domain": request.args.get("domaine", DOMAINS[0][0]), "title": "", "lieu": "",
                                    "annee": "", "description": "", "image": "", "visible": 1}

    if request.method == "POST":
        f = request.form
        values.update(domain=f.get("domain", ""), title=f.get("title", "").strip()[:120], lieu=f.get("lieu", "").strip()[:80],
                      annee=f.get("annee", "").strip()[:20], description=f.get("description", "").strip()[:400],
                      visible=1 if f.get("visible") else 0)
        error = None
        if values["domain"] not in DOMAIN_SLUGS:
            error = "Domaine invalide."
        elif len(values["title"]) < 3:
            error = "Le nom du projet est obligatoire (3 caractères minimum)."

        image = values["image"]
        upload = request.files.get("image")
        new_file = None
        if not error and upload and upload.filename:
            try:
                new_file = save_image(upload, REALISATIONS_DIR)
            except ValueError as exc:
                error = str(exc)

        if error:
            flash(error, "err")
            return render_template("admin/project_form.html", p=values, pid=pid, domains=DOMAINS), 422

        if new_file:
            remove_upload(REALISATIONS_DIR, image)
            image = new_file
        elif f.get("remove_image"):
            remove_upload(REALISATIONS_DIR, image)
            image = ""

        if pid:
            pos = row["position"] if row["domain"] == values["domain"] else next_position("projects")
            conn.execute("UPDATE projects SET domain=?,title=?,lieu=?,annee=?,description=?,image=?,visible=?,position=? WHERE id=?",
                         (values["domain"], values["title"], values["lieu"], values["annee"], values["description"],
                          image, values["visible"], pos, pid))
        else:
            conn.execute("INSERT INTO projects(domain,title,lieu,annee,description,image,visible,position) VALUES (?,?,?,?,?,?,?,?)",
                         (values["domain"], values["title"], values["lieu"], values["annee"], values["description"],
                          image, values["visible"], next_position("projects")))
        conn.commit()
        flash("Projet enregistré.", "ok")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html", p=values, pid=pid, domains=DOMAINS)


@bp.route("/realisations/nouveau", methods=["GET", "POST"])
def project_new():
    return _project_form(None)


@bp.route("/realisations/<int:pid>/modifier", methods=["GET", "POST"])
def project_edit(pid: int):
    return _project_form(pid)


@bp.post("/realisations/<int:pid>/supprimer")
def project_delete(pid: int):
    row = get_db().execute("SELECT image FROM projects WHERE id=?", (pid,)).fetchone()
    if row:
        remove_upload(REALISATIONS_DIR, row["image"])
        get_db().execute("DELETE FROM projects WHERE id=?", (pid,))
        get_db().commit()
        flash("Projet supprimé.", "ok")
    return redirect(url_for("admin.projects"))


@bp.post("/realisations/<int:pid>/visibilite")
def project_toggle(pid: int):
    get_db().execute("UPDATE projects SET visible = 1 - visible WHERE id=?", (pid,))
    get_db().commit()
    return redirect(url_for("admin.projects"))


@bp.post("/realisations/<int:pid>/deplacer")
def project_move(pid: int):
    move_item("projects", pid, request.form.get("dir", ""), "domain")
    return redirect(url_for("admin.projects"))


# --------------------------------------------------------------------------- #
# Partenaires
# --------------------------------------------------------------------------- #


def _clean_url(raw: str) -> str | None:
    raw = raw.strip()
    if not raw:
        return ""
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    return raw[:300] if re.match(r"^https?://[^\s/]+\.[^\s/]+", raw) else None


@bp.get("/partenaires")
def partners():
    rows = get_db().execute("SELECT * FROM partners ORDER BY position, id").fetchall()
    return render_template("admin/partners.html", rows=rows)


@bp.post("/partenaires/ajouter")
def partner_add():
    name, url, upload = request.form.get("name", "").strip()[:80], _clean_url(request.form.get("url", "")), request.files.get("logo")
    if len(name) < 2:
        flash("Le nom du partenaire est obligatoire.", "err")
    elif url is None:
        flash("Adresse du site invalide.", "err")
    elif not upload or not upload.filename:
        flash("Ajoutez le logo du partenaire (JPG, PNG ou WebP).", "err")
    else:
        try:
            logo = save_image(upload, PARTNERS_DIR, logo=True)
        except ValueError as exc:
            flash(str(exc), "err")
        else:
            get_db().execute("INSERT INTO partners(name,url,logo,position) VALUES (?,?,?,?)",
                             (name, url, logo, next_position("partners")))
            get_db().commit()
            flash("Partenaire ajouté.", "ok")
    return redirect(url_for("admin.partners"))


@bp.post("/partenaires/<int:pid>/enregistrer")
def partner_save(pid: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM partners WHERE id=?", (pid,)).fetchone()
    if row is None:
        abort(404)
    name, url, upload = request.form.get("name", "").strip()[:80], _clean_url(request.form.get("url", "")), request.files.get("logo")
    if len(name) < 2 or url is None:
        flash("Nom ou adresse du site invalide.", "err")
        return redirect(url_for("admin.partners"))
    logo = row["logo"]
    if upload and upload.filename:
        try:
            new = save_image(upload, PARTNERS_DIR, logo=True)
        except ValueError as exc:
            flash(str(exc), "err")
            return redirect(url_for("admin.partners"))
        remove_upload(PARTNERS_DIR, logo)
        logo = new
    conn.execute("UPDATE partners SET name=?, url=?, logo=?, visible=? WHERE id=?",
                 (name, url, logo, 1 if request.form.get("visible") else 0, pid))
    conn.commit()
    flash("Partenaire enregistré.", "ok")
    return redirect(url_for("admin.partners"))


@bp.post("/partenaires/<int:pid>/supprimer")
def partner_delete(pid: int):
    row = get_db().execute("SELECT logo FROM partners WHERE id=?", (pid,)).fetchone()
    if row:
        remove_upload(PARTNERS_DIR, row["logo"])
        get_db().execute("DELETE FROM partners WHERE id=?", (pid,))
        get_db().commit()
        flash("Partenaire supprimé.", "ok")
    return redirect(url_for("admin.partners"))


@bp.post("/partenaires/<int:pid>/deplacer")
def partner_move(pid: int):
    move_item("partners", pid, request.form.get("dir", ""))
    return redirect(url_for("admin.partners"))


# --------------------------------------------------------------------------- #
# FAQ
# --------------------------------------------------------------------------- #


@bp.get("/faq")
def faq():
    rows = get_db().execute("SELECT * FROM faq ORDER BY position, id").fetchall()
    return render_template("admin/faq.html", rows=rows)


@bp.post("/faq/ajouter")
def faq_add():
    q, a = request.form.get("question", "").strip()[:200], request.form.get("answer", "").strip()[:1200]
    if len(q) < 5 or len(a) < 5:
        flash("La question et la réponse sont obligatoires.", "err")
    else:
        get_db().execute("INSERT INTO faq(question,answer,position) VALUES (?,?,?)", (q, a, next_position("faq")))
        get_db().commit()
        flash("Question ajoutée.", "ok")
    return redirect(url_for("admin.faq"))


@bp.post("/faq/<int:fid>/enregistrer")
def faq_save(fid: int):
    q, a = request.form.get("question", "").strip()[:200], request.form.get("answer", "").strip()[:1200]
    if len(q) < 5 or len(a) < 5:
        flash("La question et la réponse sont obligatoires.", "err")
    else:
        get_db().execute("UPDATE faq SET question=?, answer=?, visible=? WHERE id=?",
                         (q, a, 1 if request.form.get("visible") else 0, fid))
        get_db().commit()
        flash("Question enregistrée.", "ok")
    return redirect(url_for("admin.faq"))


@bp.post("/faq/<int:fid>/supprimer")
def faq_delete(fid: int):
    get_db().execute("DELETE FROM faq WHERE id=?", (fid,))
    get_db().commit()
    flash("Question supprimée.", "ok")
    return redirect(url_for("admin.faq"))


@bp.post("/faq/<int:fid>/deplacer")
def faq_move(fid: int):
    move_item("faq", fid, request.form.get("dir", ""))
    return redirect(url_for("admin.faq"))


# --------------------------------------------------------------------------- #
# Paramètres : coordonnées + chiffres clés
# --------------------------------------------------------------------------- #


@bp.route("/parametres", methods=["GET", "POST"])
def settings():
    site = db.site_info()
    stats = db.get_stats()
    if request.method == "POST":
        f = request.form
        new_site = {k: f.get(k, "").strip()[:200] for k in db.SITE_FIELDS}
        new_stats, error = [], None
        for i, s in enumerate(stats):
            try:
                value = int(f.get(f"stat_value_{i}", ""))
                if not 0 <= value <= 100000:
                    raise ValueError
            except ValueError:
                error = "Les chiffres clés doivent être des nombres entiers positifs."
                break
            new_stats.append({"value": value, "suffix": f.get(f"stat_suffix_{i}", "").strip()[:4],
                              "label": f.get(f"stat_label_{i}", "").strip()[:40] or s["label"],
                              "sub": f.get(f"stat_sub_{i}", "").strip()[:60] or s["sub"]})
        if not new_site["phone"] or not re.search(r"\d{6,}", re.sub(r"\D", "", new_site["phone"])):
            error = "Indiquez un numéro de téléphone valide."
        elif not EMAIL_RE.match(new_site["email"]):
            error = "Adresse e-mail invalide."
        elif not new_site["address"] or not new_site["website"]:
            error = "L'adresse et le site web sont obligatoires."
        if error:
            flash(error, "err")
            site, stats = {**site, **new_site}, [{**s, **n} for s, n in zip(stats, new_stats)] or stats
        else:
            new_site["address_short"] = new_site["address_short"] or new_site["address"]
            db.save_setting("site", new_site)
            db.save_setting("stats", new_stats)
            flash("Paramètres enregistrés.", "ok")
            return redirect(url_for("admin.settings"))
    return render_template("admin/settings.html", site=site, stats=stats)


# --------------------------------------------------------------------------- #
# Création du compte administrateur
# --------------------------------------------------------------------------- #


def _upsert_admin(username: str, password: str) -> None:
    with sqlite3.connect(db.DB_PATH) as conn:
        conn.execute(
            "INSERT INTO admins(username,password_hash,created_at) VALUES (?,?,?) "
            "ON CONFLICT(username) DO UPDATE SET password_hash=excluded.password_hash",
            (username, generate_password_hash(password), datetime.now().isoformat(timespec="seconds")),
        )


def ensure_env_admin(logger=None) -> None:
    """Crée le premier administrateur depuis ADMIN_USERNAME / ADMIN_PASSWORD (.env) si aucun n'existe."""
    user, pwd = os.getenv("ADMIN_USERNAME", "").strip(), os.getenv("ADMIN_PASSWORD", "")
    if not user or not pwd:
        return
    with sqlite3.connect(db.DB_PATH) as conn:
        if conn.execute("SELECT COUNT(*) FROM admins").fetchone()[0]:
            return
    _upsert_admin(user, pwd)
    if logger:
        logger.warning("Administrateur '%s' créé depuis .env : retirez ADMIN_PASSWORD du .env après la première connexion.", user)


@click.command("create-admin")
@click.option("--username", prompt="Identifiant", help="Identifiant de connexion.")
@click.password_option("--password", prompt="Mot de passe", confirmation_prompt=True, help="Mot de passe (10 caractères minimum).")
def create_admin(username: str, password: str) -> None:
    """Crée un administrateur ou réinitialise son mot de passe."""
    username = username.strip()
    if len(username) < 3:
        raise click.ClickException("L'identifiant doit contenir au moins 3 caractères.")
    if len(password) < MIN_PASSWORD:
        raise click.ClickException(f"Le mot de passe doit contenir au moins {MIN_PASSWORD} caractères.")
    _upsert_admin(username, password)
    click.echo(f"Administrateur « {username} » enregistré. Connexion : /admin")
