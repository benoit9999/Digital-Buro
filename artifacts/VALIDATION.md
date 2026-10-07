# Envoi PHP de la version HTML — validation du 7 octobre 2026

- Dix formulaires de `site-html/` raccordés à `send_contact.php`, avec e-mail HTML vers le destinataire fixe `digital-buro@skynet.be`. Le fichier fourni de l’autre client a été lu comme référence et n’a pas été modifié. La version principale `public/` est inchangée par ce raccordement.
- PHP 8.5.11 : syntaxe des deux fichiers PHP et du JavaScript validée. Transport réel `mail()` vers un SMTP de capture isolé sur localhost ; dix messages acceptés localement, aucun envoi externe. Destinataire fixe, Reply-To facultatif, caractères UTF-8, longs sujets MIME et échappement du HTML vérifiés.
- 33 scénarios consignés dans [html-form-tests.json](html-form-tests.json) : absence/expiration/réutilisation du jeton, délai serveur, piège anti-robots, mauvais champs, tableaux à la place de chaînes, injection d’en-têtes, volume et liens, origine étrangère, quotas IP/téléphone/global, doublons entre compartiments IP, verrou partagé et stockage indisponible.
- 32 parcours de mise en page sur les 16 pages à 390 et 1440 px. Préremplissage, validations client, contact, rappels FR/NL/EN et service Cartouches exercés dans Chrome via le vrai PHP. Formulaire sans JavaScript et redirection vers `merci.html` vérifiés. [html-form-browser-tests.json](html-form-browser-tests.json).
- Raccordement testé à la racine et sous `/site-html/` avec cookie de session correctement limité au chemin. Panne réelle du SMTP : HTTP 503, aucune confirmation de réussite, données du formulaire conservées et bouton réactivé.
- Plafonds par défaut : 5 tentatives/IP/h, 3 par téléphone/h, 30 globales/h et 100 sur 24 h glissantes ; intervalle IP de 30 s, jeton valable une heure, délai de remplissage de 2 s et doublons bloqués 10 min. Compteurs salés et horaires hors du dossier public, sous verrou ; aucun message stocké en clair dans ce registre.
- Les sources du raccordement sont maintenues dans `tools/site-html/` et reprises par `tools/sync_site_html.py`. Notice de confidentialité et documentation de la copie HTML actualisées.
- La réception réelle dans Skynet et l’autorisation de l’expéditeur par l’hébergement restent à vérifier après installation sur le serveur du client. Les tests locaux prouvent l’acceptation par le transport de capture, pas la délivrabilité en production.

---

# Synchronisation HTML — validation du 6 octobre 2026

- Les 16 pages de `site-html/` ont été reconstruites depuis la version actuelle de `public/`, après un build validé. Les dernières corrections et les crédits sont présents ; liens, ancres, métadonnées, sitemap et manifeste utilisent les noms des fichiers HTML.
- 64 parcours Chrome à 320, 390, 768 et 1440 px : aucun débordement horizontal, texte tronqué, image cassée, erreur JavaScript ou réponse HTTP locale en erreur. Les 64 comparaisons avec la version principale confirment l’identité des textes visibles, des positions, dimensions et styles examinés.
- 49 médias/notices de licence et `refresh.js` identiques octet par octet. Empreintes de `public/` inchangées après la copie ; anciens fichiers cartouches et illustration réseau supprimés de `site-html/`.
- Douze paires de captures complètes : onze identiques pixel par pixel. Le viewport mobile de Contact est identique ; seule sa capture complète présente un faible écart sur une ligne de texte partiellement masquée par la barre fixe, sans différence de contenu ou de géométrie. Détails dans [site-html-checks.json](site-html-checks.json).
- Navigation, menu et rotation, FAQ, carrousel, tableaux, préremplissage et validation des formulaires vérifiés. Aucun POST ni appel API ; l’envoi sera traité ultérieurement selon la demande du client. Ouverture à la racine, en sous-dossier, en `file://` et sans JavaScript contrôlée. Police Inter et icônes chargées en ouverture directe, sans erreur de console.
- Sauvegarde ZIP de l’ancienne copie et inventaire des fichiers : [site-html-sync-files.json](site-html-sync-files.json). Captures actualisées `site-html-*`.

---

# Crédits photos — validation du 6 octobre 2026

