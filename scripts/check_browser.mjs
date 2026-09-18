const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
import { fileURLToPath } from 'node:url';
import { resolve, join } from 'node:path';
const root = fileURLToPath(new URL('../', import.meta.url));
const base = process.env.BASE_URL || 'http://127.0.0.1:8022';
const artifacts = process.env.ARTIFACT_DIR || '/tmp/book2-review';
import { readdirSync, mkdirSync } from 'node:fs';
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH||undefined});
const page=await browser.newPage();
const issues=[];
page.on('pageerror',error=>issues.push(String(error)));
page.on('requestfailed',r=>issues.push('request '+r.url()+' '+r.failure()?.errorText));
const routes=['index.html','about.html',...readdirSync(resolve(root, 'chapters')).filter(x=>x.endsWith('.html')).map(x=>'chapters/'+x)];
let formulas=0,answers=0,figures=0,optional=0;
mkdirSync(artifacts,{recursive:true});
for(const width of [1440,390]) {
 await page.setViewportSize({width,height:1000});
 for(const route of routes) {
  await page.goto(base+'/'+route,{waitUntil:'networkidle'});
  const data=await page.evaluate(()=>({
   overflow:document.documentElement.scrollWidth>innerWidth,
   mathErrors:[...document.querySelectorAll('.katex-error')].map(x=>x.textContent),
   math:document.querySelectorAll('.katex').length,
   answers:document.querySelectorAll('details:not(.more)').length,
   lang:document.documentElement.lang,
   // Figures: smallest rendered label, and whether any figure spills outside its scroll box.
   figures:document.querySelectorAll('figure .fig-svg').length,
   smallLabel:Math.min(99,...[...document.querySelectorAll('.fig-svg text, .fig-svg tspan')].map(x=>{
     const svg=x.closest('svg');const k=svg.getBoundingClientRect().width/svg.viewBox.baseVal.width;
     return parseFloat(getComputedStyle(x).fontSize)*k;})),
   unwrapped:[...document.querySelectorAll('.fig-svg')].filter(x=>!x.parentElement.classList.contains('fig-scroll')).length,
   captionless:[...document.querySelectorAll('figure')].filter(x=>!x.querySelector('figcaption')||!x.querySelector('svg title')||!x.querySelector('svg desc')).length,
   raw:[...document.querySelectorAll('p,td')].filter(x=>!x.querySelector('.katex')&&/\$/.test(x.textContent)).map(x=>x.textContent)
  }));
  if(data.overflow||data.mathErrors.length||data.raw.length||data.lang!=='en')issues.push({route,width,...data});
  if(data.figures&&(data.smallLabel<10||data.unwrapped||data.captionless))issues.push({route,width,figureProblem:{smallLabel:data.smallLabel,unwrapped:data.unwrapped,captionless:data.captionless}});
  if(width===1440)figures+=data.figures;
  if(route.startsWith('chapters/')){
   if(data.math<5||data.answers!==2)issues.push({route,width,missingContent:data});
   if(width===1440)optional+=await page.locator('details.more').count();
   for(const summary of await page.locator('summary').all()){
    await summary.focus();await page.keyboard.press('Enter');
    if(!await summary.evaluate(x=>x.parentElement.open))issues.push('answer did not open '+route);
    await page.keyboard.press('Enter');
   }
  }
  if(width===1440){formulas+=data.math;answers+=data.answers;}
  await page.evaluate(()=>window.scrollTo(0,0));
  if(['index.html','chapters/09-teleportation-superdense.html','chapters/15-entropy-holevo.html'].includes(route))await page.screenshot({path:join(artifacts,route.replaceAll('/','-')+'-'+width+'.png'),fullPage:true});
 }
}
await page.goto(base+'/chapters/01-superposition-qubit.html');
await page.locator('.theme-toggle').click();
const theme=await page.locator('html').getAttribute('data-theme');
await page.reload();
if(await page.locator('html').getAttribute('data-theme')!==theme)issues.push('theme not persisted');
await page.goto(base+'/chapters/01-superposition-qubit.html',{waitUntil:'networkidle'});
await page.keyboard.press('Tab');
if(!await page.locator('.skip-link').evaluate(x=>document.activeElement===x))issues.push('Skip link was not the first keyboard target');
await page.emulateMedia({media:'print'});
const printedAnswers = await page.evaluate(() => {
 window.dispatchEvent(new Event('beforeprint'));
 const count=document.querySelectorAll('details[open]:not(.more)').length;
 window.dispatchEvent(new Event('afterprint'));
 return count;
});
if(printedAnswers!==2)issues.push('Print did not open both solutions');
const printedOptional = await page.evaluate(() => {
 window.dispatchEvent(new Event('beforeprint'));
 const closed=document.querySelectorAll('details.more:not([open])').length;
 window.dispatchEvent(new Event('afterprint'));
 return closed;
});
if(printedOptional)issues.push('Print left an optional derivation closed');
const printInk=await page.locator('h1').evaluate(x=>getComputedStyle(x).color);
if(printInk!=='rgb(0, 0, 0)')issues.push('Print theme is not black: '+printInk);
await page.pdf({path:join(artifacts,'chapter01.pdf'),format:'A4',printBackground:true});
if(await page.locator('details[open]').count())issues.push('Printing left solutions open');
console.log(JSON.stringify({routes:routes.length,viewports:2,formulas,answers,figures,optional,issues},null,2));
await browser.close();
if(issues.length)process.exit(1);
