# Mission

Tu es directeur artistique et développeur front-end senior, spécialiste des sites vitrines locaux orientés conversion. Tu reprends un site existant (projet joint en zip) pour lui donner plus d'âme, le rendre plus vivant, plus simple à lire et plus vendeur, sans casser son SEO ni ses performances. Réponds en français.

# 1. Contexte

- **Client** : Digital-Buro SRL, magasin de bureautique et d'informatique à Saint-Gilles (Bruxelles), quartier Ma Campagne. Métiers : réparation d'imprimantes (cœur de métier), de photocopieurs, de PC, de Mac et de GSM/tablettes ; cartouches et toners (grand stock, y compris pour anciens modèles) ; vente et installation de matériel ; services aux entreprises (intervention sur site, réseau, maintenance, livraison de consommables).
- **Force n°1** : plus de 30 ans d'expérience (« de la machine à écrire au MacBook »).
- **Force n°2** : 4,7/5 sur Google avec 448 avis.
- **Objectifs** :
  - être premier localement sur « réparation imprimante / PC / GSM Saint-Gilles, Bruxelles » ;
  - le client paie Google Ads, donc chaque page de service est aussi une page d'atterrissage ;
  - faire appeler, faire venir au magasin ou obtenir une demande de devis.
- **Clientèle** : habitants et petites entreprises du quartier, pressés, pas techniciens, surtout sur mobile, avec une machine en panne. Ils ne lisent pas un site en entier. Ils veulent savoir en 5 secondes si on répare leur appareil, où, si c'est ouvert et comment appeler, puis être rassurés (avis, expérience).

# 2. Le site actuel (à conserver comme base)

**Architecture**
- Site statique généré par `build.py` (Python 3 + Jinja2) dans le dossier `public/`, mis en ligne chez OVH (Apache + PHP).
- Pas de framework, pas de CMS : garde cette architecture.
- `pip install -r requirements.txt`, puis `python build.py` : génère `public/` et affiche un rapport SEO (liens cassés, un seul H1 par page, longueur des titres et descriptions, attributs alt).
- `python build.py --serve` : aperçu sur http://localhost:8080.

**Fichiers**
- `src/data/site.json` : coordonnées, horaires, services (clé, nom, url, icône, illustration, accroche), marques, note Google, suivi Google Ads.
- `src/data/pages.json` : title, meta description, fil d'Ariane, type et langues de chaque page. C'est la source unique du SEO de chaque page.
- `src/templates/base.html` : head SEO, Open Graph, hreflang, JSON-LD injecté au build.
- `src/templates/macros.html` : composants `ui.icon`, `call_btn`, `quote_btn`, `directions_btn`, `rating`, `stars`, `breadcrumb`, `faq`, `service_card` / `service_grid`, `feature`, `feature_link`, `chips`, `hours_table`, `map_facade`, `process`, `cta_band`, `related`, `service_hero`.
- `src/templates/partials/` : barre d'annonce, header avec méga-menu, footer, barre d'appel mobile, bannière de consentement.
- `src/pages/*.html` : 17 pages (accueil, 7 pages de services, à propos, contact, guide imprimantes, 2 pages légales, merci, 404, NL, EN).
- `src/assets/css/style.css` : design system, jetons dans `:root`.
- `src/assets/js/main.js` : statut « Ouvert / Fermé » à l'heure de Bruxelles, menus, barre d'appel mobile, carte Google chargée au clic, formulaire AJAX avec préremplissage `?appareil=&sujet=`, consentement et suivi des conversions via les attributs `data-track`.
- `src/assets/img/` : sprite d'icônes `icons.svg` (via `ui.icon('nom')`), illustrations `ill-*.svg`, `logo.svg` et `logo-white.svg` (à remplacer), photo `vitrine-digital-buro-saint-gilles.webp` (900×334, seule vraie photo).
- `src/static/` : `.htaccess` (HTTPS + www, redirections 301 des anciennes URL, cache), `api/contact.php` (envoi du formulaire), favicons.