- Builds PHP et GitHub Pages : les 16 pages conservent des liens et ressources valides ; les crédits sont liés dans le pied de page des trois langues.
- 12 parcours Chrome : accueil FR/NL/EN et mentions légales examinés à 320, 390 et 1440 px. Huit miniatures chargées, sept liens externes de source/licence, aucun débordement horizontal, image cassée, erreur JavaScript ni réponse HTTP locale en erreur. Navigation depuis le lien NL vers l’ancre des crédits vérifiée.
- Notices MIT/ISC Feather/Lucide et OFL Inter accessibles en HTTP 200. Ancienne clause d’appropriation globale des contenus remplacée, sans prétendre qu’un crédit accorde des droits d’utilisation.
- Sources individuelles PC/Mac et licences vérifiées ; droits du magasin/cartouches déclarés par le client. La vérification **ne valide pas** la publication commerciale des photos HP/Brother/Epson et ne remplace pas une autorisation.
- Captures examinées : `photo-credits-1440.png`, `photo-credits-320.png` et `photo-credits-footer-1440.png`. Rapport des contrôles : [photo-credits-checks.json](photo-credits-checks.json). Bilan des droits : [IMAGE-RIGHTS.md](IMAGE-RIGHTS.md).

---

# Corrections complémentaires du client — validation du 6 octobre 2026

- Builds PHP et GitHub Pages (`/Digital-Buro`) réussis : 16 pages, aucun lien cassé, un H1 par page, titres et descriptions uniques.
- 36 parcours Chrome : les 16 pages à 320 et 1440 px, puis les accueils FR/NL/EN et la page Cartouches à 390 px. Aucun débordement horizontal, image cassée, erreur JavaScript ou réponse HTTP locale en erreur. Menu mobile ouvert puis fermé avec Échap.
- Titres d’accueil associant vente et réparation ; quartier Ma Campagne dans les trois langues. Absence des anciennes mentions de l’arrêt, des prestations réseau/Wi-Fi, de l’ancienne photo des cartouches et de l’ancienne façade dans le HTML examiné, y compris les FAQ et métadonnées.
- Même photo du stock de cartouches dans la carte de services et la page détaillée, sans recadrage ni illustration superposée. Format 4:3 vérifié ; limite de hauteur mobile retirée pour conserver ce format.
- Nouvelle photo extérieure identique à celle du haut de l’accueil près des horaires, dans Contact et À propos. Image de partage actualisée.
- Rapport : [client-corrections-checks.json](client-corrections-checks.json). Captures examinées : `client-corrections-hero-1440.png`, `client-corrections-hero-390.png`, `client-corrections-access-1440.png`, `client-corrections-cartouches-1440.png`, `client-corrections-cartouches-390.png`, ainsi que l’image de partage.

---

# Modifications du client — validation du 6 octobre 2026

- Carte « Cartouches & toners » : photo du client chargée à 320, 390, 768 et 1440 px, tous les produits visibles grâce à `object-fit: contain`, aucun débordement horizontal et lien vers la page Cartouches fonctionnel. Trois WebP de 400/800/1200 px sous 150 Ko. Captures examinées : `cartouches-client-390.png` et `cartouches-client-1440.png` ; rapport : [cartouches-client-checks.json](cartouches-client-checks.json).
- Builds PHP et GitHub Pages (`/Digital-Buro`) : 16 pages, aucun lien cassé, un H1 par page, titres et descriptions uniques.
- 42 contrôles ponctuels dans Chrome : les accueils FR/NL/EN examinés à 320, 375, 390, 640, 768, 1100 et 1440 px, ainsi que les 16 pages sur mobile. Aucun débordement horizontal, image cassée, erreur JavaScript ou réponse HTTP locale en erreur.
- Localisation dans un encadré orange sous le titre, texte de 18 à 23 px : arrêt Ma Campagne et proximité de l’avenue Louise. « +35 » dans le badge et le compteur ; « +450 » dans les badges Google, le compteur d’avis et le résumé des trois langues. Aucune ancienne mention de 30 ans d’expérience, 440 ou 448 avis dans les pages examinées. Navigation mobile et affichage sans JavaScript vérifiés.
- Logo fourni présent dans l’en-tête et le pied de page des 16 pages, avec URL versionnée ; fichier PNG de 350 × 110 px identique à l’original fourni. Données structurées et image de partage actualisées.
- Les deux photos du magasin conservent leur format 4:3. Six variantes de 400/800/1200 px, de 33 200 à 144 768 octets ; attributs de taille, srcset et textes alternatifs présents.
- Captures examinées : `client-home-desktop.png`, `client-home-mobile.png`, `client-hero-desktop.png`, `client-hero-mobile.png` et l’image de partage `src/assets/img/og-image.jpg`. Captures complémentaires : `client-footer-desktop.png`, `client-reviews-desktop.png`. Rapport : [client-updates-checks.json](client-updates-checks.json).
- `tools/check_pages.cjs` passe : les 16 pages de l’aperçu préfixé, les liens, les images responsives, les polices, la navigation et le contact par e-mail restent valides. Les captures `pages-1440.png` et `pages-390.png` sont actualisées.

