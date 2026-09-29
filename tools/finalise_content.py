from pathlib import Path
import json,re
root=Path('.')
def edit(path,replacements):
 p=root/path;s=p.read_text(encoding='utf-8-sig')
 for a,b in replacements:
  if a not in s: print('Missing:',path,a[:65])
  s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
p=root/'src/data/site.json';site=json.loads(p.read_text(encoding='utf-8-sig'))
site['services']=[s for s in site['services'] if s['key']!='gsm'];site['service_content'].pop('gsm');site['photos'].pop('gsm',None)
for s in site['services']:
 if s['key']=='imprimante':s['teaser']='Diagnostic, entretien et réparation, en atelier ou dans vos locaux.'
 if s['key']=='entreprises':s['teaser']='Maintenance, réseau, installation et livraison de consommables pour votre bureau.'
for key,c in site['service_content'].items():
 c.pop('review_tag',None);c['process_title']='Comment se déroule la réparation ?';c['faq_title']='Questions pratiques'
 c['related']=[k for k in c['related'] if k!='gsm']
 for qa in c['faq']:
  qa[1]=qa[1].replace('Le devis vous permet de décider de la suite, sans mauvaise surprise sur les travaux envisagés.','Le devis précise les travaux proposés avant votre décision.')
updates={
'imprimante':{'lead':'Diagnostic et réparation d’imprimantes et de photocopieurs, en atelier ou sur site.','heading':'Les pannes d’imprimante courantes','advice':'Pour votre visite : notez le modèle et le code erreur. Apportez une page montrant le défaut.'},
'ordinateur':{'eyebrow':'DIAGNOSTIC & ENTRETIEN','heading':'Les pannes de PC courantes','lead':'PC fixe ou portable : décrivez la panne pour préparer le diagnostic.','note':'','advice':'Apportez le chargeur de votre portable et notez les symptômes. Sauvegardez vos fichiers si vous le pouvez.'},
'mac':{'lead':'Contactez le magasin avec le modèle de votre Mac et les symptômes de la panne.','eyebrow':'DIAGNOSTIC & RÉPARATION','heading':'Les problèmes à signaler','advice':'Notez le modèle de votre Mac. Pour un MacBook, apportez le chargeur. Sauvegardez vos fichiers si possible.'},
'cartouches':{'heading':'Cartouches, toners, tambours et rubans','process_title':'Trouver votre consommable','advice':'Apportez votre ancienne cartouche ou une photo de sa référence et du modèle de l’imprimante.'},
'vente':{'heading':'Le matériel disponible au magasin','process_title':'Choisir et installer votre matériel','note':'','advice':'Indiquez votre budget, votre usage et la place disponible. Apportez la référence de l’appareil à remplacer.'},
'entreprises':{'lead':'Entretien, réparation et installation de votre matériel de bureau, en atelier ou dans vos locaux.','heading':'Les services pour votre entreprise','process_title':'Organiser une intervention','note':'Interventions en atelier ou dans vos locaux : contactez le magasin pour convenir des modalités.','advice':'Pour une intervention : indiquez votre adresse, les appareils concernés et le problème rencontré.'}}
for key,data in updates.items():site['service_content'][key].update(data)
pc=site['service_content']['ordinateur'];pc['faq']=[q for q in pc['faq'] if 'Windows 11' not in q[0]]
site['service_content']['cartouches']['steps']=[['Votre référence','Apportez la cartouche ou le modèle de votre imprimante.'],['Vérification du stock','Nous vérifions la référence et sa disponibilité.'],['Achat au magasin','Choisissez le consommable adapté à votre appareil.']]
site['service_content']['vente']['steps']=[['Votre besoin','Indiquez votre usage et votre budget.'],['Choix du matériel','Comparez les appareils et les consommables nécessaires.'],['Installation','Convenez de la livraison et de la configuration souhaitées.']]
site['service_content']['entreprises']['steps']=[['Votre demande','Décrivez la panne, le matériel et le lieu d’intervention.'],['Diagnostic et devis','Nous définissons avec vous les travaux à réaliser.'],['Intervention','En atelier ou dans vos locaux, selon les modalités convenues.']]
p.write_text(json.dumps(site,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=root/'src/data/pages.json';pages=json.loads(p.read_text(encoding='utf-8-sig'));pages=[x for x in pages if x.get('nav')!='gsm']
for x in pages:
 x['description']=x['description'].replace('PC, Mac et GSM','PC et Mac').replace('pc’s, Macs en gsm’s','pc’s en Macs').replace('PC, Mac and phone repair','PC and Mac repair')
 if x['nav']=='ordinateur':x['description']='Réparation de PC fixes et portables toutes marques à Saint-Gilles, Bruxelles. Diagnostic, entretien et dépannage informatique au magasin Digital-Buro.'
 if x['nav']=='vente':x['description']=x['description'].replace('Conseil honnête,','Conseil,')
p.write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in ['src/templates/partials/header.html','src/templates/partials/footer.html']:
 edit(path,[("['imprimante', 'ordinateur', 'mac', 'gsm']","['imprimante', 'ordinateur', 'mac']")])
edit('src/pages/404.html',[("'mac', 'gsm', 'cartouches'","'mac', 'vente', 'cartouches'")])
edit('build.py',[("de PC, de Mac et de GSM toutes marques","de PC et de Mac toutes marques"),('"refresh": short_hash(out / "assets/css/refresh.css"),','"brand": short_hash(out / "favicon.svg"),\n        "refresh": short_hash(out / "assets/css/refresh.css"),'),(', "gsm": "Gsm- en tabletherstelling"',''),(', "gsm": "Phone & tablet repair"','')])
edit('src/templates/base.html',[("href=\"/favicon.ico\"","href=\"/favicon.ico?v={{ v.brand }}\""),("href=\"/favicon.svg\"","href=\"/favicon.svg?v={{ v.brand }}\""),("href=\"/apple-touch-icon.png\"","href=\"/apple-touch-icon.png?v={{ v.brand }}\"")])
edit('src/pages/index.html',[
 ("('gsm','GSM / tablette','smartphone')","('imprimante','Photocopieur','scan')"),
 ("['imprimante','ordinateur','mac','gsm','cartouches','entreprises']","['imprimante','ordinateur','mac','vente','cartouches','entreprises']"),
 ('PC, Mac, GSM et tablettes','PC et Mac'),
 ('<span class="photo-label">Le goût du travail bien fait.</span>',''),
 ('Les machines changent.<br>Le savoir-faire reste.','Réparation, conseil<br>et entretien au magasin.'),
 ('UN VRAI MAGASIN, TOUT SIMPLEMENT.','DIGITAL-BURO · MA CAMPAGNE'),
 ('Un problème en moins.<br>Un appareil qui repart.','Nos services au magasin.'),
 ('<strong>Votre magasin. Vos solutions.</strong>','<strong>Chaussée de Charleroi 257</strong>'),
 ('<strong>Une seconde vie.</strong><small>Ça commence ici.</small>','<strong>Réparation & entretien</strong><small>Imprimantes toutes marques</small>'),
 ('Chaque génération de machines nous a appris quelque chose.','Plus de 30 ans d’expérience en bureautique et informatique.'),
 ("ui.cta_band('On regarde ça ensemble ?', 'Un appel, et vous savez par où commencer.')","ui.cta_band('Besoin d’une réparation ou d’un consommable ?', 'Retrouvez-nous Chaussée de Charleroi 257, à Saint-Gilles.')"),
 ('<div class="hero-status">{{ fx.status() }}</div>','<div class="hero-status">{{ fx.status() }}</div><p class="visit-address">{{ ui.icon("pin") }}<a href="#acces">{{ site.street }} · Ma Campagne</a></p>')])
edit('src/templates/service-compact.html',[
 ('<div class="hero__proof">{{ ui.rating() }}</div>','<p class="visit-address">{{ ui.icon("pin") }}<a href="/contact/#acces">{{ site.street }}, {{ site.city }}</a></p>'),
 ('{{ fx.reviews(c.review_tag) }}',''),
 ('{{ ui.process() }}','{{ ui.process(c.steps|default(None)) }}'),
 ('<p class="text service-advice">{{ c.advice }}</p>','<p class="text service-advice">{{ c.advice }}</p><div class="btn-row visit-actions">{{ ui.directions_btn(label="Venir au magasin",cls="btn--primary") }}{{ ui.call_btn(label="Appeler le magasin",cls="btn--outline") }}</div>')])
edit('src/templates/macros.html',[
 ('{% macro process() -%}','{% macro process(custom_steps=None) -%}'),
 ("('Votre appareil repart', 'La réparation convenue, votre machine retrouve son utilité.')","('Réparation', 'Nous réalisons les travaux convenus avec vous.')"),
 ('{% for title,desc in steps %}','{% if custom_steps %}{% set steps=custom_steps %}{% endif %}\n{% for title,desc in steps %}'),
 ('{{ quote_btn(cls="btn--outline btn--lg") }}\n      </div>\n    </div>\n  </div>\n</section>','{{ directions_btn(cls="btn--outline btn--lg") }}\n      </div>\n    </div>\n  </div>\n</section>')])
edit('src/pages/a-propos.html',[
 ('{{ ui.rating() }}',''),('{{ fx.reviews() }}',''),
 ('30 ans de métier.<br>Et toujours l’envie de réparer.','Plus de 30 ans d’expérience<br>en bureautique et informatique.'),
 ('Les machines changent. Le plaisir de trouver la solution reste.','Réparation, vente et entretien de matériel à Saint-Gilles, pour particuliers et professionnels.'),
 ('Un vrai magasin. Un vrai interlocuteur.','Réparation · Consommables · Vente'),
 ("ui.cta_band('Faisons connaissance.', 'Appelez-nous ou retrouvez-nous à Ma Campagne.')","ui.cta_band('Visitez notre magasin à Saint-Gilles.', 'Chaussée de Charleroi 257, quartier Ma Campagne.')")])
edit('src/pages/contact.html',[
 ('    <div style="margin-top:20px">{{ ui.rating() }}</div>','    <div class="btn-row" style="margin-top:20px">{{ ui.directions_btn(label="Venir au magasin",cls="btn--primary") }}<a class="btn btn--outline" href="#horaires">Voir les horaires</a></div>'),
 ('<div class="stack-lg">','<div class="stack-lg" id="acces">'),
 ('<h2 class="h4">Horaires d’ouverture</h2>','<h2 class="h4" id="horaires">Horaires d’ouverture</h2>'),
 ("'Mac','GSM / tablette','Cartouche / toner'","'Mac','Cartouche / toner'"),
 ('Passez au magasin, appelez-nous ou décrivez votre demande ci-dessous&nbsp;: nous vous répondons pendant les heures d’ouverture.','Retrouvez-nous Chaussée de Charleroi 257, à Ma Campagne. Pour une question, appelez-nous ou utilisez le formulaire.'),
 ('Réponse pendant les heures d’ouverture','Écrire au magasin'),
 ('Parlons de votre appareil.','Envoyer une demande')])
# Home translations retain the homepage review block, not the service-page repetitions.
edit('src/templates/home-international.html',[
 ("'Phone / tablet'","'Photocopier'"),("'Gsm / tablet'","'Kopieerapparaat'"),("('gsm','smartphone')","('imprimante','scan')"),
 ('printer, PC, Mac or phone','printer, PC or Mac'),('printer, pc, Mac of gsm','printer, pc of Mac'),
 ('Your shop. Your solutions.','Chaussée de Charleroi 257'),('Uw winkel. Uw oplossing.','Charleroise Steenweg 257'),
 ('Devices change. Experience stays.','Repairs, advice and maintenance.'),('Toestellen veranderen. Vakmanschap blijft.','Herstelling, advies en onderhoud.')])
edit('src/templates/partials/fresh-macros.html',[
 ('La confiance, ça se répare aussi.','Les avis de nos clients'),('A shop you can trust.','Customer reviews'),('Een winkel die u vertrouwt.','Klantenreviews'),
 ('Nos clients en parlent le mieux','DIGITAL-BURO · SAINT-GILLES'),('Your neighbours say it best','DIGITAL-BURO · SAINT-GILLES'),('Onze klanten aan het woord','DIGITAL-BURO · SINT-GILLIS')])
print('Content and customer journey updated.')
