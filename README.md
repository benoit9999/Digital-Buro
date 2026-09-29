# Digital-Buro — refonte du site vitrine

Version du 29 septembre 2026. Site statique généré avec Python/Jinja2, compatible avec l’hébergement Apache/PHP existant. Le site comprend 16 pages. La page GSM/tablettes ajoutée pendant la maquette a été retirée faute de confirmation sur le site d’origine ; les URL des prestations confirmées sont conservées. Rien n’a été publié sur le site de production.

## Générer et prévisualiser

```sh
pip install -r requirements.txt
python build.py
python build.py --serve
```

Aperçu : http://localhost:8080. Le serveur Python montre le site mais **n’exécute pas PHP**. Le dossier `public/` est généré ; modifier les sources, puis reconstruire.

| Emplacement | Contenu |
|---|---|
| `src/data/site.json` | Coordonnées, horaires, services, contenus courts, photos, avis, options |
| `src/data/pages.json` | Titres SEO, descriptions, URL, langues et fil d’Ariane |
| `src/pages/` | Accueil, contact, histoire, guide, pages légales et entrées des services |
| `src/templates/service-compact.html` | Structure commune des six pages de service |
| `src/templates/partials/fresh-macros.html` | Avis, photos, rappel, frise, marques, badge |
| `src/assets/css/style.css`, `refresh.css` | Base et nouvelle direction visuelle ; fusionnées au build |
| `src/assets/js/main.js`, `refresh.js` | Navigation, formulaires, interactions sans bibliothèque |
| `src/static/api/` | Traitement PHP des demandes et adaptateur Places facultatif |
| `artifacts/` | Captures, rapport du build et résultats des contrôles |

Les anciennes URL et redirections, les données structurées LocalBusiness/Service/FAQPage/BreadcrumbList, le sitemap, les liens de langues et les attributs de suivi sont conservés. Aucun balisage Review ou AggregateRating n’a été ajouté.

## Identité et interactions

Le logo reprend les arcs, les points et le mot bicolore de l’enseigne jointe. Le lettrage est vectorisé : pas de police à charger pour l’afficher. Variantes dans `src/assets/img/` : `logo.svg` orange/bleu nuit, `logo-heritage.svg` rouge/bleu, `logo-white.svg` et `logo-mark.svg`. Les favicons et l’image de partage sont déjà générés.

Pour régénérer les assets de marque, installer aussi Pillow et fonttools, puis exécuter `python tools/make_brand.py` et `node tools/raster_brand.cjs` (nécessite le module Node sharp, ou CODEX_NODE_MODULES pointant vers son dossier parent). Reconstruire ensuite le site. La police source est fournie dans `tools/fonts/`.

Les effets comprennent soulignements, boutons, menus, FAQ animées, apparitions, compteurs, frise, illustrations et défilé des marques. Le bouton de pause du défilé arrête aussi le badge tournant. La préférence système de réduction des animations est respectée. Sans JavaScript, contenus, liens, FAQ, navigation de secours et formulaires HTML restent accessibles.

## Photos et licences

La vitrine existante reste la seule photo identifiée comme celle du magasin. Les photos de banque d’images illustrent les prestations ; elles ne sont pas présentées comme l’équipe ou l’atelier de Digital-Buro.