---

# Photos complémentaires et mobile — validation du 4 octobre 2026

- 16 pages examinées dans Chrome sur dix formats : 320 × 740, 360 × 800, 375 × 812, 390 × 844, 430 × 932, 640 × 900, 768 × 1024, 844 × 390, 1024 × 900 et 1440 × 1000. Les 160 parcours passent : aucun débordement horizontal de la page, titre ou bouton tronqué, image en erreur, erreur JavaScript ou réponse HTTP locale en erreur.
- Six cartes photographiques sur l’accueil. Une colonne sous 640 px, deux de 640 à 1023 px, trois à partir de 1024 px. Les appareils restent entiers ; les photos éditoriales remplissent leur cadre. Photo réelle du magasin visible dans Contact et champs mobiles de 16 px minimum.
- Menu testé sur les neuf formats inférieurs à 1100 px : arrière-plan rendu inactif, barre d’appel masquée, accès aux dernières actions par défilement et fermeture avec Échap. Position vérifiée après passage du portrait au paysage ; fermeture automatique et restauration du contenu lors du passage au grand écran.
- FAQ, carrousel et défilement au clavier des tableaux du guide vérifiés. Le cadre du tableau défile, tandis que la page reste à la largeur de l’écran.
- `tools/check_refresh.cjs` passe aussi avec les animations habituelles : navigation, FAQ, carrousel, formulaires simulés, réduction des animations et navigation sans JavaScript. Aucun message externe envoyé.
- Builds PHP et GitHub Pages avec `/Digital-Buro` : 16 pages, liens et srcset valides ; `tools/check_pages.cjs` passe sur la version préfixée.
- Rapport détaillé : [mobile-responsive-checks.json](mobile-responsive-checks.json). Captures examinées : `mobile-home-*`, `mobile-services-*`, `mobile-contact-*`, `mobile-guide-*` et `mobile-menu-landscape.png`. Contrôles locaux de mise en page ; aucune nouvelle mesure Lighthouse et aucun test sur un téléphone physique.

---

# Photos d’imprimantes — validation du 4 octobre 2026

- Build de l’hébergement PHP : 16 pages, aucun lien cassé, un H1 par page, titres et descriptions uniques.
- Build GitHub Pages avec le préfixe `/Digital-Buro` et contrôle existant `tools/check_pages.cjs` : 16 pages, liens, assets, srcset, navigation et affichage mobile/ordinateur validés.
- 10 pages vérifiées à 390, 768 et 1440 px, soit 30 parcours : toutes les images décodées, aucun débordement horizontal, aucune erreur JavaScript ou réponse HTTP locale en erreur.
- Trois photos dans les cartes de services de l’accueil et une photo légendée sur chacune des pages Imprimantes, Vente et Entreprises. Les produits restent entiers (`object-fit: contain`).
- Huit variantes WebP de 3 070 à 19 146 octets, identiques dans `src/` et `public/`. Sources officielles, textes alternatifs et droits documentés dans `site.photos` et le README.
- Captures examinées : accueil, cartes de services, Imprimantes, Vente et Entreprises sur mobile et ordinateur. Rapport : [printer-photo-checks.json](printer-photo-checks.json) ; captures `printers-*.png`.

---

# Validation locale — 29 septembre 2026

## Build

16 pages générées après retrait de l’offre GSM non confirmée. Résultat :

> ✓ Aucun lien cassé, un seul H1 par page, titres et descriptions uniques.

La sortie complète figure dans [build-report.txt](build-report.txt). Les URL des prestations confirmées et leurs métadonnées restent définies dans `src/data/pages.json`. Le fichier de redirections Apache existant est conservé.

## Lighthouse mobile — mesures de la refonte avant cette dernière passe

| Page | Performance | Accessibilité | SEO | CLS |
|---|---:|---:|---:|---:|
| Accueil | 94 | 100 | 100 | 0 |
| Réparation imprimante | 95 | 100 | 100 | 0 |
| Contact | 91 | 100 | 100 | 0,028 |

Mesures Lighthouse 13.5.0 avec son profil mobile et sa simulation de ralentissement par défaut, Chrome local, sur http://127.0.0.1:8081. Le serveur de contrôle `tools/preview_gzip.py` reproduit la compression gzip et un cache statique, déjà prévus dans `public/.htaccess`. Il ne reproduit pas PHP, les redirections Apache ni la latence réelle d’OVH.

Le serveur Python simple de prévisualisation, sans compression, a donné des scores plus faibles et variables (notamment 83 à 89 sur les dernières mesures de l’accueil). Les scores ci-dessus ne garantissent pas ceux de la production et devront être remesurés après mise en ligne.

