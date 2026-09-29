"""Vectorise le logo historique avec Inter ; rasterisation via raster_brand.cjs."""
from pathlib import Path
from fontTools.ttLib import TTFont
from make_brand import glyph_run, path_for

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / 'src/assets/img'
font = TTFont(ROOT / 'tools/fonts/Inter-Display-700.ttf')

def text_paths(text, x, baseline, size, color):
    run, width = glyph_run(font, text, -0.028)
    scale = size / font['head'].unitsPerEm
    paths = ' '.join(path_for(font, name, x+dx*scale, scale, baseline) for name, dx in run)
    return f'<path fill="{color}" d="{paths}"/>', width*scale

def logo(a, b):
    left, lw = text_paths('DIGITAL', 0, 0, 35, a)
    right, rw = text_paths('BURO', 0, 0, 35, b)
    x = (350-lw-rw-14)/2
    left, _ = text_paths('DIGITAL', x, 49, 35, a)
    right, _ = text_paths('BURO', x+lw+14, 49, 35, b)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 72" width="350" height="72"><title>Digital-Buro</title>
<path d="M80 22C123 0 228 0 270 22" fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round"/>
<path d="M80 57C123 75 228 75 270 57" fill="none" stroke="{b}" stroke-width="5" stroke-linecap="round"/>
{left}{right}<path d="M{x+lw+3:.2f} 39h8" stroke="{b}" stroke-width="3"/>
<g fill="{b}"><circle cx="12" cy="38" r="3"/><circle cx="23" cy="38" r="3"/><circle cx="34" cy="38" r="3"/></g>
<g fill="{a}"><circle cx="316" cy="38" r="3"/><circle cx="327" cy="38" r="3"/><circle cx="338" cy="38" r="3"/></g></svg>'''

for name,a,b in [('logo','#ff5900','#0b1f4d'),('logo-heritage','#ec222a','#3e59aa'),('logo-white','#ffffff','#ffffff')]:
    (IMG/f'{name}.svg').write_text(logo(a,b),encoding='utf-8')
mark_text,_ = text_paths('D-B',28,77,49,'#0b1f4d')
mark=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 144 144"><rect width="144" height="144" rx="30" fill="white"/><path d="M25 42Q72 7 119 42" fill="none" stroke="#ff5900" stroke-width="7" stroke-linecap="round"/>{mark_text}<path d="M25 99Q72 134 119 99" fill="none" stroke="#0b1f4d" stroke-width="7" stroke-linecap="round"/></svg>'''
(IMG/'logo-mark.svg').write_text(mark,encoding='utf-8')
(ROOT/'src/static/favicon.svg').write_text(mark,encoding='utf-8')
og=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#f3f3f7"/><rect x="780" width="420" height="630" fill="#0b1f4d"/><g transform="translate(50 30)">{logo('#ff5900','#0b1f4d').replace('<svg ', '<svg x="0" y="0" ')}</g>'''
for label,y,size,color in [('Réparer.',255,88,'#0b1f4d'),('C’est notre métier.',350,66,'#0b1f4d'),('Imprimantes · PC · Mac',435,30,'#60646c'),('Saint-Gilles, Bruxelles',490,30,'#60646c')]:
    og+=text_paths(label,65,y,size,color)[0]
og+=text_paths('30+',831,315,126,'#ffffff')[0]+text_paths('ans d’expérience',820,373,31,'#ffffff')[0]+'</svg>'
(IMG/'og-source.svg').write_text(og,encoding='utf-8')
print('Logos vectorisés : principal, héritage, blanc et monogramme.')