**Ce que fait `build.py` automatiquement**
- JSON-LD : LocalBusiness, Service, BreadcrumbList et FAQPage. Le FAQPage est lu dans le balisage `<details class="faq__item" data-faq><summary class="faq__q">…</summary><div class="faq__a">…</div></details>` : garde-le.
- sitemap.xml avec hreflang, robots.txt.
- Typographie française (espaces insécables).

**Charte actuelle** (inspirée de « Brex – white concrete, single ember »)
- Fond blanc et Fog `#f3f3f7`, texte Ink `#000` et Graphite `#60646c`.
- Un seul accent : Ember `#ff5900`. Les boutons principaux ont un texte **noir** pour le contraste AA.
- Police Inter auto-hébergée, interlettrage négatif.
- Rayons de 12 px (6 px pour les étiquettes), filets `#e2e3e9`, pas d'ombres.
- Barre d'annonce Carbon `#15191e` en haut, footer Abyss `#000710`.

**À conserver**
- Architecture, URL et SEO technique.
- Statut « Ouvert / Fermé » en direct, barre d'appel mobile, carte chargée au clic.
- Frise « De la machine à écrire au MacBook ».
- Illustrations SVG, pages NL et EN, suivi des conversions.

# 3. Ce qui ne va pas (retours sur la version actuelle)

1. Le site manque d'âme : trop fade, pas assez vivant.
2. Presque aucune interaction agréable. Exemple : survoler « Vente » dans le header ne fait rien, alors qu'un soulignement orange animé est attendu.
3. Le logo actuel est un simple texte générique. Il faut reprendre LEUR logo (joint) et le moderniser.
4. Il manque quelques vraies images. Les illustrations SVG sont bien, à garder, mais le site manque de vie.
5. Trop de texte et trop de petits détails inutiles : ce n'est ni assez pratique ni assez vendeur pour cette clientèle.
6. Les avis Google ne sont pas mis en scène. Il faut un bloc d'avis qui ressemble au widget Google.
7. La « barre de recherche » du hero est trompeuse : elle envoie vers la page contact. Elle doit être supprimée, ou rendue réellement utile.

# 4. Travail demandé

## 4.1 Logo modernisé et header

**Point de départ**
- Le logo actuel est joint (`1.png`) et visible sur https://www.digital-buro.be/images/1.png.
- Mot « DIGITAL-BURO » en capitales grasses, « DIGITAL » en rouge, « BURO » en bleu.
- Il est encadré d'une ellipse en deux arcs (rouge en haut, bleu en bas), avec des points de part et d'autre.
- C'est aussi l'enseigne du magasin : il doit rester reconnaissable.

**À faire**
- Redessine-le en SVG vectoriel propre, version 2026.
- Garde son ADN : mot bicolore, ellipse en deux arcs, rythme des points.
- Supprime ce qui date : effets, lettrage étiré, détails inutiles.
- Utilise une sans-serif géométrique grasse et moderne, aux proportions resserrées, lisible à 28 px de haut.
- Vectorise le texte : aucune dépendance de police.

**Couleurs**
- Version principale harmonisée avec le site :
  - Ember `#ff5900` pour « DIGITAL », l'arc supérieur et les points ;
  - un bleu nuit profond (autour de `#0B1F4D`, à ajuster) pour « BURO » et l'arc inférieur.
