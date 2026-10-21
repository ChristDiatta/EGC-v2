"""Contenu éditorial du site EGC Ingénierie.

Tout le contenu est ici : modifier ce fichier suffit pour mettre à jour le site.
Les classes Tailwind sont écrites en entier (pas de concaténation) pour rester lisibles.
"""

SITE = {
    "name": "EGC Ingénierie",
    "title": "EGC Ingénierie - Bureau d'Études Techniques MEP Sénégal & Maroc",
    "tagline": "Énergie & Génie Civil",
    "description": (
        "EGC Ingénierie : bureau d'études techniques MEP au Sénégal et au Maroc. "
        "Électricité, CVC, plomberie, sécurité incendie et efficacité énergétique."
    ),
    "phone": "+221 77 139 19 19",
    "phone_href": "tel:+221771391919",
    "email": "energeniecivil.sn@gmail.com",
    "address": "Cité Municipale, Parcelle 58/A, Sénégal",
    "address_short": "Cité Municipale, Parcelle 58/A",
    "website": "www.energeniecivil.sn",
    "website_href": "https://www.energeniecivil.sn",
}

NAV = [
    {"endpoint": "index", "label": "Accueil"},
    {"endpoint": "a_propos", "label": "EGC"},
    {"endpoint": "expertises", "label": "Expertises"},
    {"endpoint": "secteurs", "label": "Secteurs"},
    {"endpoint": "realisations", "label": "Réalisations"},
    {"endpoint": "methodologie", "label": "Notre méthode"},
    {"endpoint": "contact", "label": "Contact"},
]

NAV_MOBILE = [
    {"endpoint": "index", "label": "Accueil"},
    {"endpoint": "a_propos", "label": "À Propos"},
    {"endpoint": "expertises", "label": "Expertises MEP"},
    {"endpoint": "secteurs", "label": "Secteurs"},
    {"endpoint": "realisations", "label": "Réalisations"},
    {"endpoint": "methodologie", "label": "Méthodologie"},
    {"endpoint": "contact", "label": "Contact"},
]

HERO_MODULES = [
    {"icon": "fa-bolt", "icon_c": "text-cyan-400", "hover": "hover:border-cyan-500/30",
     "title": "Électricité", "sub": "CFO / CFA & Sécurité"},
    {"icon": "fa-snowflake", "icon_c": "text-blue-400", "hover": "hover:border-cyan-500/30",
     "title": "Études CVC", "sub": "Thermique & VMC"},
    {"icon": "fa-droplet", "icon_c": "text-teal-400", "hover": "hover:border-cyan-500/30",
     "title": "Plomberie", "sub": "Fluides & AEP / EU"},
    {"icon": "fa-leaf", "icon_c": "text-green-400", "hover": "hover:border-green-500/30",
     "title": "Énergie", "sub": "Audits & EnR"},
]

HERO_PILLARS = [
    {"icon": "fa-shield-halved", "c": "text-cyan-400", "label": "Normes NF C 15-100 & Européennes"},
    {"icon": "fa-layer-group", "c": "text-green-400", "label": "Approche Multi-lots Majeure"},
    {"icon": "fa-star", "c": "text-amber-400", "label": "Rigueur & Ancrage Local"},
]

STATS = [
    {"value": 2, "suffix": "", "label": "Pays d'Expertise", "sub": "Sénégal & Maroc",
     "border": "border-t-cyan-400", "num": "text-gradient-cyan"},
    {"value": 5, "suffix": "", "label": "Domaines Clés", "sub": "Ingénierie Spécialisée MEP",
     "border": "border-t-green-400", "num": "text-gradient-green"},
    {"value": 6, "suffix": "", "label": "Phases Projet", "sub": "De l'idée à la Réception",
     "border": "border-t-blue-400", "num": "text-cyan-300"},
    {"value": 100, "suffix": "%", "label": "Couverture", "sub": "Toutes régions du Sénégal",
     "border": "border-t-amber-400", "num": "text-gradient-gold"},
]

PILLARS = [
    {"n": 1, "title": "Rigueur Européenne",
     "text": "Méthodologie structurée, normes et référentiels européens appliqués rigoureusement à chaque étude.",
     "box": "bg-cyan-500/10 border-cyan-500/30 text-cyan-400"},
    {"n": 2, "title": "Ancrage Sénégalais",
     "text": "Connaissance fine du contexte local, de la réglementation environnementale et des contraintes de chantier.",
     "box": "bg-green-500/10 border-green-500/30 text-green-400"},
    {"n": 3, "title": "Performance Optimisée",
     "text": "Des solutions techniques durables et équilibrées en termes de coût, de délai et de performance énergétique.",
     "box": "bg-amber-500/10 border-amber-500/30 text-amber-400"},
]

