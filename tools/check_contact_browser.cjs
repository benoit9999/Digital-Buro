/* Runs only against the isolated PHP+SMTP test server, never production. */
const assert=require('assert');
const {chromium}=require(process.env.CODEX_NODE_MODULES+'/playwright');
(async()=>{
 const base=process.env.DB_TEST_BASE;
 assert(/^http:\/\/127\.0\.0\.1:\d+$/.test(base||''));
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try {
  const page=await browser.newPage();let posts=0;
  page.on('request',r=>{if(r.method()==='POST')posts++;});
  await page.goto(base+'/contact/');
  await page.locator('#f-nom').fill('Jean123');
  await page.locator('#f-tel').fill('025344702');
  await page.locator('[type=submit]').click();
  assert(!(await page.locator('#f-nom').evaluate(el=>el.checkValidity())));
  assert.equal(posts,0);
  await page.locator('#f-nom').fill('Élodie Martin');
  await page.locator('#f-tel').fill('0000000000');
  await page.locator('[type=submit]').click();
  assert(!(await page.locator('#f-tel').evaluate(el=>el.checkValidity())));
  assert.equal(posts,0);
  await page.locator('#f-tel').fill('+32 476 25 38 49');
  await page.waitForTimeout(2200);
  await page.locator('[type=submit]').click();
  await page.locator('.form__status--ok').waitFor();
  assert.equal(posts,1);
  assert(!(await page.locator('[type=submit]').isDisabled()));
  console.log('Browser → real PHP → local SMTP: OK; client validation OK');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
