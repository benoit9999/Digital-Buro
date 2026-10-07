# Envoi PHP et anti-spam de la copie HTML — 7 octobre 2026

- Script fourni `send_reservation.php` adapté au contact et aux rappels de Digital-Buro : e-mail HTML via `mail()`, destinataire fixe `digital-buro@skynet.be`, expéditeur Digital-Buro et Reply-To facultatif validé.
- Dix formulaires HTML raccordés à `send_contact.php`, dont les accueils FR/NL/EN et les pages de services. Champs, préremplissage, validations locales et présentation conservés ; formulaire PHP disponible sans JavaScript.
- Anti-spam serveur : champ piège, jeton de session à usage unique, délai minimal, contrôles de formats et d’injection, quotas par IP/téléphone, blocage des doublons et plafond global de 30 tentatives/h et 100/24 h.
- Registre de compteurs avec verrou et empreintes salées, hors du dossier public ; échec de stockage ou du transport traité sans confirmation d’envoi.
- `tools/sync_site_html.py` conserve désormais le raccordement PHP lors des synchronisations. Notices d’exploitation et de confidentialité adaptées au fonctionnement de cette version.
- Tests du transport réel vers un SMTP de capture local, des refus anti-spam et des parcours navigateur ; aucun envoi externe. Le script de l’autre client n’est pas modifié.

---

# Synchronisation de la copie HTML — 6 octobre 2026

- Les 16 pages de `site-html/` reprennent la version principale actuelle : textes, titres, logo du client, chiffres, photos du magasin, cartouches multimarques, crédits et derniers ajustements visuels.
- Prestations réseau et Wi-Fi, ancienne photo de cartouches et anciens fichiers supprimés de la copie ; notices Feather/Lucide ajoutées.
- Liens relatifs, ancres des crédits, variantes WebP, métadonnées, sitemap et manifeste adaptés aux noms des pages HTML. Une seule feuille CSS éditable et deux scripts JavaScript.
- Envoi des formulaires conservé pour une étape ultérieure, selon la demande du client ; champs, préremplissage et validation locale repris.
- Synchronisation reproductible via `tools/sync_site_html.py`, avec sauvegarde ZIP de la copie précédente et inventaire des empreintes des fichiers.

---

# Crédits et vérification des droits d’image — 6 octobre 2026

- Lien « Crédits photos » dans le pied de page FR/NL/EN ; rubrique dédiée des mentions légales avec les huit miniatures, images utilisées, auteurs, sources et licences lorsqu’elles sont vérifiées.
- Propriété des photos du magasin et des cartouches déclarée par le client ; pages individuelles et licences commerciales des photos PC/Mac vérifiées sur Pexels et Unsplash.
- Autorisations des visuels HP, Brother et Epson signalées comme non établies, avec sources et conditions dans `artifacts/IMAGE-RIGHTS.md`. Les liens de source ne sont pas présentés comme des autorisations ; accord ou remplacement nécessaire avant publication.
- Clause attribuant globalement tous les contenus à Digital-Buro remplacée par une mention respectant les droits des tiers. Notices de licence Feather/Lucide distribuées avec les assets, et licence Inter liée.
- Inventaire daté avec empreintes des variantes dans `artifacts/image-rights-inventory.json` ; affichage, liens, licences et navigation des crédits vérifiés sur mobile et ordinateur.

---

# Corrections complémentaires du client — 6 octobre 2026

- « Quartier Ma Campagne » remplace les mentions de l’arrêt dans les pages, les traductions, les métadonnées et l’image de partage ; icône de localisation dans l’encadré d’accueil.
- Vente et réparation d’imprimantes présentées ensemble dans le titre principal FR/NL/EN, le texte d’accueil et les métadonnées.
- Photo du stock multimarque utilisée pour tous les visuels photographiques des cartouches et toners, y compris la page détaillée, avec cadrage complet. Ancienne photo et ses trois variantes supprimées.
- Prestations réseau et Wi-Fi retirées des cartes, listes de services, FAQ, marques et métadonnées ; illustration réseau supprimée.
- Nouvelle photo extérieure réutilisée près des horaires, sur Contact et À propos, et dans les données structurées. Images responsives au format 4:3.