EXPERTISES = [
    {
        "icon": "fa-bolt", "title": "Études Électricité",
        "subtitle": "Courant Fort & Courant Faible",
        "top": "border-t-cyan-400",
        "box": "bg-cyan-500/10 border-cyan-500/30 text-cyan-400",
        "text": "text-cyan-400",
        "items": [
            "Courant fort et courant faible (CFO/CFA)",
            "Dimensionnement des tableaux électriques",
            "Conformité NF C 15-100",
            "Schémas unifilaires et multifilaires",
            "Calculs de bilans de puissance",
            "Études d'éclairage intérieur / extérieur",
        ],
        "footer": "Applications : Tertiaire, Résidentiel & Industriel",
    },
    {
        "icon": "fa-snowflake", "title": "Études CVC",
        "subtitle": "Climatisation, Ventilation & Chauffage",
        "top": "border-t-blue-500",
        "box": "bg-blue-500/10 border-blue-500/30 text-blue-400",
        "text": "text-blue-400",
        "items": [
            "Calculs de charges thermiques",
            "Dimensionnement des réseaux aérauliques",
            "Sélection des équipements CVC performants",
            "Ventilation Mécanique Contrôlée (VMC)",
            "Conformité aux réglementations thermiques",
            "Optimisation de l'air ambiant",
        ],
        "footer": "Confort thermique & Économies d'énergie",
    },
    {
        "icon": "fa-faucet-drip", "title": "Plomberie & Fluides",
        "subtitle": "Eau, Assainissement & Hydraulique",
        "top": "border-t-teal-400",
        "box": "bg-teal-500/10 border-teal-500/30 text-teal-400",
        "text": "text-teal-400",
        "items": [
            "Réseaux d'eau potable (AEP)",
            "Assainissement et eaux usées (EU/EV)",
            "Réseaux d'Eaux Pluviales (EP)",
            "Groupes de surpression & Réservoirs",
            "Études techniques de piscines",
            "Plans détaillés des réseaux sanitaires",
        ],
        "footer": "Gestion hydraulique globale & sanitaire",
    },
    {
        "icon": "fa-fire-extinguisher", "title": "Sécurité Incendie",
        "subtitle": "Protéger les Personnes & les Biens",
        "top": "border-t-red-500",
        "box": "bg-red-500/10 border-red-500/30 text-red-400",
        "text": "text-red-400",
        "items": [
            "Études de sécurité incendie réglementaires",
            "Réseaux d'extinction (RIA, Sprinklers)",
            "Systèmes de Désenfumage mécanique/naturel",
            "Détection automatique incendie (SSI)",
            "Plans d'évacuation & moyens de secours",
        ],
        "footer": "Normes ERP, IGH & Sites Industriels",
    },
    {
        "icon": "fa-leaf", "title": "Efficacité Énergétique",
        "subtitle": "Consommer Mieux, Dépenser Moins",
        "top": "border-t-green-500",
        "box": "bg-green-500/10 border-green-500/30 text-green-400",
        "text": "text-green-400",
        "items": [
            "Audits énergétiques complets",
            "Simulation Thermique Dynamique (STD)",
            "Optimisation globale des consommations",
            "Intégration Énergies Renouvelables (Solaire)",
            "Conformité aux normes environnementales",
        ],
        "footer": "Transition écologique & réduction de coûts",
    },
]

STEPS = [
    {"n": "01", "phase": 1, "title": "Études de Faisabilité",
     "text": "Analyse approfondie des besoins, évaluation des contraintes du site et pré-dimensionnement des lots techniques."},
    {"n": "02", "phase": 2, "title": "AVP - Avant-Projet",
     "text": "Choix des solutions techniques, définition des principes de distribution et premières estimations financières."},
    {"n": "03", "phase": 3, "title": "APD - Avant-Projet Détaillé",
     "text": "Dimensionnement précis, calculs de charges, élaboration des plans complets et notes techniques détaillées."},
    {"n": "04", "phase": 4, "title": "DCE - Dossier Consultation",
     "text": "Rédaction des pièces écrites et graphiques permettant le lancement de la consultation des entreprises."},
    {"n": "05", "phase": 5, "title": "Suivi des Travaux",
     "text": "Suivi rigoureux de chantier, visa des plans d'exécution et contrôle de conformité des installations."},
    {"n": "06", "phase": 6, "title": "Réception & Levée de Réserves",
     "text": "Assistance aux opérations de réception, gestion de la levée des réserves et remise des dossiers DOE finals."},
]

