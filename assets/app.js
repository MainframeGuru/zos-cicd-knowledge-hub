/* z/OS CI/CD Compass – progressive enhancement. The site works fully without JS. */
(function(){
  var root=document.documentElement;
  var btn=document.getElementById('theme-toggle');
  function current(){return root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');}
  if(btn){btn.hidden=false;btn.addEventListener('click',function(){var n=current()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}btn.setAttribute('aria-label',n==='dark'?'Switch to light theme':'Switch to dark theme');});}
  var mb=document.getElementById('menu-toggle'),menu=document.getElementById('menu');
  if(mb&&menu){mb.addEventListener('click',function(){var o=menu.classList.toggle('open');mb.setAttribute('aria-expanded',o);});}

  function toast(msg){var t=document.getElementById('toast');if(!t)return;t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},1800);}
  function copy(text){if(navigator.clipboard){navigator.clipboard.writeText(text).then(function(){toast('Copied to clipboard')});}else{prompt('Copy:',text);}}
  document.addEventListener('click',function(e){
    var el=e.target.closest('[data-copy]');if(el){e.preventDefault();copy(el.getAttribute('data-copy')==='url'?location.href.split('#')[0]+(el.getAttribute('data-hash')||''):el.getAttribute('data-copy'));}
  });

  /* List filters: container with data-filter-list, chips with data-value, optional search field */
  /* Legacy (v1, German) filter values in shared URLs are mapped to the new English keys */
  var LEGACY={'alle':'all','projektreferenz':'case-study','erfahrungsbericht':'experience','vortrag':'talk','presse':'press'};
  document.querySelectorAll('[data-filter-root]').forEach(function(rootEl){
    var key=rootEl.getAttribute('data-filter-root');
    var list=rootEl.querySelector('[data-filter-list]');
    var chips=rootEl.querySelectorAll('.chip');
    var search=rootEl.querySelector('.search');
    var count=rootEl.querySelector('.count');
    var ui=rootEl.querySelector('.filters');if(ui)ui.hidden=false;if(search)search.hidden=false;
    var active='all';
    var params=new URLSearchParams(location.search);if(params.get(key))active=LEGACY[params.get(key)]||params.get(key);
    function apply(){
      var q=(search&&search.value||'').toLowerCase().trim(),n=0;
      list.querySelectorAll('[data-'+key+']').forEach(function(item){
        var ok=(active==='all'||item.getAttribute('data-'+key)===active)&&(!q||item.textContent.toLowerCase().indexOf(q)>-1);
        item.classList.toggle('hidden',!ok);if(ok)n++;
      });
      chips.forEach(function(c){c.setAttribute('aria-pressed',c.getAttribute('data-value')===active)});
      if(count)count.textContent=n+(n===1?' entry':' entries');
      var u=new URL(location.href);if(active==='all')u.searchParams.delete(key);else u.searchParams.set(key,active);history.replaceState(null,'',u);
    }
    chips.forEach(function(c){c.addEventListener('click',function(){active=c.getAttribute('data-value');apply();});});
    if(search)search.addEventListener('input',apply);
    apply();
  });
})();
// Deep links to collapsible sections (e.g. /migrations/#pitfall-codepages): open the targeted <details>.
(function(){
  function openTarget(){var id=decodeURIComponent(location.hash.slice(1));if(!id)return;var el=document.getElementById(id);if(el&&el.tagName==='DETAILS'){el.open=true;el.scrollIntoView();}}
  window.addEventListener('hashchange',openTarget);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',openTarget);else openTarget();
})();
