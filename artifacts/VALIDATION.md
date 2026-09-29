# Validation locale — 29 septembre 2026

## Build

17 pages générées. Résultat :

> ✓ Aucun lien cassé, un seul H1 par page, titres et descriptions uniques.

La sortie complète figure dans [build-report.txt](build-report.txt). Les URL et métadonnées restent définies dans `src/data/pages.json`. Le fichier de redirections Apache existant est conservé.

## Lighthouse mobile

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