TOOLS = ["AutoCAD", "Revit MEP (BIM)", "CYPCAD", "Caneco BT", "Dialux evo", "PVSyst", "Pleiades STD"]

SECTORS = [
    {"icon": "fa-building", "grad": "text-gradient-cyan", "title": "Résidentiel",
     "box": "bg-cyan-500/10 border-cyan-500/30 text-cyan-400",
     "text": "Immeubles de grand standing, villas individuelles, complexes résidentiels et programmes immobiliers neufs ou rénovations."},
    {"icon": "fa-hotel", "grad": "text-gradient-green", "title": "Tertiaire",
     "box": "bg-green-500/10 border-green-500/30 text-green-400",
     "text": "Bureaux, centres commerciaux, hôtels, établissements de santé, écoles et établissements recevant du public (ERP)."},
    {"icon": "fa-industry", "grad": "text-gradient-gold", "title": "Industriel",
     "box": "bg-amber-500/10 border-amber-500/30 text-amber-400",
     "text": "Unités de production, entrepôts logistiques, usines et sites techniques nécessitant des fluides complexes."},
]

CLIENTS = [
    {"icon": "fa-city", "c": "text-cyan-400", "label": "Promoteurs Immobiliers"},
    {"icon": "fa-compass-drafting", "c": "text-green-400", "label": "Architectes"},
    {"icon": "fa-helmet-safety", "c": "text-amber-400", "label": "Entreprises BTP"},
    {"icon": "fa-user-tie", "c": "text-blue-400", "label": "Maîtres d'Ouvrage"},
]

CONTACT_ITEMS = [
    {"icon": "fa-phone", "label": "Téléphone", "value": SITE["phone"], "href": SITE["phone_href"],
     "box": "bg-cyan-500/10 border-cyan-500/30 text-cyan-400", "hover": "hover:text-cyan-400"},
    {"icon": "fa-envelope", "label": "E-mail", "value": SITE["email"], "href": "mailto:" + SITE["email"],
     "box": "bg-green-500/10 border-green-500/30 text-green-400", "hover": "hover:text-green-400"},
    {"icon": "fa-location-dot", "label": "Adresse Siege", "value": SITE["address"], "href": None,
     "box": "bg-amber-500/10 border-amber-500/30 text-amber-400", "hover": ""},
    {"icon": "fa-globe", "label": "Site Web", "value": SITE["website"], "href": SITE["website_href"],
     "box": "bg-blue-500/10 border-blue-500/30 text-blue-400", "hover": "hover:text-blue-400"},
]

# Valeur envoyée => libellé affiché
LOTS = [
    ("Electricite", "Électricité"),
    ("CVC", "CVC"),
    ("Plomberie", "Plomberie/Fluides"),
    ("Incendie", "Securité Incendie"),
    ("Energie", "Audit Énergétique"),
    ("Tous", "Multi-lots MEP"),
]

FOOTER_LINKS = [
    {"endpoint": "index", "label": "Accueil"},
    {"endpoint": "a_propos", "label": "À propos d'EGC"},
    {"endpoint": "expertises", "label": "Expertises Métiers"},
    {"endpoint": "secteurs", "label": "Secteurs d'intervention"},
    {"endpoint": "realisations", "label": "Réalisations"},
    {"endpoint": "methodologie", "label": "Méthodologie en 6 phases"},
    {"endpoint": "contact", "label": "Contact"},
    {"endpoint": "devis", "label": "Demande de devis"},
]


# =========================================================================== #
# Pages dédiées : contenu détaillé
# =========================================================================== #

# --- Liaison expertises <-> pages de détail <-> lots du formulaire ---------- #
for _e, (_slug, _lot) in zip(EXPERTISES, [
    ("electricite", "Electricite"),
    ("cvc", "CVC"),
    ("plomberie-fluides", "Plomberie"),
    ("securite-incendie", "Incendie"),
    ("efficacite-energetique", "Energie"),
]):
    _e["slug"], _e["lot"] = _slug, _lot

