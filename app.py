"""EGC Ingénierie - Site web du bureau d'études techniques MEP (Flask)."""
from __future__ import annotations

import json
import os
import re
import secrets
import smtplib
import sqlite3
import threading
import time
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, g, jsonify, render_template, request, session

import data
import db
from db import DB_PATH, get_db

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, instance_path=str(BASE_DIR / "instance"))
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",  # mettre COOKIE_SECURE=1 en HTTPS
    PERMANENT_SESSION_LIFETIME=8 * 3600,  # session admin : 8 h
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 10 Mo (envoi d'images dans l'admin)
)
CONTACT_MAX_BYTES = 64 * 1024  # l'API publique de devis reste limitée à 64 Ko


VALID_LOTS = {value for value, _ in data.LOTS}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

# --------------------------------------------------------------------------- #
# Base de données (voir db.py)
# --------------------------------------------------------------------------- #

db.init_app(app)

# --------------------------------------------------------------------------- #
# Sécurité légère : jeton CSRF + limitation de débit
# --------------------------------------------------------------------------- #

_rate: dict[str, list[float]] = {}
_rate_lock = threading.Lock()
RATE_LIMIT, RATE_WINDOW = 5, 600  # 5 demandes / 10 min / IP


def rate_limited(ip: str) -> bool:
    now = time.time()
    with _rate_lock:
        hits = [t for t in _rate.get(ip, []) if now - t < RATE_WINDOW]
        if len(hits) >= RATE_LIMIT:
            _rate[ip] = hits
            return True
        hits.append(now)
        _rate[ip] = hits
        return False


def csrf_token() -> str:
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


# --------------------------------------------------------------------------- #
# Partenaires : les logos sont lus automatiquement dans static/img/partners/
# --------------------------------------------------------------------------- #


def load_partners() -> list[dict]:
    """Logos visibles, dans l'ordre défini dans l'admin."""
    rows = get_db().execute("SELECT * FROM partners WHERE visible=1 ORDER BY position, id").fetchall()
    return [{"name": r["name"], "file": f"img/partners/{r['logo']}", "url": r["url"]} for r in rows]


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #


@app.context_processor
def inject_globals():
    return {
        "site": db.site_info(),
        "nav": data.NAV,
        "year": datetime.now().year,
        "csrf_token": csrf_token(),
        "active": request.endpoint,
        "footer_links": data.FOOTER_LINKS,  # <-- AJOUTEZ CETTE LIGNE

    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        nav_mobile=data.NAV_MOBILE,
        hero_modules=data.HERO_MODULES,
        hero_pillars=data.HERO_PILLARS,
        stats=db.get_stats(),
        pillars=data.PILLARS,
        expertises=data.EXPERTISES,
        steps=data.STEPS,
        tools=data.TOOLS,
        sectors=data.SECTORS,
        clients=data.CLIENTS,
        contact_items=db.contact_items(),
        lots=data.LOTS,
        partners=load_partners(),
        partners_section=data.PARTNERS_SECTION,
        partner_points=data.PARTNER_POINTS,
    )


@app.route("/a-propos")
def a_propos():
    return render_template(
        "a_propos.html", intro=data.ABOUT_INTRO, mission=data.MISSION, values=data.VALUES,
        commitments=data.COMMITMENTS, presence=data.PRESENCE, pillars=data.PILLARS,
        tools=data.TOOLS, stats=db.get_stats(),
    )


@app.route("/expertises")
def expertises():
    return render_template("expertises.html", expertises=data.EXPERTISES, tools=data.TOOLS)


@app.route("/expertises/<slug>")
def expertise_detail(slug):
    exp = next((e for e in data.EXPERTISES if e["slug"] == slug), None)
    if exp is None:
        abort(404)
    others = [e for e in data.EXPERTISES if e["slug"] != slug]
    return render_template("expertise_detail.html", e=exp, d=data.EXPERTISE_DETAILS[slug], others=others)


@app.route("/secteurs")
def secteurs():
    return render_template(
        "secteurs.html", sectors=data.SECTORS, details=data.SECTOR_DETAILS,
        clients=data.CLIENTS, client_roles=data.CLIENT_ROLES,
    )



def load_faq() -> list[tuple[str, str]]:
    rows = get_db().execute("SELECT question, answer FROM faq WHERE visible=1 ORDER BY position, id").fetchall()
    return [(r["question"], r["answer"]) for r in rows]


def realisation_sections() -> list[dict]:
    """Domaines d'intervention + leurs projets visibles (gérés depuis l'admin)."""
    rows = get_db().execute("SELECT * FROM projects WHERE visible=1 ORDER BY position, id").fetchall()
    by_domain: dict[str, list[dict]] = {}
    for r in rows:
        by_domain.setdefault(r["domain"], []).append({
            "title": r["title"], "lieu": r["lieu"], "annee": r["annee"], "description": r["description"],
            "image": f"img/realisations/{r['image']}" if r["image"] else "img/realisations/placeholder.svg",
            "placeholder": not r["image"],
        })
    return [{**r, "projects": by_domain.get(r["slug"], [])} for r in data.REALISATIONS]


@app.route("/realisations")
def realisations():
    return render_template("realisations.html", items=realisation_sections(), filters=data.REALISATIONS_FILTERS)


@app.route("/methodologie")
def methodologie():
    return render_template(
        "methodologie.html", steps=data.STEPS, details=data.STEP_DETAILS,
        tools=data.TOOLS, collab=data.COLLAB,
    )


@app.route("/contact")
def contact():
    return render_template(
        "contact.html", contact_items=db.contact_items(), lots=data.LOTS,
        hours=data.HOURS, faq=load_faq(),
    )


