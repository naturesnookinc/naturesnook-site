
<script>
/* Pickup orders. Dormant unless NN_PICKUP.endpoint is set (see tools/pickup/README.md). The order list lives in page memory only: no cookies, no storage. */
window.NN_PICKUP={endpoint:"",maxLines:30,maxQty:10};
(function(){
  var C=window.NN_PICKUP; if(!C.endpoint) return;
  var cart={}, order=[], d=document, lastFocus=null;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function money(n){return '$'+Number(n).toFixed(2)}
  function count(){return order.reduce(function(a,u){return a+cart[u].qty},0)}
  function total(){return order.reduce(function(a,u){return a+cart[u].qty*cart[u].price},0)}

  // floating button + dialog
  var fab=d.createElement('button'); fab.type='button'; fab.className='pk-fab'; fab.hidden=true; d.body.appendChild(fab);
  var back=d.createElement('div'); back.className='pk-back'; back.hidden=true;
  back.innerHTML='<div class="pk" role="dialog" aria-modal="true" aria-labelledby="pk-h"><button type="button" class="pk-x" aria-label="Close">×</button><div id="pk-body"></div></div>';
  d.body.appendChild(back);
  var dlg=back.firstChild, body=d.getElementById('pk-body');

  function syncFab(){ var n=count(); fab.hidden=!n; fab.textContent='Pickup order ('+n+')'; }
  function open(){ lastFocus=d.activeElement; back.hidden=false; draw(); var f=dlg.querySelector('input,button.pk-x'); (dlg.querySelector('#pk-name')||f).focus(); }
  function close(){ back.hidden=true; if(lastFocus&&lastFocus.focus) try{lastFocus.focus()}catch(e){} }
  fab.addEventListener('click',open);
  dlg.querySelector('.pk-x').addEventListener('click',close);
  back.addEventListener('click',function(e){ if(e.target===back) close(); });
  d.addEventListener('keydown',function(e){
    if(back.hidden) return;
    if(e.key==='Escape'){ close(); return; }
    if(e.key==='Tab'){ // keep focus inside the dialog
      var f=[].slice.call(dlg.querySelectorAll('button,input,textarea,a[href]')).filter(function(x){return !x.disabled&&x.offsetParent!==null});
      if(!f.length) return; var a=f[0], z=f[f.length-1];
      if(e.shiftKey&&d.activeElement===a){ e.preventDefault(); z.focus(); } else if(!e.shiftKey&&d.activeElement===z){ e.preventDefault(); a.focus(); }
    }
  });

  function draw(done){
    if(done){
      body.innerHTML='<h2 id="pk-h">Order received</h2><p>Thanks, '+esc(done.name)+'. Your pickup request <strong>#'+esc(done.id)+'</strong> is in. We will text you at the number you gave once we have confirmed it and it is ready.</p><p class="pk-fine">Pay in store at pickup. Prices are those shown on the site; the price at the register applies. Questions? Call <a href="tel:+12083565284">(208) 356-5284</a>.</p><button type="button" class="pk-btn" id="pk-done">Done</button>';
      d.getElementById('pk-done').addEventListener('click',close); d.getElementById('pk-done').focus(); return;
    }
    if(!order.length){ body.innerHTML='<h2 id="pk-h">Pickup order</h2><p>Your order is empty. Open any product and choose &ldquo;Add to pickup order&rdquo;.</p><button type="button" class="pk-btn" id="pk-done">Close</button>'; d.getElementById('pk-done').addEventListener('click',close); return; }
    body.innerHTML='<h2 id="pk-h">Pickup order</h2><p class="pk-fine">This is a request, not a purchase. We confirm what is in stock by text or phone, and you pay in store at pickup.</p>'
     +'<ul class="pk-lines">'+order.map(function(u){var l=cart[u];return '<li><div><div class="pk-n">'+esc(l.name)+'</div><div class="pk-v">'+esc([l.brand,l.variant].filter(Boolean).join(' · '))+'</div></div><div>'+money(l.price*l.qty)+'</div><div class="pk-qty" data-u="'+esc(u)+'"><button type="button" data-a="-" aria-label="Fewer: '+esc(l.name)+'">&minus;</button><output aria-live="polite">'+l.qty+'</output><button type="button" data-a="+" aria-label="More: '+esc(l.name)+'">+</button><button type="button" class="pk-rm" data-a="x" aria-label="Remove '+esc(l.name)+'">Remove</button></div></li>'}).join('')+'</ul>'
     +'<div class="pk-total"><span>Estimated total</span><span>'+money(total())+'</span></div><p class="pk-fine">Estimate only. Member prices and the register price apply at pickup.</p>'
     +'<form id="pk-form" novalidate><label>Your name<input type="text" id="pk-name" name="name" autocomplete="name" maxlength="80" required></label>'
     +'<label>Mobile phone<input type="tel" id="pk-phone" name="phone" autocomplete="tel" inputmode="tel" maxlength="20" required></label>'
     +'<label>Note for the store (optional)<textarea id="pk-note" name="note" rows="2" maxlength="300"></textarea></label>'
     +'<div class="pk-hp" aria-hidden="true"><label>Leave this empty<input type="text" id="pk-hp" tabindex="-1" autocomplete="off"></label></div>'
     +'<label class="pk-consent"><input type="checkbox" id="pk-ok"><span>I agree that Nature&rsquo;s Nook may text me at this number about this order only. Message and data rates may apply. Reply STOP to opt out. See the <a href="/privacy/">privacy policy</a>.</span></label>'
     +'<p class="pk-msg" id="pk-msg" role="status"></p><button type="submit" class="pk-btn pk-submit" id="pk-go">Send pickup order</button></form>';
    body.querySelectorAll('.pk-qty button').forEach(function(b){ b.addEventListener('click',function(){
      var u=b.parentNode.getAttribute('data-u'), a=b.getAttribute('data-a'), l=cart[u]; if(!l) return;
      if(a==='+') l.qty=Math.min(C.maxQty,l.qty+1); else if(a==='-') l.qty=Math.max(1,l.qty-1); else { delete cart[u]; order=order.filter(function(x){return x!==u}); }
      syncFab(); var keep=body.querySelector('#pk-name')?{n:d.getElementById('pk-name').value,p:d.getElementById('pk-phone').value,t:d.getElementById('pk-note').value,c:d.getElementById('pk-ok').checked}:null;
      draw(); if(keep&&d.getElementById('pk-name')){ d.getElementById('pk-name').value=keep.n; d.getElementById('pk-phone').value=keep.p; d.getElementById('pk-note').value=keep.t; d.getElementById('pk-ok').checked=keep.c; }
      if(!order.length) syncFab();
    }); });
    var form=d.getElementById('pk-form'); if(form) form.addEventListener('submit',submit);
  }

  function submit(e){
    e.preventDefault();
    var msg=d.getElementById('pk-msg'), go=d.getElementById('pk-go');
    function err(t){ msg.className='pk-msg err'; msg.textContent=t; }
    var name=d.getElementById('pk-name').value.trim(), phone=d.getElementById('pk-phone').value.replace(/[^\d+]/g,''), digits=phone.replace(/\D/g,'');
    if(d.getElementById('pk-hp').value) return;                       // bots fill the hidden field
    if(!name) return err('Please enter your name.');
    if(digits.length<10||digits.length>11) return err('Please enter a 10-digit mobile number.');
    if(!d.getElementById('pk-ok').checked) return err('Please check the box to let us text you about this order.');
    if(!order.length) return err('Your order is empty.');
    var payload={name:name,phone:phone,note:d.getElementById('pk-note').value.trim(),consent:true,
      items:order.map(function(u){var l=cart[u];return {upc:u,brand:l.brand,name:l.name,variant:l.variant,qty:l.qty,price:l.price}})};
    go.disabled=true; msg.className='pk-msg'; msg.textContent='Sending…';
    fetch(C.endpoint,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(payload),redirect:'follow'})
      .then(function(r){return r.json()})
      .then(function(j){
        if(!j||!j.ok) throw new Error((j&&j.error)||'failed');
        cart={}; order=[]; syncFab(); draw({id:j.id,name:name});
      })
      .catch(function(){ go.disabled=false; err('We could not send that. Please try again, or call (208) 356-5284 and we will take your order.'); });
  }

  // product dialog hook: "Add to pickup order"
  window.nnPickupHook=function(i){
    var box=d.getElementById('pd-pickup'); if(!box) return;
    var u=String(i[6]), price=Number(i[5])||0;
    function paint(){
      var l=cart[u];
      box.innerHTML='<div class="pk-add">'+(l?'<span class="pk-in">In your pickup order ('+l.qty+')</span><button type="button" class="pk-link" id="pk-view">View order</button>':'<button type="button" class="btn" id="pk-addbtn">Add to pickup order</button>')+'</div>';
      var a=d.getElementById('pk-addbtn'), v=d.getElementById('pk-view');
      if(a) a.addEventListener('click',function(){
        if(order.length>=C.maxLines){ box.innerHTML='<p class="pk-fine">Your order is full. Please send it first, or call us.</p>'; return; }
        cart[u]={brand:i[1],name:i[2],variant:[i[3],(i[4]||'').split(' · ')[1]||''].filter(Boolean).join(', '),qty:1,price:price}; order.push(u); syncFab(); paint();
        var vb=d.getElementById('pk-view'); if(vb) vb.focus();
      });
      if(v) v.addEventListener('click',function(){ var p=d.getElementById('pd'); var cb=d.getElementById('pd-close'); if(cb) cb.click(); open(); });
    }
    paint();
  };
})();
</script>