# --- À propos ---------------------------------------------------------------- #
ABOUT_INTRO = [
    "Énergie & Génie Civil Ingénierie (EGC) est un bureau d'études techniques spécialisé dans les lots MEP "
    "(Mécanique, Électricité, Plomberie) : électricité, CVC, plomberie et fluides, sécurité incendie et efficacité énergétique.",
    "Nous intervenons auprès des promoteurs, architectes, entreprises du BTP et maîtres d'ouvrage, au Sénégal comme au Maroc, "
    "avec un objectif simple : des installations techniques fiables, conformes et économes à l'usage.",
]

MISSION = ("Concevoir des installations techniques performantes, sûres et maîtrisées en coût, "
           "en alliant rigueur européenne et connaissance du terrain sénégalais.")

VALUES = [
    {"icon": "fa-ruler-combined", "box": "bg-cyan-500/10 border-cyan-500/30 text-cyan-400",
     "title": "Rigueur", "text": "Notes de calcul tracées, hypothèses explicites, plans cohérents entre lots : chaque choix technique est justifié."},
    {"icon": "fa-handshake", "box": "bg-green-500/10 border-green-500/30 text-green-400",
     "title": "Transparence", "text": "Des livrables clairs, un planning partagé et un interlocuteur identifié du début à la fin du projet."},
    {"icon": "fa-seedling", "box": "bg-amber-500/10 border-amber-500/30 text-amber-400",
     "title": "Durabilité", "text": "Nous privilégions les solutions sobres, maintenables et compatibles avec les énergies renouvelables."},
    {"icon": "fa-location-crosshairs", "box": "bg-blue-500/10 border-blue-500/30 text-blue-400",
     "title": "Proximité", "text": "Une équipe qui connaît les contraintes locales : climat, approvisionnement, pratiques de chantier."},
]

COMMITMENTS = [
    {"icon": "fa-scale-balanced", "title": "Conformité réglementaire",
     "text": "Application des normes et réglementations en vigueur (NF C 15-100, référentiels européens, règles locales)."},
    {"icon": "fa-puzzle-piece", "title": "Coordination inter-lots",
     "text": "Synthèse des réseaux électricité / CVC / plomberie pour éviter les conflits en phase chantier."},
    {"icon": "fa-comments", "title": "Réactivité",
     "text": "Réponse à vos demandes de devis sous 24 h et points d'avancement réguliers pendant les études."},
    {"icon": "fa-coins", "title": "Maîtrise des coûts",
     "text": "Choix techniques arbitrés entre investissement, consommation et maintenance sur la durée de vie."},
]

PRESENCE = [
    {"flag": "Sénégal", "icon": "fa-location-dot", "c": "text-green-400",
     "text": "Siège à Cité Municipale. Intervention sur l'ensemble des régions du Sénégal : Dakar, Thiès, Saint-Louis, Casamance et intérieur du pays."},
    {"flag": "Maroc", "icon": "fa-location-dot", "c": "text-red-400",
     "text": "Études et accompagnement de projets au Maroc, avec prise en compte du contexte thermique et réglementaire local."},
]

