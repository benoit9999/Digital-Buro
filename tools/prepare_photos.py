"""Téléchargement des photos identifiées et variantes WebP optimisées."""
import io, json, urllib.request
from pathlib import Path
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'src/assets/img/photos'
OUT.mkdir(exist_ok=True)
photos=[
 ('imprimante','https://images.unsplash.com/photo-1650094980833-7373de26feb6','https://unsplash.com/photos/CGnoRQZGWmw','engin akyurt','Photocopieur multifonction blanc dans un bureau'),
 ('entreprises','https://images.unsplash.com/photo-1613395450289-e560907d9308','https://unsplash.com/photos/8r1ZlqqGxMU','Meatball Overexposure','Imprimante et matériel informatique dans un bureau lumineux'),
 ('mac','https://images.unsplash.com/45/QDSMoAMTYaZoXpcwBjsL__DSC0104-1.jpg','https://unsplash.com/photos/mCg0ZgD7BgU','Aleksi Tappura','MacBook ouvert sur un bureau en bois'),
 ('ordinateur','https://images.pexels.com/photos/7639373/pexels-photo-7639373.jpeg','https://www.pexels.com/photo/7639373/','IT services EU','Réparation d’un ordinateur portable ouvert avec un tournevis'),
 ('gsm','https://images.pexels.com/photos/6754839/pexels-photo-6754839.jpeg','https://www.pexels.com/photo/6754839/','Tima Miroshnichenko','Intervention sur un smartphone avec des outils de précision'),
 ('cartouches','https://images.pexels.com/photos/17536002/pexels-photo-17536002.jpeg','https://www.pexels.com/photo/17536002/','Jakub Zerdzicki','Cartouches d’encre dans une imprimante photo'),
]
def get(p):
 key,url,source,author,alt=p
 # Pas de contournement : une source indisponible reste signalée.
 try:
  req=urllib.request.Request(url+'?w=1600&auto=format&fit=crop',headers={'User-Agent':'Mozilla/5.0'})
  image=Image.open(io.BytesIO(urllib.request.urlopen(req,timeout=20).read())).convert('RGB')
  for width in (800,1600):
   im=ImageOps.fit(image,(width,width*5//8),method=Image.Resampling.LANCZOS)
   q=80
   while True:
    buffer=io.BytesIO();im.save(buffer,'WEBP',quality=q,method=6)
    if len(buffer.getvalue())<=150000 or q<=40:break
    q-=5
   (OUT/f'{key}-{width}.webp').write_bytes(buffer.getvalue())
  return key,dict(file=key,alt=alt,source=source,author=author,license='https://unsplash.com/license' if 'unsplash' in url else 'https://www.pexels.com/license/')
 except Exception as exc:
  print(key, str(exc));return key,None
with ThreadPoolExecutor(max_workers=4) as pool:
 result=dict(pool.map(get,photos))
(ROOT/'tools/photo-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Photos disponibles:', ', '.join(k for k,v in result.items() if v))