---

# Modifications demandées par le client — 6 octobre 2026

- Photo de la carte « Cartouches & toners » remplacée par `photo_cartouche.jpeg` fournie par le client. Trois variantes WebP de 400/800/1200 px et affichage de tous les produits sans recadrage.
- Localisation mise en avant dans un encadré orange sous le titre d’accueil : « À côté de l’arrêt Ma Campagne » et « À deux pas de l’avenue Louise », en gros caractères, également traduits sur NL/EN.
- « +450 avis » affiché dans les badges Google, le compteur et le résumé des avis des trois langues, selon la demande du client ; chiffres et libellés centralisés dans `site.google`.
- Logo rouge/bleu `LOGO DIGITAL.png` repris à l’identique dans l’en-tête et le pied de page. Référence des données structurées et image de partage actualisées ; URL du logo versionnée pour renouveler le cache.
- Expérience passée à « +35 ans » dans les textes, le badge, le compteur, le guide, les pieds de page et les métadonnées, y compris sur les versions NL/EN.
- Photos réelles de l’intérieur et de l’extérieur ajoutées côte à côte dans le bloc du magasin en haut de l’accueil FR/NL/EN. Cadrage complet en 4:3, légendes et WebP responsives de 400/800/1200 px.
- Préparation reproductible des photos avec `tools/prepare_shop_photos.py` ; sources et provenance renseignées dans `site.photos`.

---

# Photos complémentaires et mobile — 4 octobre 2026

- Photos ajoutées aux cartes PC, Mac et Cartouches ; les six prestations de l’accueil utilisent maintenant le même format photographique. Photo réelle de la vitrine ajoutée à la page Contact.
- Cartes sur une colonne sur téléphone, deux sur tablette et trois sur ordinateur ; textes, boutons et champs de formulaire adaptés aux petits écrans. Miniatures WebP de 400 px pour les photos PC, Mac et Cartouches.
- Débordement horizontal corrigé dans le guide : ses tableaux défilent dans un cadre accessible au clavier sans élargir la page.
- Menu recalé lors des changements de taille et d’orientation ; barre d’appel masquée pendant son ouverture et marges adaptées aux zones de sécurité des téléphones.
- Vérification des 16 pages sur dix formats de 320 à 1440 px, dont le paysage, puis contrôles des interactions et du build GitHub Pages.

---

# Photos d’imprimantes — 4 octobre 2026

- Visuels officiels téléchargés depuis HP, Brother et Epson : HP OfficeJet Pro 9120e, Brother MFC-L8390CDW et gamme EcoTank 2025.
- Photos ajoutées aux cartes de services de l’accueil et aux premiers écrans des pages Imprimantes, Vente et Entreprises ; petit visuel HP actualisé dans l’accueil.
- Mise en page existante conservée, appareils entiers sur fond blanc, légendes d’illustration et textes alternatifs. Lenovo et Bitdefender restent dans les catégories ordinateurs et logiciels.
- WebP responsives de moins de 20 Ko chacune, hébergées localement ; originaux, sources et droits documentés. Régénération avec `tools/prepare_printer_photos.py`.

---

# Formulaires et derniers ajustements

