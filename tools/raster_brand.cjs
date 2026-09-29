const path = require('path');
const sharp = require(process.env.CODEX_NODE_MODULES ? process.env.CODEX_NODE_MODULES + '/sharp' : 'sharp');
const fs = require('fs');
(async () => {
 const img='src/assets/img/', out='src/static/';
 for (const [name,size] of [['apple-touch-icon.png',180],['icon-192.png',192],['icon-512.png',512]])
  await sharp(img+'logo-mark.svg').resize(size,size).png().toFile(out+name);
 await sharp({create:{width:512,height:512,channels:4,background:'#ffffff'}}).composite([{input:await sharp(img+'logo-mark.svg').resize(300,300).png().toBuffer()}]).png().toFile(out+'icon-maskable-512.png');
 const png=await sharp(img+'logo-mark.svg').resize(48,48).png().toBuffer();
 const head=Buffer.alloc(22); head.writeUInt16LE(1,2);head.writeUInt16LE(1,4);head[6]=48;head[7]=48;head.writeUInt16LE(1,10);head.writeUInt16LE(32,12);head.writeUInt32LE(png.length,14);head.writeUInt32LE(22,18);
 fs.writeFileSync(out+'favicon.ico',Buffer.concat([head,png]));
 await sharp(img+'og-source.svg').jpeg({quality:85}).toFile(img+'og-image.jpg');
 console.log('Favicons et image de partage générés.');
})();
