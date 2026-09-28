# Digital-Buro — nouveau site vitrine

Site statique (HTML/CSS/JS pur, aucun framework) généré par un petit script Python.
Objectif : **SEO local** (« réparation imprimante Saint-Gilles », « réparation PC Bruxelles »…),
**pages d'atterrissage Google Ads** et modernisation complète de www.digital-buro.be.

## Structure

```
build.py              générateur : assemble les pages, JSON-LD, sitemap, robots, contrôles SEO
src/data/site.json    coordonnées, horaires, services, marques, note Google, suivi Ads
src/data/pages.json   titres, meta descriptions, fil d'Ariane, langues de chaque page
src/pages/            contenu des pages (gabarits Jinja2)
src/templates/        mise en page commune, en-tête, pied de page, composants
src/assets/           CSS, JS, police Inter (auto-hébergée), icônes et illustrations
src/static/           .htaccess, formulaire PHP (api/contact.php), favicons
public/               ⇦ SITE FINAL À METTRE EN LIGNE (généré, ne pas modifier à la main)
tools/                outils de développement (logo, captures d'écran) — non déployés
```

## Modifier puis régénérer le site

```bash
pip install -r requirements.txt
python build.py            # génère public/ et affiche le rapport SEO
python build.py --serve    # idem + aperçu sur http://localhost:8080
```

Le rapport vérifie à chaque build : liens internes cassés, un seul `<h1>` par page,
longueur et unicité des titres / descriptions, images sans `alt`.

- Horaires, téléphone, note Google… : `src/data/site.json` (répercuté partout, y compris dans les données structurées).
- Titres et descriptions Google : `src/data/pages.json`.
- Textes : `src/pages/*.html`.

## Mise en ligne (hébergement OVH actuel)

1. Sauvegarder l'ancien site (FTP), puis **supprimer ses fichiers** : `index.html`, `Presentation.html`,
   `Principe-impression.html`, `Reclamation.php`, `contact.php`, dossiers `css/`, `js/`, `images/`, `fonts/`.
2. Envoyer **le contenu** du dossier `public/` à la racine (`www/`), **y compris `.htaccess`** (fichier caché).
3. Vérifier que PHP ≥ 7.2 est actif (espace client OVH), puis créer l'adresse `site@digital-buro.be`
   (ou modifier `FROM_EMAIL` dans `api/contact.php`) : c'est l'expéditeur des e-mails du formulaire.
4. Tester : le formulaire de contact, `https://digital-buro.be` → doit rediriger vers `https://www.digital-buro.be`,
   et les anciennes adresses (`/Presentation.html`, `/contact.php`…) → redirection 301 vers les nouvelles pages.

## Après la mise en ligne (indispensable pour le SEO local)

- **Google Search Console** : ajouter le domaine, envoyer `https://www.digital-buro.be/sitemap.xml`, demander l'indexation de l'accueil et des pages de services.
- **Fiche Google (Google Business Profile)** — c'est elle qui fait apparaître le magasin dans la carte :
  catégorie principale « Service de réparation d'ordinateurs » + « Magasin informatique », « Service de réparation d'imprimantes » ;
  lister les services en liant chaque page du site ; ajouter des photos récentes ; publier une actualité par mois ;
  répondre à chaque avis et en demander aux clients satisfaits.
- **Cohérence NAP** : même nom, adresse et téléphone partout (Pages d'Or, Yelp, Kompass, koifaire…), avec le lien vers le nouveau site.
- **Bing Places** : importer la fiche Google (5 minutes).

## Google Ads

- Chaque groupe d'annonces pointe vers **sa** page : imprimantes → `/reparation-imprimante/`, PC → `/reparation-ordinateur/`,
  Mac → `/reparation-mac/`, GSM → `/reparation-gsm-tablette/`, toner → `/cartouches-toners/`, B2B → `/entreprises/`.
  Titre de page = mot-clé de l'annonce : meilleur Niveau de qualité, donc clics moins chers.
- **Suivi des conversions** : renseigner `tracking` dans `src/data/site.json` (`google_ads_id` = `AW-…`,
  libellés de conversion « appel » et « formulaire »), puis relancer `python build.py`.
  La bannière de consentement (RGPD / Consent Mode) s'active alors automatiquement ; sans identifiant, **aucun** traceur n'est chargé.
  Sont mesurés : clics sur le numéro, envois du formulaire, demandes d'itinéraire.

## À confirmer avec le client

| Point | Pourquoi |
|---|---|
| **Réparation de GSM / tablettes** | Page créée car demandée dans le brief, mais absente de l'ancien site. À supprimer si le magasin ne le fait pas. |
| **Pages NL et EN** (`/nl/`, `/en/`) | Captent les recherches néerlandophones et des expatriés. À garder si l'accueil en NL/EN est possible. |
| Année de début du dirigeant | L'ancien site (2017) annonçait 30 ans d'expérience : on pourrait écrire « près de 40 ans » / « depuis 1987 ». |
| Diagnostic : payant ? tarif ? garantie ? délais ? | À afficher clairement (FAQ) : rassure et évite les avis négatifs sur le prix du diagnostic. |
| GSM 0486 65 91 04 (listé sur Pages d'Or), WhatsApp ? | Un bouton WhatsApp augmenterait les contacts mobiles. |
| « Ingénieurs et techniciens certifiés » | Mention de l'ancien site non reprise faute de pouvoir la vérifier. |
| WebShop (digital-buro.1.ufp.de) | Lien mort (404) : retiré. À réintégrer si une nouvelle boutique existe. |
| Photos réelles | Intérieur, comptoir, atelier, technicien au travail : remplaceraient avantageusement les illustrations (la photo de vitrine actuelle est en basse définition). |
| Lien « laisser un avis » | Renseigner `google.review_url` (lien fourni dans l'espace Google Business Profile). |
| Adresse e-mail | Une adresse `contact@digital-buro.be` ferait plus professionnel que `@skynet.be`. |
| Congés et jours fériés | L'indicateur « Ouvert / Fermé » suit les horaires habituels uniquement. |
| Note Google | 4,7/5 et « plus de 440 avis » relevés le 28/09/2026 : à actualiser de temps en temps dans `site.json`. |

## Choix de design

- Charte « White concrete, single ember » : toile blanche, Inter à interlettrage négatif, un seul accent Ember `#ff5900`,
  rayons 12 px, filets fins, pas d'ombres, cadres sombres (barre d'annonce Carbon, pied de page Abyss).
- **Boutons Ember en texte noir** plutôt que blanc : contraste 6,7:1 (norme WCAG AA) contre 3,1:1 en blanc, et c'est le
  code couleur classique des ateliers de réparation (orange et noir).
- Logo modernisé : « Digital-Buro » en Inter, le trait d'union devient l'étincelle Ember ; favicon « D-B » dans la continuité de l'ancien.
- Police Inter auto-hébergée (42 Ko, aucun appel à Google Fonts), carte Google chargée uniquement au clic : rapide et conforme au RGPD.