- Bouton de pause des marques supprimé ; pause au survol et au clavier conservée.
- Nom et téléphone requis, avec contrôles identiques dans le navigateur et sur le serveur. Accents, apostrophes et noms composés acceptés ; chiffres dans le nom et numéros incohérents refusés.
- Envoi effectif via PHP mail() au destinataire fixe digital-buro@skynet.be, vérifié sur le site d’origine. E-mail facultatif utilisé uniquement comme adresse de réponse.
- Jeton de session à usage unique, délai contrôlé côté serveur, protections contre les injections, champ piège et limitation des envois avec verrou atomique.
- Formulaire PHP autonome accessible sans JavaScript ; données de session limitées à la protection du formulaire.
- Tests avec vrai PHP et SMTP local, y compris via le navigateur ; erreur réelle affichée si le transport de courrier refuse le message. Réception externe à valider sur l’hébergement après publication.

---

# Finalisation du parcours client

- Version précédente sauvegardée et poussée sur main : 67a4244.
- Vérification du site d’origine et de ses bannières : imprimantes, PC et Mac confirmés ; aucune prestation GSM/tablettes trouvée. Offre GSM retirée des menus, cartes, formulaire, métadonnées, données structurées et sitemap. Le site généré contient désormais 16 pages.
- Avis conservés sur les seuls accueils FR/NL/EN. Suppression des notes répétées sur les autres pages et du titre « La confiance, ça se répare aussi ».
- Retrait de « Le goût du travail bien fait », titres plus factuels et conseils de visite raccourcis.
- Adresse accessible dans les premières sections ; boutons vers le magasin et les horaires plus visibles. Le parcours Cartouches/Vente ne décrit plus une réparation.
- Suppression de la promesse de migration Windows 11, non confirmée sur le site d’origine.
- Séparateurs fins bleu nuit/orange entre sections. Favicon D-B centré géométriquement ; icônes régénérées et URL versionnées pour renouveler le cache.
- Build, parcours responsive, menus, FAQ, formulaires simulés, absence de GSM et contrôle axe-core revérifiés. Aucun déploiement sur le domaine public.

---

# Changements — 29 septembre 2026

- Logo redessiné depuis l’enseigne : arcs, points, lettrage vectoriel et quatre variantes. Favicons, icônes mobiles et image de partage régénérés.
- Accueil restructuré : photo réelle du magasin, badge expérience, accès direct aux appareils, preuves de confiance, services courts, avis, histoire, étapes et accès pratique.
- Barre de recherche trompeuse remplacée par six liens vers les prestations correspondantes.
- Sept pages de service compactes, photos responsives, pannes courantes, FAQ courtes, rappel et liens connexes. Pages À propos, Contact, NL et EN simplifiées.
- Guide imprimantes conservé, avec résumé et progression de lecture.
- Navigation animée, menu mobile avec gestion du focus, FAQ, compteurs, frise, défilé des marques et illustrations. Réduction des animations et fonctionnement sans JavaScript préservés.
- Trois extraits Google attribués, carrousel au clavier et au toucher, filtrage par service avec repli explicitement général. Aucune note structurée ajoutée.
- Contact : nom et téléphone OU e-mail ; message facultatif. Nouveau formulaire de rappel, validation serveur adaptée, états d’envoi et erreur.
- Prix et WhatsApp uniquement si renseignés. Adaptateur Places serveur préparé et désactivé ; aucun appel payant effectué.
- Architecture Python/Jinja, 17 URL, redirections, sitemap, langues, suivi et schémas SEO conservés.
- Feuilles de style fusionnées au build ; mesures de géométrie inutiles au démarrage supprimées.

## Écarts documentés

- Trois extraits vérifiés au lieu de six avis complets ; dates approximatives assumées et absence d’avis spécialisés signalée.
- Photos de banque d’images en attendant les photos du client ; Vente réutilise une photo et Cartouches montre une imprimante ouverte plutôt qu’un rayonnage.
- Adaptateur Places sans cache de contenu ; configuration et raccordement à valider avant activation, voir README.
- Aucun tarif, engagement de délai, gratuité, certification ou garantie de classement inventé.
- Aucun déploiement ni test d’envoi réel d’e-mail. Résultats locaux et limites dans artifacts/VALIDATION.md.