Rapports bruts : `lighthouse-home.json`, `lighthouse-service.json`, `lighthouse-contact.json`.

## Interfaces et accessibilité

Le contrôle navigateur `tools/check_refresh.cjs` couvre les largeurs 375, 390, 768, 1100 et 1440 px sur l’accueil, le contact, deux services et les pages NL/EN : débordement horizontal, H1, images chargées, erreurs JavaScript. Il contrôle aussi le menu et Échap, l’ouverture/fermeture des FAQ, le carrousel, les succès et erreurs des formulaires, la préférence de réduction des animations et la navigation sans JavaScript.

Les réponses du formulaire sont simulées : aucun message réel n’est envoyé. Cela vérifie les interactions du navigateur, pas la délivrabilité des e-mails.

Un contrôle axe-core WCAG A/AA est enregistré dans `accessibility.json` pour accueil, contact, imprimante, NL, EN et À propos. La réduction des animations est activée pour éviter de mesurer le contraste au milieu d’un fondu. Un résultat automatisé ne remplace pas un audit d’accessibilité complet.

Captures : `home-desktop.png`, `home-mobile.png`, `service-desktop.png`, `service-mobile.png`, `reviews-mobile.png`. Les animations sont figées pour les captures.

## Poids et syntaxe

- JavaScript total livré : 23 548 octets, avant compression ; inférieur au plafond de 30 Ko même sans minification.
- Douze variantes photographiques : 587 530 octets au total ; plus lourde : 128 548 octets, sous 150 Ko.
- Syntaxe des deux fichiers JavaScript vérifiée avec Node.
- Syntaxe de `contact.php` et `reviews.php` analysée avec php-parser en mode PHP 7.4. Aucun runtime PHP n’étant installé, leur exécution serveur n’a pas été testée.
- Les dépendances de contrôle restent locales et ne sont pas chargées par le site.

## Reproduire

```sh
python build.py
python tools/preview_gzip.py
```

Dans un autre terminal, installer Playwright, Lighthouse, @axe-core/playwright et php-parser pour les outils de contrôle. Les scripts utilisent Chrome Windows et `CODEX_NODE_MODULES` comme chemin des modules Playwright ; Lighthouse et axe-core se trouvent dans `tools/qa-deps/node_modules`.

Pour Lighthouse, définir `LH_BASE=http://127.0.0.1:8081`, puis exécuter `node tools/lighthouse_refresh.cjs`. Les contrôles fonctionnels et axe utilisent l’aperçu standard du site sur le port 8080. Les dépendances volumineuses et caches sont exclus de l’archive.

## Avant publication

Tester sur l’hébergement : formulaires contact/rappel avec réception effective, erreurs de validation PHP, adresse d’expédition autorisée, HTTPS/www et anciennes URL. Confirmer les données commerciales et les photos avec le client. Le flux Places est une option préparée côté serveur, pas une récupération automatique actuellement active.


## Contrôles de finalisation

Le build final génère 16 pages sans lien cassé. Les contrôles navigateur ont été relancés après les modifications : aucun débordement sur les cinq largeurs testées, menus, FAQ, carrousel d’accueil et formulaires simulés fonctionnels. Le contrôle axe-core ne remonte aucune violation sur les six pages examinées.

`content-checks.json` confirme que les avis sont présents uniquement sur les accueils FR/NL/EN, que l’offre GSM est absente du HTML, du catalogue structuré et du sitemap, et que les formules signalées sont retirées. Le favicon régénéré a été contrôlé visuellement. Les captures correspondent à cette dernière version.

Les scores Lighthouse conservés ci-dessus sont ceux de la précédente refonte, pas une nouvelle mesure de cette passe éditoriale. Les limites de validation PHP et de messagerie restent inchangées.

## Formulaires — validation PHP réelle

La limitation concernant l’absence de runtime PHP ci-dessus est levée pour les tests locaux : PHP 8.4.26 portable, téléchargé depuis la distribution officielle avec vérification SHA-256, a exécuté le traitement. Aucun binaire PHP n’est inclus dans Git ou le site.

`contact-tests.json` consigne les scénarios : nom avec chiffres ou balises, numéros incorrects, e-mail invalide/injection, champ piège, trop de liens, origine étrangère, jeton absent/réutilisé, délai minimal, intervalle et quota horaire, contact, rappel, formulaire sans JS et panne du transport. Le test navigateur contrôle aussi le refus des mauvaises saisies puis envoie via le vrai PHP vers le serveur SMTP de capture local. Aucun e-mail de test n’a quitté la machine. La réception effective chez le client et le transport OVH restent à valider après publication.
