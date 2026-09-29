const fs=require('fs');const {pathToFileURL}=require('url');const path=require('path');
const {chromium}=require(process.env.CODEX_NODE_MODULES+'/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--remote-debugging-port=9223']});
 try {
  const {default:lighthouse}=await import(pathToFileURL(path.resolve('tools/qa-deps/node_modules/lighthouse/core/index.js')));
  for(const [name,route] of [['home','/'],['service','/reparation-imprimante/'],['contact','/contact/']]){
   if(process.env.LH_PAGE&&name!==process.env.LH_PAGE)continue;
   const result=await lighthouse((process.env.LH_BASE||'http://127.0.0.1:8080')+route,{port:9223,output:'json',onlyCategories:['performance','accessibility','seo'],logLevel:'error'});
   fs.writeFileSync('artifacts/lighthouse-'+name+'.json',result.report);
   console.log(name,Object.fromEntries(Object.entries(result.lhr.categories).map(([key,val])=>[key,val.score])), 'CLS',result.lhr.audits['cumulative-layout-shift'].numericValue);
  }
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
