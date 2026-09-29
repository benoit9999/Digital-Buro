/* Progressive enhancement : the document remains useful without JavaScript. */
(() => {
  'use strict';
  const root=document.documentElement;
  root.classList.add('js');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const lang=root.lang.slice(0,2);
  const text=(fr,nl,en)=>lang==='nl'?nl:lang==='en'?en:fr;
  const all=(s,r=document)=>Array.from(r.querySelectorAll(s));
  let runtime={};try{runtime=JSON.parse(document.getElementById('site-data').textContent);}catch(_){/* Static fallback. */}

  // Only content below the first screen is revealed. Never hide the hero/LCP.
  if ('IntersectionObserver' in window) {
    const nodes=all('.svc-card,.feature,.symptom,[data-reveal]');
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(!entry.isIntersecting){if(!reduced.matches&&entry.boundingClientRect.top>(entry.rootBounds?.bottom||0))entry.target.classList.add('will-reveal');return;}
      entry.target.classList.remove('will-reveal');entry.target.classList.add('is-revealed');observer.unobserve(entry.target);
    }),{threshold:0.08});
    nodes.forEach((el,i)=>{el.dataset.reveal='';el.style.setProperty('--reveal-delay',`${i%3*60}ms`);observer.observe(el);});
    // A later JS error, anchor jump or preference change must never strand hidden content.
    const revealAll=()=>nodes.forEach(el=>el.classList.remove('will-reveal'));
    reduced.addEventListener('change',revealAll);window.addEventListener('error',revealAll);setTimeout(revealAll,6500);
    const counters=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(!entry.isIntersecting)return;
      counters.unobserve(entry.target);const el=entry.target,goal=Number(el.dataset.count),digits=Number(el.dataset.decimals||0);
      if(reduced.matches)return;
      const start=performance.now();const run=now=>{const progress=Math.min((now-start)/950,1);el.textContent=(goal*(1-Math.pow(1-progress,3))).toLocaleString(lang,{minimumFractionDigits:digits,maximumFractionDigits:digits});if(progress<1&&!reduced.matches)requestAnimationFrame(run);else el.textContent=goal.toLocaleString(lang,{minimumFractionDigits:digits,maximumFractionDigits:digits});};requestAnimationFrame(run);
    }),{threshold:.5});all('[data-count]').forEach(el=>counters.observe(el));
  }

  const header=document.querySelector('[data-header]');let lastY=0,scheduled=false;
  const article=document.querySelector('article[data-reading]');let progress;
  if(article){progress=document.createElement('div');progress.className='reading-progress';progress.setAttribute('aria-hidden','true');document.body.append(progress);}
  const scroll=()=>{const y=scrollY;if(header){const menuOpen=document.body.classList.contains('menu-open');header.classList.toggle('is-hidden',innerWidth<768&&y>200&&y>lastY+4&&!menuOpen&&!header.contains(document.activeElement));}if(progress){const total=article.offsetHeight-innerHeight;progress.style.transform=`scaleX(${Math.min(1,Math.max(0,(y+100-article.offsetTop)/Math.max(1,total)))})`;}lastY=y;scheduled=false;};
  addEventListener('scroll',()=>{if(!scheduled){requestAnimationFrame(scroll);scheduled=true;}},{passive:true});

  // Modal navigation: keep keyboard focus in the menu and hide the background.
  const toggle=document.querySelector('[data-menu-toggle]'),menu=document.querySelector('[data-mobile-menu]');
  if(toggle&&menu){
    all('.mobile-menu__link',menu).forEach((el,i)=>el.style.setProperty('--menu-i',i));
    const background=all('main,.site-footer,[data-callbar]');
    const sync=()=>{const open=toggle.getAttribute('aria-expanded')==='true';background.forEach(el=>el.inert=open);menu.inert=!open;if(open){header.classList.remove('is-hidden');menu.style.setProperty('--menu-top',header.getBoundingClientRect().bottom+'px');menu.querySelector('a')?.focus({preventScroll:true});}};
    new MutationObserver(sync).observe(toggle,{attributes:true,attributeFilter:['aria-expanded']});menu.inert=true;
    document.addEventListener('keydown',e=>{if(e.key!=='Tab'||toggle.getAttribute('aria-expanded')!=='true')return;const focusables=[toggle,...all('a,button',menu)];const first=focusables[0],last=focusables.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}});
  }

  // Native details remain the source of truth and work without this enhancement.
  all('[data-faq]').forEach(details=>{
    const summary=details.querySelector('summary');let animation;
    summary.addEventListener('click',e=>{
      if(reduced.matches||!details.animate)return;
      e.preventDefault();if(animation){animation.cancel();animation=null;details.style.overflow='';}
      const from=details.offsetHeight,closing=details.open;details.open=true;
      const to=closing?summary.offsetHeight:details.offsetHeight;
      details.style.overflow='hidden';animation=details.animate({height:[from+'px',to+'px']},{duration:230,easing:'ease-out'});
      animation.onfinish=()=>{details.open=!closing;details.style.overflow='';animation=null;};
      animation.oncancel=()=>{details.style.overflow='';};
    });
  });

  all('[data-carousel]').forEach(box=>{
    const track=box.querySelector('[data-review-track]'),prev=box.querySelector('[data-prev]'),next=box.querySelector('[data-next]');
    if(!track){prev.hidden=next.hidden=true;return;}
    const update=()=>{prev.disabled=track.scrollLeft<=2;next.disabled=track.scrollLeft+track.clientWidth>=track.scrollWidth-2;};
    const move=dir=>track.scrollBy({left:dir*(track.querySelector('article').offsetWidth+18),behavior:reduced.matches?'instant':'smooth'});
    prev.addEventListener('click',()=>move(-1));next.addEventListener('click',()=>move(1));
    track.addEventListener('keydown',e=>{if(e.target!==track)return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();move(e.key==='ArrowRight'?1:-1);}});
    track.addEventListener('scroll',update,{passive:true});new ResizeObserver(update).observe(track);
    const moreButtons=all('[data-review-more]',box);
    moreButtons.forEach(button=>{button.previousElementSibling.classList.add('is-collapsed');button.addEventListener('click',()=>{const expanded=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(expanded));button.previousElementSibling.classList.toggle('is-collapsed',!expanded);button.textContent=expanded?text('Moins','Minder','Less'):text('Plus','Meer','More');});});
    const measureReviews=()=>{const overflowing=moreButtons.map(button=>button.previousElementSibling.scrollHeight>button.previousElementSibling.clientHeight+2);moreButtons.forEach((button,i)=>{button.hidden=!overflowing[i];});};
    if('IntersectionObserver' in window){const reviewObserver=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting)){measureReviews();reviewObserver.disconnect();}},{rootMargin:'100px'});reviewObserver.observe(box);}else requestAnimationFrame(measureReviews);
  });
  all('[data-review-date]').forEach(time=>{const date=new Date(time.dateTime);if(!Number.isFinite(date.getTime()))return;const days=Math.round((date-Date.now())/86400000);const units=Math.abs(days)>365?['year',Math.round(days/365)]:Math.abs(days)>30?['month',Math.round(days/30)]:['day',days];time.textContent=new Intl.RelativeTimeFormat(lang,{numeric:'auto'}).format(units[1],units[0]);});
  all('[data-motion-toggle]').forEach(btn=>btn.addEventListener('click',()=>{const paused=btn.getAttribute('aria-pressed')!=='true';btn.setAttribute('aria-pressed',String(paused));root.classList.toggle('motion-paused',paused);btn.closest('[data-marquee]').classList.toggle('is-paused',paused);btn.textContent=paused?text('Reprendre','Hervatten','Resume'):text('Mettre en pause','Pauzeren','Pause animation');}));

  // Keep tel links for touch devices and when clipboard access fails.
  const toast=document.createElement('div');toast.className='toast';toast.setAttribute('role','status');toast.setAttribute('aria-live','polite');document.body.append(toast);let toastTimer;
  if(matchMedia('(hover:hover) and (pointer:fine)').matches&&navigator.clipboard){all('a[href^="tel:"]').forEach(a=>{a.title=text('Copier le numéro','Nummer kopiëren','Copy phone number');a.addEventListener('click',async e=>{if(e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();try{await navigator.clipboard.writeText(a.href.includes('5345351')?'02 534 53 51':'02 534 47 02');toast.textContent=text('Numéro copié : 02 534 47 02','Nummer gekopieerd: 02 534 47 02','Number copied: 02 534 47 02');toast.classList.add('is-visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.classList.remove('is-visible'),2600);}catch(_){location.href=a.href;}});});}
})();
