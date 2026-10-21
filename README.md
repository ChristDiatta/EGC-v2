# EGC Ingénierie

EGC Ingénierie » (thème sombre, glassmorphism, dégradés cyan/vert/or)
en projet Flask, avec une couche d'animations modernes.

## Démarrage

```bash
python -m venv venv && source venv/bin/activate   # Windows : venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                               # puis adapter SECRET_KEY
flask --app app run --debug
```
Ouvrir http://127.0.0.1:5000

## Structure

```
EGC-Ingenierie/
├── app.py                 # routes, API /api/contact, SQLite, e-mail optionnel
├── data.py                # TOUT le contenu (textes, listes, coordonnées)
├── wsgi.py                # point d'entrée production
├── templates/
│   ├── base.html          # <head>, config Tailwind, loader, navbar, footer
│   ├── index.html
│   ├── _macros.html       # en-tête de section réutilisable
│   ├── 404.html
│   └── partials/          # _hero, _about, _expertises, _methodologie, _secteurs, _contact...
└── static/
    ├── css/style.css      # design d'origine + animations
    ├── js/main.js         # interactions
    └── img/               # logo-egc*.png/webp, favicon.ico, apple-touch-icon.png, og-image.jpg, partners/, realisations/
```

## Pages

| URL | Contenu |
|---|---|
| `/` | Accueil (inchangé : hero, à propos, expertises, méthode, secteurs, contact) |
| `/a-propos` | Mission, valeurs, engagements, présence Sénégal / Maroc |
| `/expertises` et `/expertises/<slug>` | Les 5 métiers + une page détaillée chacun (prestations, livrables, référentiels, FAQ) |
| `/secteurs` | Résidentiel, tertiaire, industriel + rôle auprès de chaque type de client |
| `/realisations` | Missions types filtrables par secteur (à remplacer par vos vraies références) |
| `/methodologie` | Les 6 phases détaillées (actions + livrables) |
| `/contact` | Coordonnées, formulaire, horaires, FAQ |
| `/devis` | Page « Demander un devis » (accepte `?lot=CVC` pour présélectionner un lot) |

Le bouton **Demander un devis** est dans la barre de navigation (et le menu mobile), sur chaque page d'expertise
(lot présélectionné) et dans un bandeau en bas de chaque page.

## Administration (`/admin`)

Espace réservé pour gérer le contenu du site sans toucher au code.

**Première connexion**

```bash
pip install -r requirements.txt
flask --app app create-admin      # demande l'identifiant et le mot de passe (10 caractères minimum)
flask --app app run --debug       # puis ouvrir http://127.0.0.1:5000/admin
```

La même commande réinitialise un mot de passe oublié. Alternative : renseigner `ADMIN_USERNAME` et
`ADMIN_PASSWORD` dans `.env` (le compte est créé au démarrage s'il n'y en a aucun ; supprimez ensuite le mot de passe du `.env`).

| Menu | Ce que vous pouvez faire |
|---|---|
| Tableau de bord | Vue d'ensemble, dernières demandes |
| Demandes de devis | Recherche, statut (nouveau / en cours / traité / archivé), note interne, réponse par e-mail, export CSV, suppression |
| Réalisations | Ajouter, modifier, masquer, réordonner et supprimer les projets de chaque domaine, avec photo |
| Partenaires | Ajouter ou remplacer des logos, lien du site, ordre, visibilité |
| FAQ | Questions affichées sur la page Contact |
| Paramètres du site | Téléphone, e-mail, adresse, site web et les 4 chiffres clés |
| Mon compte | Changement du mot de passe |

Les images envoyées sont contrôlées (JPG, PNG, WebP), redimensionnées automatiquement et enregistrées dans
`static/img/realisations/` et `static/img/partners/` (préfixe `u-`). Les textes plus longs (expertises, secteurs, méthode…)
restent dans `data.py`.

**Sécurité** : mots de passe hachés, session de 8 h, jeton CSRF sur chaque formulaire, blocage après 6 échecs de connexion
(15 min), en-têtes `no-store` / `noindex`, aucun envoi de fichier exécutable. En production (HTTPS), mettez
`COOKIE_SECURE=1` et une vraie valeur pour `SECRET_KEY` dans `.env`.

