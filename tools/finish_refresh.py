from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def write(p,s):(ROOT/p).write_text(s,encoding='utf-8')
# Preserve existing language anchors.
p='src/templates/home-international.html';s=read(p);s=s.replace('<a class="device-tile" href="{{ services[key].url }}"','<a {% if key == \'cartouches\' %}id="{{ \'ink-toner\' if en else \'inkt-toner\' }}"{% endif %} class="device-tile" href="{{ services[key].url }}"');write(p,s)
# Trim a redundant sentence and protect the caption under the experience stamp.
p='src/pages/index.html';s=read(p).replace('Votre appareil fait des siennes ? On s’en occupe. Toutes marques, depuis plus de 30 ans.','Votre appareil fait des siennes ? On s’en occupe. Plus de 30 ans d’expérience.');write(p,s)
p='src/assets/css/refresh.css';s=read(p)+'''\n/* Finishes after real browser review. */
.review-card{display:block}.experience-seal{bottom:-48px}.hero-scene{margin-bottom:32px}.floating-note--top{z-index:2}.floating-note--bottom{bottom:-40px}.service-advice{max-width:60ch;margin-top:24px;font-size:14px}.story-photo .photo-label{max-width:calc(100% - 32px)}
.timeline__track::before{top:58px}.timeline__track::after{top:58px}
@media(max-width:767px){.experience-seal{bottom:-30px}.hero-scene{margin-bottom:24px}.floating-note--bottom{bottom:-20px}.timeline__track::before,.timeline__track::after{top:44px}.timeline__label{font-size:9px}.review-card{padding:20px}.review-card header{margin-bottom:14px}.home-hero .hero-rating{min-height:24px}}
''';write(p,s)
# Animate only decorative SVG elements; static fallbacks remain intact.
for name in ['ill-printer.svg','ill-laptop.svg','ill-network.svg']:
 p='src/assets/img/'+name;s=read(p)
 styles='<style>@keyframes led{50%{opacity:.25}}@keyframes bar{0%{transform:scaleX(.2)}100%{transform:scaleX(1)}}@keyframes sheet{0%{transform:translateY(-3px)}100%{transform:translateY(2px)}}.led{animation:led 2s 3}.progress{transform-box:fill-box;transform-origin:left;animation:bar 2.4s 2}.sheet{animation:sheet 2s 2 alternate}@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
 s=s.replace('><path','>'+styles+'<path',1)
 if name=='ill-printer.svg':s=s.replace('<circle cx="229"','<circle class="led" cx="229"').replace('<path d="M128 38','<path class="sheet" d="M128 38')
 if name=='ill-laptop.svg':s=s.replace('<rect x="116" y="104" width="58"','<rect class="progress" x="116" y="104" width="58"')
 if name=='ill-network.svg':s=s.replace('<path d="M136.7','<path class="led" d="M136.7')
 write(p,s)
# Match the privacy description to optional contact fields; never claim no processor sees data.
p='src/pages/confidentialite.html';s=read(p).replace('votre nom, votre adresse e-mail, votre numéro de téléphone s’il est indiqué, l’appareil concerné et votre message.', 'votre nom, votre téléphone ou votre adresse e-mail, ainsi que l’appareil et le message si vous les renseignez. Le formulaire de rappel demande votre nom et votre téléphone.');write(p,s)
# Contact action validates digits consistently with PHP.
p='src/assets/js/main.js';s=read(p).replace('!/^[+()0-9 .-]{7,40}$/.test(phone.value.trim())','(!/^[+()0-9 .-]{7,40}$/.test(phone.value.trim()) || phone.value.replace(/[^0-9]/g, "").length < 7)');write(p,s)
# Leave brand generation reproducible from the established entry point.
p='tools/make_brand.py';s=read(p);s=s.replace('    main()','    import runpy\n    runpy.run_path(os.path.join(ROOT, "tools", "refresh_brand.py"), run_name="__main__")');write(p,s)
print('Finitions appliquées.')
