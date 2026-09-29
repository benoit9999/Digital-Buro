/* Local regression checks; never sends a real form or calls external APIs. */
const fs=require('fs');const assert=require('assert');
const {chromium}=require(process.env.CODEX_NODE_MODULES+'/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const base='http://127.0.0.1:8080';fs.mkdirSync('artifacts',{recursive:true});const errors=[];
 const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({animations:'disabled',path:'artifacts/home-desktop.png'});
 for(const width of [375,390,768,1100,1440]){
  await page.setViewportSize({width,height:900});
  for(const route of ['/','/contact/','/reparation-imprimante/','/reparation-ordinateur/','/nl/','/en/']){
   await page.goto(base+route);await page.evaluate(()=>document.fonts.ready);
   const widthOK=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
   assert(widthOK,'Overflow '+width+' '+route);
   assert(await page.locator('h1').count()===1,'H1 '+route);
   assert(await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>i.complete&&!i.naturalWidth).length)===0,'Broken image '+route);
  }
 }
 await page.setViewportSize({width:390,height:844});await page.goto(base);
 await page.screenshot({animations:'disabled',path:'artifacts/home-mobile.png'});
 await page.locator('[data-menu-toggle]').click();assert(await page.locator('[data-mobile-menu]').evaluate(el=>getComputedStyle(el).visibility==='visible'));await page.keyboard.press('Escape');assert(await page.locator('[data-menu-toggle]').getAttribute('aria-expanded')==='false');
 const faq=page.locator('[data-faq]').first();await faq.locator('summary').click();await page.waitForTimeout(300);assert(await faq.getAttribute('open')!==null);await faq.locator('summary').click();await page.waitForTimeout(300);assert(await faq.getAttribute('open')===null);
 await page.locator('.reviews-section').scrollIntoViewIfNeeded();await page.screenshot({animations:'disabled',path:'artifacts/reviews-mobile.png'});
 await page.locator('[data-next]').click();await page.waitForTimeout(500);assert(await page.locator('[data-review-track]').evaluate(el=>el.scrollLeft)>0);
 await page.route('**/api/contact.php?token=1',r=>r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:true,token:'test-token'})}));await page.goto(base+'/contact/');await page.route('**/api/contact.php',r=>r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:true})}));
 await page.locator('#f-nom').fill('Test local');await page.locator('#f-tel').fill('025344702');await page.locator('button[type=submit]').click();await page.locator('.form__status--ok').waitFor();
 await page.unroute('**/api/contact.php');await page.route('**/api/contact.php',r=>r.fulfill({status:500,contentType:'application/json',body:JSON.stringify({ok:false,message:'Erreur de test'})}));
 await page.locator('#f-nom').fill('Test local');await page.locator('#f-email').fill('test@example.invalid');await page.locator('#f-tel').fill('025344702');await page.locator('button[type=submit]').click();await page.locator('.form__status--error').waitFor();assert(!await page.locator('button[type=submit]').isDisabled());
 await page.goto(base+'/reparation-imprimante/');await page.screenshot({animations:'disabled',path:'artifacts/service-mobile.png'});
 await page.setViewportSize({width:1440,height:1000});await page.goto(base+'/reparation-imprimante/');await page.screenshot({animations:'disabled',path:'artifacts/service-desktop.png'});
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto(base);assert(await page.locator('.brand-run').evaluate(el=>getComputedStyle(el).animationName)==='none');
 const noJS=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const staticPage=await noJS.newPage();await staticPage.goto(base);assert(await staticPage.locator('.no-js-nav').isVisible());assert(await staticPage.locator('h1').isVisible());
 assert(errors.length===0,errors.join('\n'));fs.writeFileSync('artifacts/browser-checks.json',JSON.stringify({ok:true,widths:[375,390,768,1100,1440],errors,forms:'Success and failure mocked; no real email sent'},null,2));
 console.log('Responsive, menu, FAQ, carousel, forms, reduced motion, no-JS: OK');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

