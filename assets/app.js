/* z/OS CI/CD Kompass – progressive enhancement. Seite funktioniert vollständig ohne JS. */
(function(){
  var root=document.documentElement;
  var btn=document.getElementById('theme-toggle');
  function current(){return root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');}
  if(btn){btn.hidden=false;btn.addEventListener('click',function(){var n=current()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}btn.setAttribute('aria-label',n==='dark'?'Helles Design aktivieren':'Dunkles Design aktivieren');});}
  var mb=document.getElementById('menu-toggle'),menu=document.getElementById('menu');
  if(mb&&menu){mb.addEventListener('click',function(){var o=menu.classList.toggle('open');mb.setAttribute('aria-expanded',o);});}

  function toast(msg){var t=document.getElementById('toast');if(!t)return;t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},1800);}
  function copy(text){if(navigator.clipboard){navigator.clipboard.writeText(text).then(function(){toast('In die Zwischenablage kopiert')});}else{prompt('Kopieren:',text);}}
  document.addEventListener('click',function(e){
    var el=e.target.closest('[data-copy]');if(el){e.preventDefault();copy(el.getAttribute('data-copy')==='url'?location.href.split('#')[0]+(el.getAttribute('data-hash')||''):el.getAttribute('data-copy'));}
  });

  /* Filter für Listen: Container mit data-filter-list, Chips mit data-filter-key/value, optional Suchfeld */
  document.querySelectorAll('[data-filter-root]').forEach(function(rootEl){
    var key=rootEl.getAttribute('data-filter-root');
    var list=rootEl.querySelector('[data-filter-list]');
    var chips=rootEl.querySelectorAll('.chip');
    var search=rootEl.querySelector('.search');
    var count=rootEl.querySelector('.count');
    var ui=rootEl.querySelector('.filters');if(ui)ui.hidden=false;if(search)search.hidden=false;
    var active='alle';
    var params=new URLSearchParams(location.search);if(params.get(key))active=params.get(key);
    function apply(){
      var q=(search&&search.value||'').toLowerCase().trim(),n=0;
      list.querySelectorAll('[data-'+key+']').forEach(function(item){
        var ok=(active==='alle'||item.getAttribute('data-'+key)===active)&&(!q||item.textContent.toLowerCase().indexOf(q)>-1);
        item.classList.toggle('hidden',!ok);if(ok)n++;
      });
      chips.forEach(function(c){c.setAttribute('aria-pressed',c.getAttribute('data-value')===active)});
      if(count)count.textContent=n+' Einträge';
      var u=new URL(location.href);if(active==='alle')u.searchParams.delete(key);else u.searchParams.set(key,active);history.replaceState(null,'',u);
    }
    chips.forEach(function(c){c.addEventListener('click',function(){active=c.getAttribute('data-value');apply();});});
    if(search)search.addEventListener('input',apply);
    apply();
  });
})();
