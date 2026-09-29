const fs=require('fs');const {chromium}=require(process.env.CODEX_NODE_MODULES+'/playwright');
const {default:AxeBuilder}=require('./qa-deps/node_modules/@axe-core/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
 const page=await context.newPage(),report=[];
 for(const route of ['/','/contact/','/reparation-imprimante/','/nl/','/en/','/a-propos/']){
  await page.goto('http://127.0.0.1:8080'+route);await page.evaluate(()=>document.fonts.ready);
  const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
  report.push({route,violations:result.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))});
 }
 fs.writeFileSync('artifacts/accessibility.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
