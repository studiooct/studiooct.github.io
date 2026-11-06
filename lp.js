(function(){
  var a=document.getElementById('bgm'),b=document.querySelector('.bgm');
  if(a&&b){a.volume=.45;
    var label=b.querySelector('b');
    b.addEventListener('click',function(){
      if(a.paused){var p=a.play();if(p&&p.catch)p.catch(function(){});b.setAttribute('aria-pressed','true');label.textContent=b.dataset.on;}
      else{a.pause();b.setAttribute('aria-pressed','false');label.textContent=b.dataset.off;}
    });
  }
  document.querySelectorAll('.ev').forEach(function(ev){
    var r=ev.querySelector('.ev-r'),bs=ev.querySelectorAll('.ev-c');
    bs.forEach(function(x){x.setAttribute('aria-pressed','false');
      x.addEventListener('click',function(){
        bs.forEach(function(y){y.setAttribute('aria-pressed','false');});
        x.setAttribute('aria-pressed','true');r.textContent=x.dataset.r;r.hidden=false;
      });});
  });
})();
