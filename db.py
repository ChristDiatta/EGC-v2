"""Base SQLite : schéma, migrations légères, données initiales et réglages éditables."""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

from flask import g

import data

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "egc.db"
PARTNERS_DIR = BASE_DIR / "static" / "img" / "partners"
REALISATIONS_DIR = BASE_DIR / "static" / "img" / "realisations"
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".avif")

# Coordonnées modifiables depuis l'admin (les autres clés de data.SITE restent dans data.py)
SITE_FIELDS = ("phone", "email", "address", "address_short", "website")

SCHEMA = """
CREATE TABLE IF NOT EXISTS quote_requests (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    name       TEXT NOT NULL,
    company    TEXT,
    email      TEXT NOT NULL,
    phone      TEXT NOT NULL,
    lots       TEXT NOT NULL,
    message    TEXT NOT NULL,
    ip         TEXT
);
CREATE TABLE IF NOT EXISTS admins (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    domain      TEXT NOT NULL,
    title       TEXT NOT NULL,
    lieu        TEXT NOT NULL DEFAULT '',
    annee       TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    image       TEXT NOT NULL DEFAULT '',
    position    INTEGER NOT NULL DEFAULT 0,
    visible     INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS partners (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL,
    url      TEXT NOT NULL DEFAULT '',
    logo     TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    visible  INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS faq (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer   TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    visible  INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_app(app) -> None:
    app.teardown_appcontext(close_db)
    init_db()


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.executescript(SCHEMA)
        # Migration : suivi des demandes de devis
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(quote_requests)")}
        if "status" not in cols:
            conn.execute("ALTER TABLE quote_requests ADD COLUMN status TEXT NOT NULL DEFAULT 'nouveau'")
        if "note" not in cols:
            conn.execute("ALTER TABLE quote_requests ADD COLUMN note TEXT NOT NULL DEFAULT ''")
        _seed(conn)


def _seeded(conn, name: str) -> bool:
    return conn.execute("SELECT 1 FROM settings WHERE key=?", (f"seeded:{name}",)).fetchone() is not None


def _mark(conn, name: str) -> None:
    conn.execute("INSERT OR REPLACE INTO settings(key, value) VALUES (?, '1')", (f"seeded:{name}",))


def _seed(conn) -> None:
    """Importe une seule fois le contenu existant (data.py + dossiers d'images) dans la base.

    Un marqueur évite de recréer le contenu si l'administrateur le supprime volontairement.
    """
    if not _seeded(conn, "projects"):
        files = {p.name.lower(): p.name for p in REALISATIONS_DIR.iterdir()} if REALISATIONS_DIR.is_dir() else {}
        for r in data.REALISATIONS:
            for n, pr in enumerate(data.REALISATION_PROJECTS.get(r["slug"], []), start=1):
                img = next((files[f"{r['slug']}-{n}{e}"] for e in IMG_EXT if f"{r['slug']}-{n}{e}" in files), "")
                conn.execute(
                    "INSERT INTO projects(domain,title,lieu,annee,image,position) VALUES (?,?,?,?,?,?)",
                    (r["slug"], pr["title"], pr.get("lieu", ""), pr.get("annee", ""), img, n),
                )
        _mark(conn, "projects")

    if not _seeded(conn, "partners"):
        meta = {}
        meta_file = PARTNERS_DIR / "partners.json"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
            except ValueError:
                meta = {}
        exts = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".avif"}
        files = sorted(p for p in PARTNERS_DIR.iterdir() if p.suffix.lower() in exts) if PARTNERS_DIR.is_dir() else []
        real = [p for p in files if not p.stem.lower().startswith("exemple")]
        for i, p in enumerate(real or files, start=1):
            info = meta.get(p.name, {}) if isinstance(meta, dict) else {}
            auto = re.sub(r"[-_]+", " ", re.sub(r"^\d+[-_ ]*", "", p.stem)).strip().title()
            url = str(info.get("url", "")).strip()
            conn.execute(
                "INSERT INTO partners(name,url,logo,position) VALUES (?,?,?,?)",
                (info.get("name") or auto or p.stem, url if url.startswith(("http://", "https://")) else "", p.name, i),
            )
        _mark(conn, "partners")

    if not _seeded(conn, "faq"):
        for i, (q, a) in enumerate(data.FAQ, start=1):
            conn.execute("INSERT INTO faq(question,answer,position) VALUES (?,?,?)", (q, a, i))
        _mark(conn, "faq")


# --------------------------------------------------------------------------- #
# Réglages éditables (coordonnées, chiffres clés)
# --------------------------------------------------------------------------- #


def _setting(key: str):
    row = get_db().execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    if not row:
        return None
    try:
        return json.loads(row["value"])
    except ValueError:
        return None


def save_setting(key: str, value) -> None:
    db = get_db()
    db.execute("INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)", (key, json.dumps(value, ensure_ascii=False)))
    db.commit()


def site_info() -> dict:
    """data.SITE + coordonnées modifiées dans l'admin (mis en cache pour la requête)."""
    if "site_info" in g:
        return g.site_info
    site = dict(data.SITE)
    over = _setting("site") or {}
    for k in SITE_FIELDS:
        if isinstance(over.get(k), str) and over[k].strip():
            site[k] = over[k].strip()
    site["phone_href"] = "tel:" + re.sub(r"[^\d+]", "", site["phone"])
    web = site["website"]
    site["website_href"] = web if web.startswith(("http://", "https://")) else "https://" + web
    g.site_info = site
    return site


def contact_items() -> list[dict]:
    """data.CONTACT_ITEMS reconstruit avec les coordonnées actuelles."""
    s = site_info()
    vals = [(s["phone"], s["phone_href"]), (s["email"], "mailto:" + s["email"]),
            (s["address"], None), (s["website"], s["website_href"])]
    return [{**it, "value": v, "href": h} for it, (v, h) in zip(data.CONTACT_ITEMS, vals)]


def get_stats() -> list[dict]:
    """data.STATS + valeurs modifiées dans l'admin (les couleurs restent celles de data.py)."""
    over = _setting("stats")
    out = [dict(s) for s in data.STATS]
    if isinstance(over, list):
        for s, o in zip(out, over):
            if not isinstance(o, dict):
                continue
            for k in ("value", "label", "sub"):
                if o.get(k) not in (None, ""):
                    s[k] = o[k]
            if isinstance(o.get("suffix"), str):
                s["suffix"] = o["suffix"]
    return out