# --- Détail des expertises --------------------------------------------------- #
EXPERTISE_DETAILS = {
    "electricite": {
        "intro": "De l'alimentation en moyenne ou basse tension aux réseaux courants faibles, nous dimensionnons des installations "
                 "électriques sûres, évolutives et conformes, adaptées à l'usage réel du bâtiment.",
        "prestations": [
            ("Bilan de puissance", "Recensement des charges, coefficients de simultanéité et choix de la puissance souscrite et des sources de secours."),
            ("Distribution BT", "Dimensionnement des tableaux, câbles, protections et sélectivité ; schémas unifilaires et multifilaires."),
            ("Éclairage", "Calculs photométriques intérieurs et extérieurs, éclairage de sécurité, choix de luminaires économes."),
            ("Courants faibles", "Réseaux VDI, contrôle d'accès, vidéosurveillance, interphonie et sonorisation."),
        ],
        "livrables": ["Notes de calcul", "Schémas unifilaires et plans d'implantation", "Cahier des clauses techniques (CCTP)",
                      "Bordereau quantitatif (DPGF)", "Visa des plans d'exécution"],
        "normes": ["NF C 15-100", "NF C 14-100", "EN 12464-1 (éclairage)", "Protection contre la foudre (série EN 62305)"],
        "faq": [("Étudiez-vous le groupe électrogène et l'onduleur ?", "Oui. Nous dimensionnons les sources de remplacement et de sécurité en fonction des charges critiques de votre site."),
                ("Pouvez-vous intégrer le solaire photovoltaïque ?", "Oui, en lien avec notre pôle efficacité énergétique (simulation PVSyst).")],
    },
    "cvc": {
        "intro": "Confort thermique, qualité de l'air et sobriété énergétique : nous concevons des systèmes de climatisation, "
                 "ventilation et chauffage adaptés aux climats chauds du Sénégal et du Maroc.",
        "prestations": [
            ("Charges thermiques", "Calcul des apports et déperditions par local pour dimensionner au plus juste les équipements."),
            ("Climatisation", "Choix des systèmes (split, VRV/VRF, groupes d'eau glacée) selon l'usage, le coût global et la maintenance."),
            ("Ventilation & VMC", "Réseaux aérauliques, débits d'air neuf, extraction des locaux humides et techniques."),
            ("Régulation", "Principes de régulation et de gestion technique pour limiter les consommations."),
        ],
        "livrables": ["Notes de calcul thermique", "Plans de réseaux aérauliques et frigorifiques", "Schémas de principe",
                      "CCTP et DPGF", "Fiches de sélection des équipements"],
        "normes": ["EN 12831 (déperditions)", "NF DTU 68.3 (VMC)", "EN 16798 (qualité d'air)", "Réglementation thermique applicable (dont RTCM au Maroc)"],
        "faq": [("Quel système choisir pour un immeuble de bureaux ?", "Cela dépend de la surface, de l'occupation et du budget. Nous comparons les solutions sur le coût global (investissement + exploitation)."),
                ("Faites-vous la ventilation de parkings ?", "Oui, y compris le désenfumage en lien avec le lot sécurité incendie.")],
    },
    "plomberie-fluides": {
        "intro": "Eau potable, eaux usées, eaux pluviales, surpression, piscines : nous concevons des réseaux hydrauliques "
                 "fiables, correctement dimensionnés et faciles à entretenir.",
        "prestations": [
            ("Alimentation en eau potable", "Bilan des besoins, dimensionnement des colonnes, bâches, surpresseurs et production d'eau chaude."),
            ("Assainissement", "Réseaux d'eaux usées et eaux vannes, ventilation primaire, raccordement et pré-traitement."),
            ("Eaux pluviales", "Collecte, évacuation et rétention adaptées à l'intensité des pluies locales."),
            ("Piscines & bassins", "Hydraulique, traitement de l'eau, local technique et plans détaillés."),
        ],
        "livrables": ["Notes de dimensionnement", "Plans de réseaux AEP / EU / EV / EP", "Schémas de principe des locaux techniques",
                      "CCTP et DPGF", "Visa des plans d'exécution"],
        "normes": ["NF DTU 60.11 (plomberie sanitaire)", "EN 806 (eau potable)", "EN 12056 (évacuation gravitaire)"],
        "faq": [("Intégrez-vous la récupération d'eau de pluie ?", "Oui, lorsque le projet s'y prête : usages non potables, arrosage, nettoyage."),
                ("Étudiez-vous les réseaux extérieurs ?", "Nous traitons les réseaux de la parcelle et le raccordement aux réseaux publics.")],
    },
    "securite-incendie": {
        "intro": "La sécurité des personnes et des biens se conçoit dès l'avant-projet. Nous définissons les dispositifs "
                 "de détection, d'alarme, de désenfumage et d'extinction adaptés à la classification de votre bâtiment.",
        "prestations": [
            ("Analyse réglementaire", "Classement du bâtiment (ERP, IGH, habitation, industriel) et exigences associées."),
            ("Détection & alarme", "Conception du système de sécurité incendie (SSI), zonage et report d'alarmes."),
            ("Désenfumage", "Désenfumage naturel ou mécanique des circulations, escaliers et parkings."),
            ("Extinction", "Robinets d'incendie armés, colonnes, sprinklers, extincteurs et réserves d'eau."),
        ],
        "livrables": ["Note de sécurité incendie", "Plans de détection, désenfumage et extinction", "Plans d'évacuation et de secours",
                      "CCTP et DPGF", "Dossier pour la commission de sécurité"],
        "normes": ["Règlement ERP / IGH applicable", "NF S 61-931 (SSI)", "EN 12845 (sprinklers)"],
        "faq": [("Accompagnez-vous le passage en commission de sécurité ?", "Nous préparons les pièces techniques du dossier et assistons aux opérations de réception."),
                ("Étudiez-vous les bâtiments existants ?", "Oui, pour la mise en conformité : diagnostic, mesures correctives et chiffrage.")],
    },
    "efficacite-energetique": {
        "intro": "Réduire les consommations sans sacrifier le confort : audits, simulations et intégration des énergies "
                 "renouvelables pour des bâtiments plus sobres et des factures mieux maîtrisées.",
        "prestations": [
            ("Audit énergétique", "Analyse des consommations, relevés sur site, identification des gisements d'économies."),
            ("Simulation thermique dynamique", "Évaluation du confort et des besoins annuels pour comparer les variantes de conception."),
            ("Énergies renouvelables", "Dimensionnement de centrales solaires photovoltaïques et de production d'eau chaude solaire."),
            ("Plan d'actions", "Hiérarchisation des travaux, chiffrage et temps de retour sur investissement."),
        ],
        "livrables": ["Rapport d'audit", "Résultats de simulation (Pleiades STD)", "Étude de productible solaire (PVSyst)",
                      "Plan d'actions chiffré", "Recommandations de suivi des consommations"],
        "normes": ["ISO 50001 (management de l'énergie)", "EN 16247 (audits énergétiques)", "Réglementation thermique applicable"],
        "faq": [("Un audit est-il utile pour un bâtiment neuf ?", "Oui : la simulation en phase conception évite des surcoûts d'exploitation durables."),
                ("Calculez-vous la rentabilité du solaire ?", "Oui, avec production estimée, coût d'investissement et temps de retour.")],
    },
}

