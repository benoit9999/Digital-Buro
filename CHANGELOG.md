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