@app.route("/devis")
def devis():
    return render_template(
        "devis.html", lots=data.LOTS, quote_steps=data.QUOTE_STEPS,
        reassurance=data.QUOTE_REASSURANCE, contact_items=db.contact_items(),
    )


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


# --------------------------------------------------------------------------- #
# API contact / devis
# --------------------------------------------------------------------------- #


def validate(payload: dict) -> tuple[dict, dict]:
    """Retourne (données nettoyées, erreurs par champ)."""
    clean, errors = {}, {}

    name = str(payload.get("name", "")).strip()
    company = str(payload.get("company", "")).strip()
    email = str(payload.get("email", "")).strip()
    phone = str(payload.get("phone", "")).strip()
    message = str(payload.get("message", "")).strip()
    lots = payload.get("lots", [])
    lots = [l for l in lots if isinstance(l, str)] if isinstance(lots, list) else []

    if len(name) < 2:
        errors["name"] = "Veuillez indiquer votre nom complet."
    elif len(name) > 120:
        errors["name"] = "Nom trop long."

    if len(company) > 160:
        errors["company"] = "Texte trop long."

    if not EMAIL_RE.match(email) or len(email) > 160:
        errors["email"] = "Adresse e-mail invalide."

    if len(re.sub(r"\D", "", phone)) < 8 or len(phone) > 30:
        errors["phone"] = "Numéro de téléphone invalide."

    if not lots:
        errors["lots"] = "Sélectionnez au moins un lot technique."
    elif any(l not in VALID_LOTS for l in lots):
        errors["lots"] = "Sélection invalide."

    if len(message) < 10:
        errors["message"] = "Décrivez brièvement votre projet (10 caractères min.)."
    elif len(message) > 4000:
        errors["message"] = "Message trop long (4000 caractères max.)."

    clean.update(name=name, company=company, email=email, phone=phone,
                 lots=lots, message=message)
    return clean, errors


def send_mail_async(entry: dict) -> None:
    """Notification SMTP facultative (désactivée si MAIL_USERNAME est vide)."""
    server = os.getenv("MAIL_SERVER")
    user = os.getenv("MAIL_USERNAME")
    password = os.getenv("MAIL_PASSWORD")
    to = os.getenv("MAIL_TO", data.SITE["email"])
    if not (server and user and password):
        return

    def _send():
        try:
            msg = EmailMessage()
            msg["Subject"] = f"[EGC Ingénierie] Nouvelle demande de devis - {entry['name']}"
            msg["From"] = user
            msg["To"] = to
            msg["Reply-To"] = entry["email"]
            msg.set_content(
                f"Nom : {entry['name']}\n"
                f"Entreprise : {entry['company'] or '-'}\n"
                f"E-mail : {entry['email']}\n"
                f"Téléphone : {entry['phone']}\n"
                f"Lots : {', '.join(entry['lots'])}\n\n"
                f"{entry['message']}\n"
            )
            with smtplib.SMTP(server, int(os.getenv("MAIL_PORT", 587)), timeout=15) as s:
                s.starttls()
                s.login(user, password)
                s.send_message(msg)
        except Exception as exc:  # noqa: BLE001
            app.logger.warning("Envoi e-mail impossible : %s", exc)

    threading.Thread(target=_send, daemon=True).start()


@app.post("/api/contact")
def api_contact():
    if not request.is_json:
        abort(415)
    if (request.content_length or 0) > CONTACT_MAX_BYTES:
        abort(413)

    if not secrets.compare_digest(request.headers.get("X-CSRF-Token", ""), session.get("csrf", "-")):
        return jsonify(ok=False, message="Session expirée, rechargez la page."), 400

    payload = request.get_json(silent=True) or {}

    # Honeypot : un bot remplit ce champ caché ; on répond "ok" sans rien enregistrer.
    if str(payload.get("website", "")).strip():
        return jsonify(ok=True, message="Votre demande a bien été envoyée.")

    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "?").split(",")[0].strip()
    if rate_limited(ip):
        return jsonify(ok=False, message="Trop de demandes. Réessayez dans quelques minutes."), 429

    clean, errors = validate(payload)
    if errors:
        return jsonify(ok=False, errors=errors, message="Veuillez corriger les champs signalés."), 422

    db = get_db()
    db.execute(
        "INSERT INTO quote_requests (created_at, name, company, email, phone, lots, message, ip)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (datetime.now().isoformat(timespec="seconds"), clean["name"], clean["company"],
         clean["email"], clean["phone"], ",".join(clean["lots"]), clean["message"], ip),
    )
    db.commit()
    send_mail_async(clean)

    return jsonify(
        ok=True,
        message="Votre demande a bien été envoyée avec succès ! "
                "Notre bureau d'études vous recontactera sous 24h.",
    )


# --------------------------------------------------------------------------- #
# CLI : flask --app app requests
# --------------------------------------------------------------------------- #


@app.cli.command("requests")
def list_requests():
    """Affiche les demandes de devis enregistrées."""
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("SELECT * FROM quote_requests ORDER BY id DESC").fetchall()
    if not rows:
        print("Aucune demande.")
    for r in rows:
        print(f"#{r['id']} {r['created_at']} | {r['name']} ({r['company'] or '-'}) | "
              f"{r['email']} | {r['phone']} | {r['lots']}\n    {r['message']}\n")


from admin import bp as admin_bp, create_admin, ensure_env_admin  # noqa: E402  (après la création de l'app)

app.register_blueprint(admin_bp)
app.cli.add_command(create_admin)
ensure_env_admin(app.logger)


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