# --- Secteurs ---------------------------------------------------------------- #
SECTOR_DETAILS = {
    "Résidentiel": {
        "intro": "Confort, sécurité et charges maîtrisées pour les occupants, rentabilité pour le promoteur.",
        "projets": ["Immeubles collectifs et résidences de standing", "Villas individuelles et lotissements", "Rénovation lourde de logements"],
        "enjeux": ["Climatisation performante et silencieuse", "Alimentation en eau fiable (surpression, bâches)", "Comptages et répartition des charges"],
    },
    "Tertiaire": {
        "intro": "Des bâtiments ouverts au public ou occupés en continu, où disponibilité et sécurité sont déterminantes.",
        "projets": ["Bureaux et sièges sociaux", "Hôtels, résidences hôtelières et restaurants", "Établissements de santé, écoles et ERP", "Centres commerciaux"],
        "enjeux": ["Sécurité incendie et évacuation", "Continuité de service (groupes, onduleurs)", "Coûts d'exploitation et maintenance"],
    },
    "Industriel": {
        "intro": "Des process exigeants en énergie, en fluides et en fiabilité, avec des contraintes de site spécifiques.",
        "projets": ["Unités de production et usines", "Entrepôts logistiques", "Sites techniques et chambres froides"],
        "enjeux": ["Puissance et qualité de l'énergie", "Ventilation et traitement de l'air", "Réseaux de fluides et protection incendie"],
    },
}

CLIENT_ROLES = {
    "Promoteurs Immobiliers": "Études techniques optimisées pour tenir les budgets, les délais de commercialisation et la qualité de livraison.",
    "Architectes": "Collaboration dès l'esquisse pour intégrer gaines, locaux techniques et réseaux sans compromettre le parti architectural.",
    "Entreprises BTP": "Plans d'exécution, notes de calcul et assistance technique pour sécuriser les offres et la mise en œuvre.",
    "Maîtres d'Ouvrage": "Pilotage technique des lots MEP, avis indépendants et contrôle de conformité jusqu'à la réception.",
}

