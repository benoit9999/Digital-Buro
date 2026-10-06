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