| Fichiers dans `src/assets/img/photos/` | Photographe et source | Licence |
|---|---|---|
| imprimante-800/1600.webp | [engin akyurt](https://unsplash.com/photos/CGnoRQZGWmw) | [Unsplash](https://unsplash.com/license) |
| entreprises-800/1600.webp | [Meatball Overexposure](https://unsplash.com/photos/8r1ZlqqGxMU) | [Unsplash](https://unsplash.com/license) |
| mac-800/1600.webp | [Aleksi Tappura](https://unsplash.com/photos/mCg0ZgD7BgU) | [Unsplash](https://unsplash.com/license) |
| ordinateur-800/1600.webp | [IT services EU](https://www.pexels.com/photo/7639373/) | [Pexels](https://www.pexels.com/license/) |
| gsm-800/1600.webp | [Tima Miroshnichenko](https://www.pexels.com/photo/6754839/) | [Pexels](https://www.pexels.com/license/) |
| cartouches-800/1600.webp | [Jakub Zerdzicki](https://www.pexels.com/photo/17536002/) | [Pexels](https://www.pexels.com/license/) |

La page Vente réutilise la photo imprimante. La photo Cartouches montre des cartouches installées, en attendant une vraie photo du rayonnage. La vitrine (900 × 334) n’est pas agrandie au-delà de sa taille native.

Pour remplacer une image, conserver ses deux noms et exporter en WebP, 800 × 500 et 1600 × 1000, chacun sous 150 Ko. Actualiser le texte alternatif, l’auteur et la source dans `site.photos`. Les attributs de taille, srcset et chargement différé sont déjà prévus ; les photos de premier écran sont prioritaires.

## Avis Google

Trois **extraits** attribués à Nathan M., Corine S. et Michael M. sont intégrés, avec un lien vers [la fiche Google](https://www.google.com/maps?cid=4568478121866388337). Les extraits sont identifiés comme tels. Aucun témoignage supplémentaire ni réponse du propriétaire n’est inventé.

La note 4,7/5 et le total 448 correspondent au relevé du 28 septembre 2026, pas à une mise à jour en direct. Modifier `site.google` pour les actualiser. Les dates exactes n’étant pas connues, `date` reste null et `date_label` indique un mois approximatif. Une date ISO confirmée active l’affichage relatif. Ne pas transformer un mois approximatif en jour inventé.

Les avis sont affichés uniquement sur les pages d’accueil FR/NL/EN. Aucun bloc d’avis ni badge de note ne surcharge les pages de service, le contact ou la présentation du magasin.

Le bloc est une sélection éditoriale du magasin avec attribution Google Maps, pas un widget officiel ni une certification Google.

### Option Places API, désactivée

`api/reviews.php` prépare l’accès serveur à Places API (New), avec clé en variable d’environnement, délai d’attente et repli vers la sélection statique. Sans configuration, il retourne une indisponibilité et n’appelle pas Google. Le site utilise actuellement les avis statiques ; le raccordement de ce flux au composant reste à activer et tester avec le compte du client.

Variables serveur : `DB_PLACES_ENABLED=1`, `DB_PLACES_API_KEY`, `DB_PLACES_ID`. La clé ne doit jamais figurer dans le JSON du site ni dans JavaScript. Restreindre la clé au service nécessaire.

Écart au brief : pas de cache de 24 h des avis. Les [règles Places](https://developers.google.com/maps/documentation/places/web-service/policies) limitent le stockage du contenu ; l’adaptateur ne conserve que l’horodatage de sa limitation de fréquence. Il ne garantit donc ni 30 appels par mois ni un coût négligeable. Vérifier les conditions, quotas et tarifs avant activation.

## Formulaires, prix et WhatsApp

Le contact accepte le nom et au moins un téléphone ou un e-mail. Message facultatif. Le rappel nécessite nom et téléphone. Spinner, confirmation, erreur et réactivation du bouton sont prévus ; le serveur conserve ses protections anti-spam.

Le destinataire reste `digital-buro@skynet.be`, l’expéditeur `site@digital-buro.be`. L’hébergement doit autoriser cet expéditeur. Aucun e-mail réel n’a été envoyé pendant les tests. Un petit fichier temporaire de limitation par IP est utilisé ; les demandes ne sont pas enregistrées dans une base de données.

- `site.whatsapp` : laisser vide jusqu’à confirmation du numéro et de son usage WhatsApp ; renseigner ensuite une URL https://wa.me/… validée.
- `site.prices` : objet vide par défaut. Ajouter un texte validé sous la clé du service (par exemple `imprimante`) pour afficher un tarif indicatif. Aucun montant n’est inventé.
- `google.review_url` : lien officiel « laisser un avis », à renseigner depuis la fiche du client.

## Mise en ligne

1. Sauvegarder le site et la configuration actuels, préparer un emplacement de préproduction.
2. Y envoyer le contenu de `public/`, y compris `.htaccess`.
3. Vérifier PHP, l’envoi des e-mails, l’expéditeur, les deux types de formulaire et les erreurs.
4. Vérifier HTTPS/www, anciennes URL, redirections 301, pages FR/NL/EN et sitemap.
5. Publier après validation, conserver une sauvegarde permettant le retour arrière.

Les contrôles locaux ne valident pas le fonctionnement de PHP, du courrier ou des règles Apache sur OVH.

## Référencement et Google Ads

Les annonces payantes et le référencement naturel sont distincts. Aucun site ne peut garantir une première place Google. L’architecture conserve des pages dédiées aux services, des contenus locaux lisibles et le maillage interne. Après publication, contrôler les redirections, l’indexation dans Search Console et la cohérence des coordonnées avec la fiche Google.

Les destinations des annonces peuvent pointer directement vers le service concerné. Les conversions restent configurables dans `tracking`. Le suivi publicitaire n’est chargé qu’avec une configuration et le consentement prévu par le site. Aucune baisse du coût par clic n’est promise.

## À confirmer avec le client

- Prix de diagnostic, délais, garanties et conditions de dépôt.
- GSM/tablettes : non proposés dans cette version. Réintroduire uniquement après confirmation explicite du client, avec des informations vérifiables.
- Année de début du dirigeant : conservation prudente de « plus de 30 ans », sans inventer « depuis 1987 ».
- Photos actuelles du magasin, du rayonnage et de l’atelier ; autorisation d’utiliser les personnes éventuellement photographiées.
- Textes exacts, notes et dates des avis manquants ; actualisation des chiffres Google.
- Numéro WhatsApp, lien pour laisser un avis et éventuelle nouvelle boutique en ligne.
- Accueil possible en néerlandais et anglais.
- Adresse d’expédition des formulaires et configuration de messagerie de l’hébergeur.
- Horaires exceptionnels et jours fériés : l’indicateur suit uniquement la semaine habituelle.
- Choix final entre le logo orange/bleu nuit et la variante héritage.

Consulter `CHANGELOG.md` et `artifacts/VALIDATION.md` pour les modifications, résultats et limites des tests.


## Dernière passe de finalisation

Les titres ont été simplifiés, les avis concentrés sur l’accueil et les accès au magasin renforcés. Les pages Vente et Cartouches disposent de leurs propres étapes. De fins séparateurs bleu nuit/orange structurent les sections ; le monogramme du favicon est centré sur les contours des lettres. La vérification des prestations est documentée dans `artifacts/source-audit/VERIFICATION.md`.