# --- Réalisations : missions types (à remplacer par vos références réelles) -- #
REALISATIONS = [
    {"icon": "fa-building", "tag": "Résidentiel", "box": "bg-cyan-500/10 border-cyan-500/30 text-cyan-400",
     "title": "Immeuble résidentiel collectif",
     "text": "Étude complète des lots techniques d'un programme de logements : distribution électrique, climatisation, alimentation en eau avec surpression et sécurité incendie des parties communes.",
     "lots": ["Électricité", "CVC", "Plomberie", "Incendie"], "phases": "AVP → Suivi des travaux"},
    {"icon": "fa-hotel", "tag": "Tertiaire", "box": "bg-green-500/10 border-green-500/30 text-green-400",
     "title": "Hôtel et résidence hôtelière",
     "text": "Conception des installations d'un établissement d'accueil : climatisation des chambres, production d'eau chaude, piscine, éclairage d'ambiance et dispositifs de sécurité.",
     "lots": ["Électricité", "CVC", "Plomberie", "Piscine"], "phases": "APD → DCE"},
    {"icon": "fa-briefcase", "tag": "Tertiaire", "box": "bg-blue-500/10 border-blue-500/30 text-blue-400",
     "title": "Immeuble de bureaux",
     "text": "Dimensionnement d'un plateau de bureaux : bilan de puissance, groupe de secours, climatisation par zones, réseaux courants faibles et désenfumage des circulations.",
     "lots": ["Électricité", "CVC", "Courants faibles"], "phases": "Faisabilité → APD"},
    {"icon": "fa-hospital", "tag": "Tertiaire", "box": "bg-red-500/10 border-red-500/30 text-red-400",
     "title": "Établissement de santé",
     "text": "Installations à haute exigence de continuité : alimentation sécurisée, traitement d'air des zones sensibles, fluides et protection incendie adaptée au public vulnérable.",
     "lots": ["Électricité", "CVC", "Fluides", "Incendie"], "phases": "AVP → DCE"},
    {"icon": "fa-industry", "tag": "Industriel", "box": "bg-amber-500/10 border-amber-500/30 text-amber-400",
     "title": "Entrepôt logistique et unité de production",
     "text": "Distribution de forte puissance, éclairage industriel, ventilation, réseaux de fluides et protection incendie d'un site de stockage ou de production.",
     "lots": ["Électricité", "Ventilation", "Incendie"], "phases": "APD → Suivi des travaux"},
    {"icon": "fa-solar-panel", "tag": "Énergie", "box": "bg-teal-500/10 border-teal-500/30 text-teal-400",
     "title": "Audit et centrale solaire en toiture",
     "text": "Audit des consommations d'un bâtiment existant, plan d'actions chiffré et étude d'une installation photovoltaïque en autoconsommation.",
     "lots": ["Audit", "Photovoltaïque", "Simulation"], "phases": "Audit → Plan d'actions"},
]

REALISATIONS_FILTERS = ["Tous", "Résidentiel", "Tertiaire", "Industriel", "Énergie"]

# --- Méthodologie : détail par phase ---------------------------------------- #
STEP_DETAILS = {
    1: {"actions": ["Recueil du programme et des contraintes du site", "Pré-dimensionnement des lots", "Identification des risques techniques"],
        "livrables": ["Note de faisabilité", "Premier ordre de grandeur des coûts"]},
    2: {"actions": ["Comparaison de variantes techniques", "Principes de distribution et locaux techniques", "Coordination avec l'architecte"],
        "livrables": ["Notice descriptive", "Plans de principe", "Estimation financière"]},
    3: {"actions": ["Calculs détaillés par lot", "Plans complets et schémas", "Synthèse des réseaux entre lots"],
        "livrables": ["Notes de calcul", "Plans APD", "Estimation affinée"]},
    4: {"actions": ["Rédaction des CCTP", "Quantitatifs (DPGF)", "Aide à l'analyse des offres"],
        "livrables": ["Dossier de consultation complet", "Rapport d'analyse des offres"]},
    5: {"actions": ["Visa des plans d'exécution", "Visites de chantier et comptes rendus", "Contrôle de conformité des installations"],
        "livrables": ["Comptes rendus de visite", "Avis sur les plans et échantillons"]},
    6: {"actions": ["Opérations préalables à la réception", "Suivi de la levée des réserves", "Collecte des documents d'exploitation"],
        "livrables": ["Procès-verbaux", "Dossier des ouvrages exécutés (DOE)"]},
}

COLLAB = [
    {"icon": "fa-user-check", "title": "Un interlocuteur unique", "text": "Un chef de projet pilote l'ensemble des lots et vous répond directement."},
    {"icon": "fa-file-circle-check", "title": "Livrables validés à chaque phase", "text": "Vous validez chaque étape avant de passer à la suivante, sans surprise."},
    {"icon": "fa-cubes", "title": "Maquette BIM possible", "text": "Modélisation Revit MEP pour détecter les conflits avant le chantier."},
]

# --- Contact / devis --------------------------------------------------------- #
HOURS = [("Lundi – Vendredi", "08h30 – 18h00"), ("Samedi", "09h00 – 13h00"), ("Dimanche", "Fermé")]

QUOTE_STEPS = [
    {"n": 1, "title": "Vous décrivez votre projet", "text": "Type de bâtiment, localisation, lots concernés et, si possible, plans ou programme."},
    {"n": 2, "title": "Nous analysons votre demande", "text": "Un ingénieur étudie le périmètre et peut vous appeler pour préciser certains points."},
    {"n": 3, "title": "Vous recevez une offre chiffrée", "text": "Proposition détaillée : mission, livrables, planning et honoraires."},
]

