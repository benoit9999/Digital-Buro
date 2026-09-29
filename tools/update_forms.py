from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def write(p,s):(ROOT/p).write_text(s,encoding='utf-8')
p='src/assets/js/main.js';s=read(p)
start=s.index('  var form = $("[data-contact-form]");')
end=s.index('  /* ------------------------------------------------------------------\n     Mesure',start)
s=s[:start]+'''  document.documentElement.classList.add("js");
  $$("[data-contact-form]").forEach(function(form) {
    var params = new URLSearchParams(location.search), F = DATA.form || {};
    ["appareil", "sujet"].forEach(function(key) {
      var field = form.elements[key], value = params.get(key);
      if (!field || !value) return;
      if (field.tagName === "SELECT") {
        var option = Array.from(field.options).find(function(o) { return o.value === value || o.textContent.toLowerCase().includes(value.toLowerCase()); });
        if (option) field.value=option.value;
      } else field.value=value.slice(0,160);
    });
    if(form.elements.ts) form.elements.ts.value=String(Date.now());
    var statusBox=$("[data-form-status]",form), submitBtn=$("[type=submit]",form);
    var messages = LANG === "en" ? {sending:"Sending…",ok:"Thank you. Your request has been sent.",error:"Sending failed. Please call 02 534 47 02.",contact:"Enter a phone number or an email address.",phone:"Enter a valid phone number."} : LANG === "nl" ? {sending:"Verzenden…",ok:"Bedankt. Uw aanvraag is verzonden.",error:"Verzenden mislukt. Bel 02 534 47 02.",contact:"Vul een telefoonnummer of e-mailadres in.",phone:"Vul een geldig telefoonnummer in."} : {sending:"Envoi en cours…",ok:"Merci ! Votre demande est bien envoyée.",error:"L’envoi a échoué. Appelez le 02 534 47 02.",contact:"Indiquez un téléphone ou une adresse e-mail.",phone:"Indiquez un numéro de téléphone valide."};
    function showStatus(kind,message) {
      statusBox.className="form__status is-visible form__status--"+kind;
      statusBox.textContent=message;statusBox.setAttribute("role",kind==="error"?"alert":"status");
    }
    function validateContact() {
      var phone=form.elements.telephone,email=form.elements.email;
      if(phone)phone.setCustomValidity("");if(email)email.setCustomValidity("");
      if(phone && phone.value.trim() && !/^[+()0-9 .-]{7,40}$/.test(phone.value.trim()))phone.setCustomValidity(messages.phone);
      if(email && !email.value.trim() && !phone.value.trim())phone.setCustomValidity(messages.contact);
    }
    ["telephone","email"].forEach(function(key){if(form.elements[key]) form.elements[key].addEventListener("input",validateContact);});
    if(params.get("erreur"))showStatus("error",messages.error);
    form.addEventListener("submit",function(e) {
      validateContact();
      if(!form.checkValidity()){e.preventDefault();form.reportValidity();return;}
      if(!window.fetch || !window.FormData)return;
      e.preventDefault();if(submitBtn.disabled)return;
      submitBtn.disabled=true;submitBtn.classList.add("is-sending");form.setAttribute("aria-busy","true");
      var old=submitBtn.innerHTML;submitBtn.textContent=messages.sending;
      var controller=new AbortController(),timeout=setTimeout(function(){controller.abort();},15000);
      fetch(form.action,{method:"POST",body:new FormData(form),headers:{Accept:"application/json"},signal:controller.signal})
      .then(function(res){return res.json().then(function(j){return {ok:res.ok&&j.ok,message:j.message};});})
      .then(function(res){if(res.ok){form.reset();if(form.elements.ts)form.elements.ts.value=String(Date.now());showStatus("ok",messages.ok);track("form");}else showStatus("error",LANG==="fr"&&res.message?res.message:messages.error);})
      .catch(function(){showStatus("error",messages.error);})
      .finally(function(){clearTimeout(timeout);submitBtn.disabled=false;submitBtn.classList.remove("is-sending");submitBtn.innerHTML=old;form.removeAttribute("aria-busy");});
    });
  });

'''+s[end:]
write(p,s)
p='src/static/api/contact.php';s=read(p)
s=s.replace("    'autre'      => 'Autre demande',","    'autre'      => 'Autre demande',\n    'rappel'     => 'Demande de rappel',")
s=s.replace("    respond(true, 'OK');\n}\n\n// Anti-spam 3", "    respond(false, 'Merci de patienter quelques secondes avant l’envoi.', 429);\n}\n\n// Anti-spam 3",1)
s=s.replace("if ($nom === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {\n    respond(false, 'Merci de compléter les champs obligatoires : nom, e-mail valide et message.', 422);\n}","""if ($nom === '' || ($telephone === '' && $email === '')) {
    respond(false, 'Indiquez votre nom et un téléphone ou une adresse e-mail.', 422);
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Merci de vérifier votre adresse e-mail.', 422);
}
if ($telephone !== '' && (!preg_match('/^[+()0-9 .-]{7,40}$/', $telephone) || strlen(preg_replace('/[^0-9]/', '', $telephone)) < 7)) {
    respond(false, 'Merci de vérifier votre numéro de téléphone.', 422);
}
if ($sujetKey === 'rappel' && $telephone === '') {
    respond(false, 'Le numéro de téléphone est nécessaire pour vous rappeler.', 422);
}""")
s=s.replace('$headers .= "Reply-To: {$email}\\r\\n";', 'if ($email !== \'\') $headers .= "Reply-To: {$email}\\r\\n";')
s=s.replace('$body .= "Répondre directement à cet e-mail pour contacter le client.\\n";', '$body .= $email !== \'\' ? "Répondre à cet e-mail ou rappeler le client.\\n" : "Rappeler le client au numéro indiqué.\\n";')
write(p,s)
# Contact: retain the original anchors used by old URLs and Ads.
p='src/pages/contact.html';s=read(p)
s=s.replace('required maxlength="180"','maxlength="180"').replace('name="message" required','name="message"')
s=s.replace('Téléphone <small>(facultatif)</small>','Téléphone <small>(ou e-mail)</small>').replace('for="f-email">E-mail</label>','for="f-email">E-mail <small>(ou téléphone)</small></label>')
s=s.replace('for="f-message">Votre message</label>','for="f-message">Votre message <small>(facultatif)</small></label>')
start=s.index('          <div class="field">\n            <label class="field__label" for="f-sujet">')
end=s.index('          </div>',start)+len('          </div>')
s=s[:start]+'''          <input type="hidden" name="sujet" value="reparation">'''+s[end:]
s=s.replace('<input class="field__input" id="f-appareil" name="appareil" type="text" maxlength="160" placeholder="Ex. : HP LaserJet Pro M404, MacBook Air 2020…">','''<select class="field__input" id="f-appareil" name="appareil"><option value="">Choisir un appareil</option>{% for label in ['Imprimante','Photocopieur','PC portable','PC fixe','Mac','GSM / tablette','Cartouche / toner','Entreprise','Achat de matériel','Autre'] %}<option>{{ label }}</option>{% endfor %}</select>''')
s=s.replace('Appareil <small>(marque et modèle, facultatif)</small>','Appareil')
s=s.replace('Demande de devis ou d’information','Parlons de votre appareil.')
s=re.sub(r'<p class="text" style="margin-top:8px">.*?</p>','<p class="text" style="margin-top:8px">Un téléphone ou un e-mail suffit pour vous répondre.</p>',s,count=1,flags=re.S)
s=re.sub(r'      <div class="contact-card">.*?</div>','',s,count=1,flags=re.S)
s=s.replace('    <div class="contact-cards"','    <div style="margin-top:20px">{{ ui.rating() }}</div>\n    <div class="contact-cards"',1)
start=s.index('<section class="section" id="sav"')
s=s[:start]+'''<section class="section section--tight" id="sav"><div class="container"><h2 class="h4">Un souci après votre passage ?</h2><p class="text">Appelez-nous ou <a href="/contact/?sujet=sav#formulaire">contactez le service après-vente</a> avec la date et l’appareil concerné.</p></div></section>
{% endblock %}'''
s=s.replace('Vos données servent uniquement à répondre à votre demande et ne sont jamais transmises à des tiers.', 'Vos coordonnées servent à répondre à votre demande.')
write(p,s)
print('Formulaires raccourcis, validation et état d’envoi actualisés.')