**Migration** : au premier lancement, le contenu existant (projets, photos, logos, FAQ) est importé dans la base `instance/egc.db`.
Ensuite, c'est l'admin qui fait foi pour ces contenus : modifier `REALISATION_PROJECTS` ou `FAQ` dans `data.py` n'a plus d'effet.
Sauvegardez `instance/egc.db` et les dossiers `static/img/` régulièrement.

## Mode clair / sombre

Un bouton soleil/lune dans la barre de navigation (et le menu mobile) bascule entre les deux thèmes.
Le choix est mémorisé dans le navigateur (`localStorage`, clé `egc-theme`) ; le mode sombre reste le thème par défaut.
Les styles du mode clair sont regroupés en section 4 de `static/css/style.css` (classe `.light` sur `<html>`).

## Animations

Loader · barre de progression de lecture · navbar qui rétrécit · scrollspy avec soulignement animé ·
révélation au scroll (haut / gauche / droite / zoom, en cascade) · compteurs animés · réseau de particules
interactif (canvas, en pause hors écran) · carte hero en 3D + flottement · halo qui suit le curseur ·
boutons magnétiques + balayage lumineux + ondulation · bordure lumineuse tournante (CTA) · menu mobile animé ·
formulaire avec erreurs « shake », état de chargement et toast · bouton retour en haut.
`prefers-reduced-motion` est respecté.

## Formulaire de devis

`POST /api/contact` (JSON) : jeton CSRF, champ piège (honeypot), limite 5 demandes / 10 min / IP,
validation serveur. Les demandes sont stockées dans `instance/egc.db` :

```bash
flask --app app requests        # lister les demandes
```
Pour recevoir un e-mail à chaque demande, renseigner `MAIL_*` dans `.env`.

## Production

```bash
gunicorn wsgi:app -w 3 -b 0.0.0.0:8000
```
Définir une vraie `SECRET_KEY`. Le CDN Tailwind est conservé comme dans le design d'origine ;
pour la production, on peut le remplacer par la CLI Tailwind (build CSS).

## Modifier le contenu
Éditer `data.py` (expertises, détails par page, réalisations, FAQ, horaires, coordonnées…) — les templates bouclent dessus.


## Section Partenaires (page d'accueil)

Elle remplace l'ancien formulaire de contact de l'accueil (le formulaire reste sur `/contact` et `/devis`).

**Ajouter un logo partenaire** : déposez le fichier image dans `static/img/partners/`
(formats `.svg`, `.png`, `.jpg`, `.webp`, `.avif` ; fond transparent recommandé ; hauteur ~100 px minimum).
Il apparaît automatiquement, sans toucher au code ni redémarrer le serveur.

- **Ordre** : alphabétique. Préfixez par un numéro pour le choisir : `01-promogroup.png`, `02-cabinet-diop.svg`.
- **Nom affiché** : déduit du fichier (`01-promo-group.png` → « Promo Group »).
- **Nom précis et lien** (facultatif) : éditez `static/img/partners/partners.json`

```json
{
  "01-promogroup.png": { "name": "Promogroup", "url": "https://www.promogroup.sn" }
}
```

- Les 8 fichiers `exemple-*.svg` sont des **logos d'exemple** : ils disparaissent automatiquement
  dès que vous ajoutez au moins un vrai logo (vous pouvez ensuite les supprimer).
- Les logos défilent en deux rangées (pause au survol) ; en mode « mouvement réduit », ils s'affichent en grille fixe.
- Textes de la section : `PARTNERS_SECTION` et `PARTNER_POINTS` dans `data.py`.


## Logo

Le logo officiel est dans `static/img/` : `logo-egc.png` (512 px, fond transparent, détouré en cercle),
`logo-egc.webp`, `logo-egc-192.png`, `logo-egc-128.png` (navigation et pied de page), `favicon.ico`,
`favicon-32.png`, `apple-touch-icon.png` et `og-image.jpg` (aperçu lors d'un partage sur les réseaux, 1200×630).
Il est utilisé dans la barre de navigation, le pied de page, l'écran de chargement et l'administration.

Pour le changer, remplacez ces fichiers en gardant les mêmes noms.