QUOTE_REASSURANCE = [
    {"icon": "fa-clock", "text": "Réponse sous 24 h"},
    {"icon": "fa-lock", "text": "Données confidentielles"},
    {"icon": "fa-circle-check", "text": "Sans engagement"},
]

FAQ = [
    ("Combien de temps pour recevoir un devis ?", "Nous répondons en général sous 24 h. Pour un projet complexe, nous revenons vers vous pour affiner le besoin avant de chiffrer."),
    ("Quels documents joindre à ma demande ?", "Plans architecte, programme, surface, localisation et calendrier visé. Une description simple suffit pour une première estimation."),
    ("Intervenez-vous en dehors de Dakar ?", "Oui, sur l'ensemble des régions du Sénégal, ainsi qu'au Maroc."),
    ("Puis-je commander un seul lot ?", "Bien sûr. Vous pouvez nous confier un lot isolé ou une mission multi-lots avec coordination."),
    ("Proposez-vous un suivi de chantier ?", "Oui, de la visite ponctuelle au suivi complet, jusqu'à la réception et la levée des réserves."),
]

# --- Partenaires (page d'accueil) --------------------------------------------- #
# Les LOGOS ne se déclarent pas ici : déposez simplement les fichiers image dans
# static/img/partners/ (voir README). Seuls les textes de la section sont ici.
PARTNERS_SECTION = {
    "kicker": "Nos Partenaires",
    "title": "Un réseau de confiance pour vos projets",
    "sub": ("Promoteurs, architectes, entreprises du BTP et fournisseurs : "
            "des collaborations durables pour mener chaque projet à bien."),
}

PARTNER_POINTS = [
    {"icon": "fa-handshake", "c": "cyan", "title": "Relations durables",
     "text": "Une collaboration de long terme avec maîtres d'ouvrage, architectes et entreprises."},
    {"icon": "fa-diagram-project", "c": "green", "title": "Projets coordonnés",
     "text": "Des études MEP synchronisées avec l'architecture, la structure et les autres corps d'état."},
    {"icon": "fa-award", "c": "amber", "title": "Qualité partagée",
     "text": "Des exigences communes de conformité, de délais et de performance technique."},
]


# --- Réalisations : projets réalisés par domaine ------------------------------- #
# Chaque domaine affiche 2 projets avec photo. Pour ajouter une photo, déposez dans
# static/img/realisations/ un fichier nommé  <domaine>-1.jpg  et  <domaine>-2.jpg
# (jpg, png, webp ou avif), par exemple  immeuble-residentiel-1.jpg.
# Tant que la photo est absente, une image d'attente s'affiche.
# À RENSEIGNER : "title" (nom du projet), "lieu" et "annee" (facultatifs, masqués si vides).
for _r, _slug in zip(REALISATIONS, [
    "immeuble-residentiel", "hotel-residence", "immeuble-bureaux",
    "etablissement-sante", "entrepot-usine", "audit-solaire",
]):
    _r["slug"] = _slug

REALISATION_PROJECTS = {
    "immeuble-residentiel": [
        {"title": "Chantier d'immeubles résidentiels", "lieu": "", "annee": ""},
        {"title": "Installations électriques en cours de pose", "lieu": "", "annee": ""},
    ],
    "hotel-residence": [
        {"title": "Hôtel / résidence - Projet 1", "lieu": "", "annee": ""},
        {"title": "Hôtel / résidence - Projet 2", "lieu": "", "annee": ""},
    ],
    "immeuble-bureaux": [
        {"title": "Immeuble de bureaux - Projet 1", "lieu": "", "annee": ""},
        {"title": "Immeuble de bureaux - Projet 2", "lieu": "", "annee": ""},
    ],
    "etablissement-sante": [
        {"title": "Établissement de santé - Projet 1", "lieu": "", "annee": ""},
        {"title": "Établissement de santé - Projet 2", "lieu": "", "annee": ""},
    ],
    "entrepot-usine": [
        {"title": "Entrepôt / unité de production - Projet 1", "lieu": "", "annee": ""},
        {"title": "Entrepôt / unité de production - Projet 2", "lieu": "", "annee": ""},
    ],
    "audit-solaire": [
        {"title": "Audit et solaire - Projet 1", "lieu": "", "annee": ""},
        {"title": "Audit et solaire - Projet 2", "lieu": "", "annee": ""},
    ],
}