- Fournis aussi une variante « héritage » (rouge et bleu d'origine, modernisés), pour que le client compare.
- Fournis une version blanche pour le footer sombre.

**Déclinaisons**
- `logo.svg`, `logo-white.svg`, `logo-mark.svg` (symbole compact, par exemple l'ellipse avec « D-B »), `favicon.svg`.
- Régénère avec le nouveau logo : `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, et `og-image.jpg` (1200×630). Le script `tools/make_brand.py` peut être adapté.

**Header**
- Logo à 32–36 px de haut sur ordinateur, 28 px sur mobile.
- Mets à jour width et height dans `partials/header.html` et `partials/footer.html`.
- Le bleu nuit peut servir aux grandes surfaces sombres (voir 4.2), jamais de second accent de bouton.

## 4.2 Donner de l'âme

On doit sentir un vrai magasin de quartier, expérimenté, chaleureux et efficace, pas un gabarit de start-up.

**Hero de l'accueil**
- À droite, une composition vivante : une vraie photo (vitrine ou atelier) dans une carte arrondie.
- Des pastilles flottantes façon interface apparaissent en décalé : « ★ 4,7 · 448 avis Google », « ● Ouvert · jusqu'à 18h », « Toutes marques ».
- Un badge rond « 30 ans » tourne lentement, avec le texte circulaire « RÉPARATION TOUTES MARQUES • DEPUIS PLUS DE 30 ANS • ». C'est un clin d'œil modernisé à l'ancien badge « 30 ANS EXPÉRIENCE » de leurs visuels.

**Rythme de page**
- Alterne sections blanches et Fog.
- Tu peux utiliser UNE bande sombre (Abyss ou bleu nuit du logo) en milieu de page pour les chiffres clés : 30+ ans, 4,7★, 448 avis, toutes marques, avec compteurs animés. C'est un écart assumé à la charte.

**Accent orange**
- Utilise un peu plus l'Ember pour réchauffer : icônes clés sur fond Fog, soulignement d'un mot du H1 qui se dessine à l'apparition, pastille « Ouvert » qui pulse.
- Les boutons principaux restent la seule grosse masse orange par écran.

**Marques**
- Défilé infini des marques en texte monochrome, avec pause au survol : HP, Canon, Epson, Brother, OKI, Xerox, Ricoh, Kyocera, Lexmark, Samsung, Dell, Lenovo, Apple…

**Illustrations**
- Garde les illustrations `ill-*.svg` et anime-les légèrement via un `<style>` interne au SVG, en respectant `prefers-reduced-motion` :
  - la LED de l'imprimante clignote ;
  - la barre de progression du portable se remplit ;
  - les arcs Wi-Fi pulsent ;
  - une feuille sort de l'imprimante.

**Ton**
- Phrases courtes, directes et chaleureuses, en « vous ». Zéro jargon.
- Exemple : « Votre imprimante fait des siennes ? On s'en occupe. »

## 4.3 Micro-interactions et JavaScript (subtil, rapide, utile)

**Règles générales**
- Vanilla JS et CSS uniquement : pas de jQuery, pas de GSAP. Une micro-librairie de 5 Ko maximum, auto-hébergée, seulement si elle est vraiment nécessaire.
- Tout doit se désactiver proprement avec `prefers-reduced-motion: reduce`.
- Le contenu reste visible si le JS ne se charge pas : ajoute une classe `js` sur `<html>` et ne masque rien sans elle.

**Navigation et en-tête**
- Soulignement Ember de 2 px animé au survol et au focus de chaque lien (Vente, Entreprises…) : scaleX de 0 à 1 depuis la gauche, environ 200 ms.
- Le soulignement reste fixe sur la page courante.
- Le méga-menu « Réparations » s'ouvre en fondu avec un léger glissement ; ses icônes passent en Ember au survol.
- L'en-tête se compacte au défilement (72 → 60 px, avec filet et ombre très légère).
- Sur mobile, l'en-tête se cache quand on descend et réapparaît quand on remonte.

**Boutons et cartes**
- Boutons : la flèche glisse de 3 px au survol ; léger enfoncement au clic (scale 0,98) ; transitions de 150 ms.
- Cartes : légère élévation au survol (−4 px), bordure renforcée, illustration qui bouge un peu.

**Apparitions et compteurs**
- Fondu et montée de 12 px à l'apparition au défilement, en 500 ms, une seule fois (IntersectionObserver).
- Décalage de 60 ms entre les cartes d'une grille.
- Compteurs animés quand ils entrent à l'écran : 30+, 4,7 (avec virgule), 448.
- Frise « machine à écrire → Mac » : les icônes s'allument une par une et le point Ember glisse jusqu'à « Mac ».

**Détails pratiques**
- FAQ : animation de hauteur à l'ouverture et à la fermeture ; l'icône + pivote.
- Téléphone sur ordinateur (pas d'écran tactile) : un clic copie « 02 534 47 02 » et affiche « Numéro copié ». Le lien `tel:` reste actif sur mobile.
- Menu mobile : le panneau glisse, les liens apparaissent en cascade, la page ne défile plus derrière.
- Guide imprimantes : fine barre de progression de lecture en haut de page.
- Formulaire : bouton avec spinner pendant l'envoi, puis message de confirmation (succès) ou d'erreur.

## 4.4 Moins de texte, plus de vente

**Règles**
- Un bloc = une idée.
- Titre de carte : 5 mots maximum. Texte de carte : 15 mots maximum.
- Intro de section : 20 mots maximum, ou pas d'intro du tout.
- Aucun paragraphe de plus de 3 lignes sur mobile.
- FAQ : 3 à 4 questions par page maximum, réponses de 45 mots maximum. Garde le balisage FAQ, il génère le JSON-LD.
- Supprime les redites et les longues listes. Transforme les blocs explicatifs en pictos, puces, badges ou en une question de FAQ.
- Chaque écran propose une action : appeler, itinéraire ou devis.
- SEO : garde les mots-clés (réparation imprimante / PC / Mac / GSM, Saint-Gilles, Bruxelles, marques) dans le H1, les H2 et les cartes. Garde au moins environ 300 mots par page de service.

**Nouveau plan de l'accueil** (environ 450 à 600 mots visibles)
1. Hero :
   - H1 court avec les mots-clés (« Réparation d'imprimantes, PC & Mac à Saint-Gilles ») et un sous-titre de 15 mots maximum ;
   - boutons Appeler et Itinéraire, avec « Demander un devis » en lien secondaire ;
   - statut Ouvert / Fermé, note Google et visuel vivant (voir 4.2).
2. « Qu'est-ce qui est en panne ? » : sélecteur d'appareils (voir 4.6).
3. Bande sombre des chiffres clés, avec compteurs.
4. Services : 6 cartes courtes (illustration, titre, une ligne).
5. Avis Google façon widget (voir 4.5).
6. Pourquoi Digital-Buro : 4 points avec picto, une ligne chacun, plus la photo, le badge 30 ans et un lien « Notre histoire ».
7. Comment ça marche : 3 étapes d'une ligne (Vous passez → Diagnostic et devis → Réparé).
8. Défilé des marques.
9. Nous trouver : horaires avec statut en direct, adresse, tram 92, carte au clic, boutons.
10. FAQ de 4 questions, puis appel à l'action final.

**Pages de services** (environ 300 à 450 mots)
- Structure :
  - hero : H1, une ligne, boutons, note Google, photo ;
  - pannes courantes : grille de 6 à 8 pictos, 8 mots maximum chacun ;
  - 3 avis filtrés sur le sujet ;
  - marques ;
  - 3 étapes ;
  - 3 à 4 questions de FAQ ;
  - appel à l'action et services liés.
- À réduire :
  - « Réparer ou remplacer » devient une question de FAQ ;
  - « Une seconde vie plutôt qu'un nouveau PC » devient un badge ;
  - « Les bons réflexes » (page GSM) devient une question de FAQ ;
  - « Le bon conseil avant l'achat » devient 3 puces.
- À garder en version compacte : le bandeau « Windows 10 n'est plus supporté ? On passe votre PC à Windows 11 », qui est un bon argument de vente d'actualité.

**Autres pages**
- À propos : 3 courts paragraphes maximum, la frise, une photo, 3 valeurs.
- Contact : cartes de contact, formulaire court, horaires, carte.
- Guide imprimantes : c'est un article SEO, il peut rester long. Ajoute en tête un encadré « L'essentiel en 30 secondes », et un schéma animé des 6 étapes de l'impression laser.
- Pages NL et EN : même traitement.

## 4.5 Bloc « Avis Google » façon widget Google

Objectif : donner l'impression que Google lui-même s'est inséré dans le site.

**En-tête du bloc**
- Logo « G » officiel de Google en SVG multicolore, avec le libellé « Avis Google ».
- La note 4,7 en grand, avec 5 étoiles jaunes Google (`#FBBC04`), la dernière remplie à 70 %.
- « 448 avis ».
- Boutons « Voir tous les avis » (lien vers la fiche) et « Laisser un avis » (seulement si `google.review_url` est renseigné dans `site.json`).

**Cartes d'avis**
- Carrousel : flèches sur ordinateur, glissement au doigt sur mobile ; environ 1,2 carte visible sur mobile et 3 sur ordinateur.
- Contenu d'une carte :
  - avatar rond avec l'initiale, sur une couleur Google (`#1a73e8`, `#e8710a`, `#188038`, `#d93025`, `#9334e6`) ;
  - « Prénom N. » ;
  - date relative calculée en JS depuis une date ISO (`Intl.RelativeTimeFormat('fr')`, pour afficher « il y a 3 mois ») ;
  - étoiles ;
  - texte limité à 4 ou 5 lignes, avec un lien « Plus » ;
  - petit « G » en haut à droite ;
  - si elle est fournie, la « Réponse du propriétaire ».

**Style**
- Cartes blanches, bordure `#dadce0`, rayon de 8 px, ombre légère.
- Noms en `#202124`, informations secondaires en `#70757a`, texte de 14 à 15 px.
- Exception à la charte, limitée à ce bloc.

**Données**
- Un tableau `reviews` dans `src/data/site.json`, avec pour chaque avis : auteur, initiale, note, date ISO, texte, tags (par exemple `["pc"]`) et réponse du propriétaire (facultative).
- Rendu par une macro Jinja2 réutilisable :
  - version complète sur l'accueil ;
  - version compacte filtrée par tag sur chaque page de service ;
  - badge de note sur la page contact.

**Honnêteté**
- Uniquement des avis réels, recopiés mot pour mot (voir annexe B), avec prénom et initiale, et un lien vers la fiche Google.
- Aucun balisage Review ni AggregateRating : Google ignore les avis que l'entreprise publie sur elle-même, et peut les pénaliser.

**Option B, à préparer mais désactivée par défaut** : récupération automatique via Google Places API (New)
- Petit script PHP côté serveur ; la clé API n'est jamais exposée au navigateur.
- Cache JSON de 24 h, soit environ 30 appels par mois pour un coût négligeable.
- Champs : `rating`, `userRatingCount`, `reviews`. Attributions Google obligatoires.
- Si l'API échoue, les avis statiques s'affichent.

## 4.6 Remplacer la fausse barre de recherche

Supprime la barre du hero. Elle ne fait qu'envoyer vers le formulaire de contact.

**Remplacement : sélecteur « Qu'est-ce qui est en panne ? »**
- 6 grosses tuiles cliquables, avec picto ou mini-illustration : Imprimante / photocopieur, PC portable, PC fixe (vers la page ordinateur), Mac, GSM / tablette, Cartouche / toner.
- Ajoute « Entreprise » en lien discret.
- Chaque tuile mène à la bonne page de service.
- Sur mobile : grille 2 × 3, tuiles d'au moins 56 px de haut.
- Au survol : l'illustration s'anime et la tuile passe en Ember.

**Si tu tiens à garder une recherche**, elle doit fonctionner réellement :
- suggestions instantanées côté navigateur, sur un petit index JSON (services, pannes, marques, questions) ;
- navigation au clavier ;
- quand rien ne correspond : proposer « Appeler » et « Demander un devis ».
- Jamais de redirection aveugle vers le contact.

## 4.7 Images

**Où**
- Garde les illustrations SVG, et ajoute de vraies photos aux endroits clés :
  - hero de l'accueil ;
  - section « Pourquoi Digital-Buro » et page À propos ;
  - hero de chaque page de service (une photo par service) ;
  - « Nous trouver » (la vitrine) ;
  - page Entreprises (un bureau) ;
  - page Cartouches (un rayonnage de cartouches).

**Quelles photos**
- Priorité aux photos du client. Prévois des emplacements nommés dans `src/assets/img/photos/`, avec ratio et taille indiqués, pour qu'il puisse les remplacer.
- En attendant : photos libres de droits (Unsplash, Pexels), lumineuses, naturelles et chaleureuses, sans logos de concurrents. Liste les sources et les licences dans le README.
- Ne légende jamais une photo de banque d'images comme « notre équipe » ou « notre atelier ».
- Rédige des textes alternatifs descriptifs : ils comptent pour le SEO.
- La photo de vitrine actuelle (900×334) est en basse définition : ne l'affiche pas plus grande que sa taille réelle.

**Technique**
- Format WebP (et AVIF si possible), en deux tailles (environ 800 et 1600 px) avec `srcset` et `sizes`.
- Attributs `width` et `height` renseignés.
- `loading="lazy"` partout, sauf l'image du hero qui prend `fetchpriority="high"`.
- 150 Ko maximum par image, rayon de 12 px, cadrages cohérents (4:3 ou 16:10).

## 4.8 Conversion

- **Premier écran sur mobile**, sans défilement : H1, une ligne, « Ouvert jusqu'à 18h », boutons Appeler et Itinéraire, note Google.
- **Barre d'appel mobile** : garde-la (Appeler / Itinéraire). Ajoute un troisième bouton WhatsApp, seulement si un champ `whatsapp` est renseigné dans `site.json`. C'est à confirmer avec le client : un GSM, 0486 65 91 04, figure sur les Pages d'Or.
- **Mini-formulaire « Être rappelé »** (nom et téléphone) sur l'accueil et les pages de services.
- **Formulaire de contact raccourci** :
  - champs : nom, téléphone, e-mail, appareil (liste déroulante), message (facultatif) ;
  - téléphone ou e-mail, au moins l'un des deux obligatoire ;
  - mets `src/static/api/contact.php` à jour en conséquence : validation « téléphone OU e-mail », nouveaux champs, protections anti-spam conservées.
- **Composant « Prix indicatifs »** (par exemple « Diagnostic à partir de … ») : il ne s'affiche que si des prix sont renseignés dans `site.json`. Le client ne les a pas encore donnés : n'invente rien.
- **À ne pas écrire tant que le client ne l'a pas confirmé** : « devis gratuit », délais, garanties, « sans rendez-vous ».

# 5. Contraintes non négociables

1. **Architecture** : garde le générateur `build.py` (Python + Jinja2) et le HTML statique. Pas de React, Next, WordPress ni Tailwind par CDN.
2. **SEO** :
   - ne change pas les URL ;
   - garde `pages.json` comme source du SEO (tu peux en améliorer les textes) ;
   - un seul H1 par page ;
   - balisage FAQ inchangé, pour le JSON-LD automatique ;
   - conserve les attributs `data-track`, le hreflang, le sitemap et le `.htaccess` ;
   - `python build.py` doit se terminer par « ✓ Aucun lien cassé… ».
3. **Performance** :
   - Lighthouse mobile : au moins 90 en performance, 100 en SEO et 95 en accessibilité ;
   - 30 Ko de JavaScript minifié au maximum ;
   - aucun script tiers, sauf Google Ads après consentement ;
   - police Inter auto-hébergée conservée ;
   - CLS inférieur à 0,1.
4. **Accessibilité** : contraste AA (boutons Ember en texte noir), focus visibles, navigation au clavier (carrousel, menu, FAQ), respect de `prefers-reduced-motion`.
5. **Honnêteté** : n'invente ni prix, ni délais, ni garanties, ni certifications, ni chiffres, ni avis. Les informations manquantes vont dans des emplacements prévus de `site.json`, et dans une liste « À confirmer » du README.
6. **Charte** : garde la base (blanc et Fog, Inter à interlettrage négatif, Ember pour les actions, rayons de 12 px). Écarts autorisés pour donner de l'âme : couleurs du logo (bleu nuit), une bande sombre, couleurs Google dans le bloc d'avis, photos.

# 6. Livrables et méthode

1. **Plan d'abord** : présente en 10 à 15 lignes ta direction visuelle, le nouveau plan de l'accueil et la liste des fichiers modifiés. Enchaîne ensuite directement sur la réalisation.
2. **Fichiers complets** : livre chaque fichier modifié ou créé en entier, avec son chemin, sans aucun « reste inchangé ».
   - Si c'est trop long, découpe en plusieurs messages dans cet ordre : logo et favicons ; CSS et JS ; templates, macros, partials et `site.json` ; pages ; PHP et README.
   - Si tu peux exécuter du code, lance `python build.py` et renvoie plutôt un zip du projet complet.
3. **Pour terminer**, fournis :
   - la sortie de `python build.py` ;
   - un journal des changements ;
   - la liste des photos avec leur source et leur licence ;
   - la liste « À confirmer avec le client », mise à jour.

# Annexe A — Informations client (déjà dans `site.json`)

- Digital-Buro SRL, Chaussée de Charleroi 257, 1060 Saint-Gilles (Bruxelles), quartier Ma Campagne.
- Tram 92, arrêt Ma Campagne.
- Téléphone : 02 534 47 02 · Fax : 02 534 53 51 · E-mail : digital-buro@skynet.be · TVA : BE 0874.004.642.
- Horaires : du lundi au vendredi de 10h30 à 18h, le samedi de 11h à 17h, fermé le dimanche.
- Google : 4,7/5 sur 448 avis, catégorie « Magasin informatique ».
- Mots qui reviennent le plus dans les avis : vendeur, cartouches, technicien, honnête. Le propriétaire répond aux avis.
- Plus de 30 ans d'expérience du dirigeant.
- Slogan historique : « Votre meilleur partenaire bureautique & digital ».

# Annexe B — Avis Google à intégrer (texte exact copié depuis la fiche)

Fiche Google : https://www.google.com/maps?cid=4568478121866388337

1. Nathan M. — note : [À COMPLÉTER] — vers juin 2026 — réparation d'ordinateur, professionnalisme, PC redevenu fluide.
   Texte : [À COLLER]
2. Corine S. — note : [À COMPLÉTER] — vers juillet 2026 — accueil, bon conseil, qualité des produits.
   Texte : [À COLLER]
3. Michael M. — note : [À COMPLÉTER] — vers mars 2026 — service impeccable du début à la fin.
   Texte : [À COLLER]
4. Un avis qui parle d'imprimante ou de cartouches — [À COLLER]
5. Un avis d'une entreprise ou d'un professionnel — [À COLLER]
6. Un autre avis 5★ récent — [À COLLER]

Si la réponse du propriétaire est copiée, affiche-la sous l'avis.

# Annexe C — Liens utiles

- Site actuel : https://www.digital-buro.be
- Ancien logo (joint) : https://www.digital-buro.be/images/1.png
- Fiche Google Maps : https://www.google.com/maps?cid=4568478121866388337
