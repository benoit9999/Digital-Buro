/* Run only against the PHP server connected to the isolated SMTP test inbox. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require((process.env.CODEX_NODE_MODULES||'C:/Users/ramym/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const base=process.env.DB_TEST_BASE,store=process.env.DB_TEST_STORE;
assert(/^http:\/\/127\.0\.0\.1:\d+$/.test(base||''));
assert(store&&path.resolve(store).startsWith(path.resolve('.deps')+path.sep));
const clearLimits=()=>{for(const file of fs.readdirSync(store).filter(f=>f.startsWith('db_html_contact_v1_')))fs.writeFileSync(path.join(store,file),'');};
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const errors=[],layouts=[];
 try{
  const page=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
  page.on('pageerror',e=>errors.push(e.message));
  if(process.env.DB_TEST_PHASE!=='failure'){
   const pages=JSON.parse(fs.readFileSync('src/data/pages.json','utf8'));
   let forms=0;
   for(const width of [390,1440]){
    await page.setViewportSize({width,height:width===390?844:1000});
    for(const spec of pages){
     await page.goto(base+'/'+spec.template);
     await page.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode()));});
     assert.equal(await page.locator('h1').count(),1,spec.template);
     assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),spec.template+' horizontal overflow');
     for(const form of await page.locator('form[data-contact-form]').all()){
      assert.equal(await form.getAttribute('action'),'send_contact.php');
      assert.equal(await form.locator('[name=form_token]').count(),1);
      assert.equal(await form.locator('[name=site_web]').count(),1);
      if(width===390)forms++;
     }
     layouts.push({page:spec.template,width});
    }
   }
   clearLimits();
   let posts=0;page.on('request',r=>{if(r.method()==='POST')posts++;});
   await page.goto(base+'/contact.html?appareil=Imprimante#formulaire');
   assert.equal(await page.locator('#f-appareil').inputValue(),'Imprimante');
   await page.locator('#f-nom').fill('Jean123');await page.locator('#f-tel').fill('025344702');
   await page.locator('[type=submit]').click();assert.equal(posts,0);
   await page.locator('#f-nom').fill('Élodie Martin');await page.locator('#f-tel').fill('0000000000');
   await page.locator('[type=submit]').click();assert.equal(posts,0);
   await page.locator('#f-tel').fill('+32 476 25 38 49');
   await page.locator('#f-message').fill('Contact envoyé depuis le navigateur de test.');
   await page.locator('[type=submit]').click();
   await page.locator('.form__status--ok').waitFor();assert.equal(posts,1);
   assert.equal(await page.locator('[type=submit]').isDisabled(),false);
   for(const filename of ['index.html','cartouches-toners.html','en.html','nl.html']){
    clearLimits();await page.goto(base+'/'+filename);
    const form=page.locator('form[data-callback]');
    await form.locator('[name=nom]').fill('Élodie Martin');
    await form.locator('[name=telephone]').fill('+32 476 25 38 49');
    await form.locator('[type=submit]').click();await form.locator('.form__status--ok').waitFor();
   }
   clearLimits();
   const native=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
   const fallback=await native.newPage();await fallback.goto(base+'/contact.html');
   await fallback.locator('noscript a[href="send_contact.php?form=1"]').click();
   await fallback.locator('[name=nom]').fill('Élodie Martin');
   await fallback.locator('[name=telephone]').fill('025344702');
   await fallback.locator('[name=message]').fill('Demande envoyée sans JavaScript.');
   await fallback.waitForTimeout(2100);await fallback.locator('[type=submit]').click();
   await fallback.waitForURL('**/merci.html');await native.close();
   fs.writeFileSync('artifacts/html-form-browser-tests.json',JSON.stringify({ok:true,pages:16,layouts:layouts.length,forms,callbackLocales:['fr','en','nl'],nativeFallback:true,errors},null,2));
   console.log('32 page layouts, 10 form connections, contact, FR/EN/NL callbacks and native PHP fallback passed.');
  }else{
   clearLimits();await page.goto(base+'/contact.html');
   await page.locator('#f-nom').fill('Élodie Martin');await page.locator('#f-tel').fill('025344702');
   await page.locator('[type=submit]').click();await page.locator('.form__status--error').waitFor();
   assert.equal(await page.locator('.form__status--ok').count(),0);
   assert.equal(await page.locator('#f-nom').inputValue(),'Élodie Martin');
   assert.equal(await page.locator('[type=submit]').isDisabled(),false);
   console.log('Mail transport failure displayed honestly; entered fields retained and submit button restored.');
  }
  assert.deepEqual(errors,[]);
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1});
