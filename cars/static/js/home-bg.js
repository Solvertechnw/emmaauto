// Background video autoplay / fallback handler
(function(){
  function initBgVideo(){
    var video = document.getElementById('bg-video');
    var playBtn = document.getElementById('bg-play-button');
    var container = document.getElementById('bg-media');
    if(!video) return;
  var tapOverlay = document.getElementById('bg-tap-overlay');

  // DEBUG: force optimized file immediately (set true to force carp-720 test)
  // Set to false for normal behavior
  var FORCE_OPTIMIZED_DEBUG = false;
    window.homeBgDebugFlag = window.homeBgDebugFlag || {};
    window.homeBgDebugFlag.forced = FORCE_OPTIMIZED_DEBUG;
  if(FORCE_OPTIMIZED_DEBUG){
      try{
        var base = video.getAttribute('data-media-url') || '';
        var testUrl = base + 'carv-720.mp4';
        console.debug('[home-bg DEBUG] forcing optimized src:', testUrl);
        var srcEl = video.querySelector('source[type="video/mp4"]');
        if(srcEl){ srcEl.src = testUrl; video.load(); }
        // attempt playback immediately
        video.muted = true;
        var p = video.play();
        console.debug('[home-bg DEBUG] forced play() returned', p);
        if(p && p.then){
          p.then(function(){ console.debug('[home-bg DEBUG] forced play succeeded'); if(playBtn) playBtn.style.display='none'; })
            .catch(function(err){ console.debug('[home-bg DEBUG] forced play rejected', err); if(playBtn) playBtn.style.display='flex'; });
        }
      }catch(e){ console.debug('[home-bg DEBUG] forced play threw', e); }
      // still continue with regular checks in case forced attempt doesn't work
    }

    // Try to swap in optimized variants if available
    (function tryOptimized(){
      console.debug('[home-bg] init tryOptimized');
      var base = video.getAttribute('data-media-url') || '';
      console.debug('[home-bg] data-media-url=', base);
      if(!base) return;
      var nav = navigator;
      var effectiveType = (nav && nav.connection && nav.connection.effectiveType) || '';
      console.debug('[home-bg] network effectiveType=', effectiveType);
      // prefer 480 for slow networks, else 720
      var preferred = (effectiveType && effectiveType.indexOf('2g')!==-1) ? '480' : '720';
      var candidates = (preferred==='480') ? ['carv-480.mp4','carv-720.mp4'] : ['carv-720.mp4','carv-480.mp4'];
      console.debug('[home-bg] candidate order=', candidates);

      function head(url){
        console.debug('[home-bg] HEAD check', url);
        return fetch(url, { method: 'HEAD', cache: 'no-cache' }).then(function(r){
          console.debug('[home-bg] HEAD result', url, r.status);
          return r && (r.status>=200 && r.status<400);
        }).catch(function(err){ console.debug('[home-bg] HEAD error', url, err); return false; });
  }

      // check candidates sequentially and replace <source> first source if found
      (function checkNext(i){
        if(i>=candidates.length) return;
        var url = base + candidates[i];
        head(url).then(function(ok){
          console.debug('[home-bg] candidate', url, 'exists=', ok);
          if(ok){
            // set the first source to optimized mp4
            var srcEl = video.querySelector('source[type="video/mp4"]');
            if(srcEl){
              console.debug('[home-bg] applying optimized source', url);
              srcEl.src = url;
              video.load();
              // attempt to play the newly loaded optimized source
              try{
                var p = video.play();
                console.debug('[home-bg] play() returned', p);
                if(p && p.then){
                  p.then(function(){
                    console.debug('[home-bg] play() succeeded');
                    // hide play UI if successful
                    if(playBtn) playBtn.style.display = 'none';
                  }).catch(function(err){
                    console.debug('[home-bg] play() rejected', err);
                    // show UI if playback blocked
                    if(playBtn) playBtn.style.display = 'flex';
                  });
                }
              }catch(e){
                console.debug('[home-bg] play() threw', e);
                if(playBtn) playBtn.style.display = 'flex';
              }
            }
          } else {
            checkNext(i+1);
          }
        });
      })(0);
    })();

    function showPlayUI(){
      if(playBtn) playBtn.style.display = 'flex';
      if(tapOverlay){ tapOverlay.classList.add('show'); tapOverlay.setAttribute('aria-hidden','false'); tapOverlay.setAttribute('tabindex','0'); }
      if(video) try{ video.pause(); }catch(e){}
      container && container.classList && container.classList.add('bg-video-paused');
    }

    function hidePlayUI(){
      if (playBtn) playBtn.style.display = 'none';
      if (tapOverlay) { tapOverlay.classList.remove('show'); tapOverlay.setAttribute('aria-hidden','true'); tapOverlay.removeAttribute('tabindex'); }
      container.classList.remove('bg-video-paused');
    }

    var startPlayback = function(){
      try{ video.muted = true; }catch(e){}
      video.play().then(function(){ hidePlayUI(); }).catch(function(){ showPlayUI(); });
    };

    // tap overlay interaction: start playback and hide overlay
    if (tapOverlay){
      var startFromOverlay = function(e){
        e && e.preventDefault();
        try{ video.muted = true; }catch(e){}
        try{
          // reload sources to ensure currentSrc is updated
          try{ video.load(); }catch(_){ }
          var p = video.play();
          console.debug('[home-bg] overlay play called', p);
          // write to debug panel if present
          if(window._homeBgDebug) window._homeBgDebug.log('overlay play called, promise=' + (p ? 'present' : 'none'));
          if(p && p.then){
            p.then(function(){ hidePlayUI(); console.debug('[home-bg] overlay play succeeded'); }).catch(function(err){
              console.debug('[home-bg] overlay play rejected', err);
              if(window._homeBgDebug) window._homeBgDebug.log('overlay play rejected: ' + (err && err.name ? err.name : String(err)) );
              // allow manual play by showing controls
              try{ video.controls = true; }catch(_){ }
            });
          } else {
            // some older browsers may not return a Promise; check playback state shortly
            setTimeout(function(){
              var stillPaused = !!video.paused;
              console.debug('[home-bg] post-play paused?', stillPaused);
              if(window._homeBgDebug) window._homeBgDebug.log('post-play paused=' + stillPaused);
              if(!stillPaused){ hidePlayUI(); }
              else { try{ video.controls = true; }catch(_){ } }
            }, 250);
          }
        }catch(err){
          console.debug('[home-bg] overlay play threw', err);
          if(window._homeBgDebug) window._homeBgDebug.log('overlay play threw: ' + (err && err.name ? err.name : String(err)) );
          try{ video.controls = true; }catch(_){ }
        }
      };
      tapOverlay.addEventListener('click', startFromOverlay);
      tapOverlay.addEventListener('keydown', function(e){ if(e.key==='Enter' || e.key===' '){ startFromOverlay(e); } });
    }

    // --- Debug panel (visible on-screen for easier diagnosis) ---
    (function ensureDebugPanel(){
      if(window._homeBgDebug) return;
      var panel = document.createElement('div');
      panel.id = 'bg-debug-panel';
      panel.style.position = 'fixed';
      panel.style.right = '12px';
      panel.style.bottom = '12px';
      panel.style.zIndex = 9999;
      panel.style.maxWidth = '320px';
      panel.style.fontSize = '12px';
      panel.style.background = 'rgba(0,0,0,0.7)';
      panel.style.color = '#fff';
      panel.style.padding = '8px';
      panel.style.borderRadius = '6px';
      panel.style.fontFamily = 'Arial, sans-serif';
      panel.style.lineHeight = '1.2';
      panel.style.display = 'none';

      var header = document.createElement('div'); header.textContent = 'bg debug'; header.style.fontWeight='700'; header.style.marginBottom='6px'; panel.appendChild(header);
      var out = document.createElement('div'); out.id = 'bg-debug-out'; out.style.maxHeight='180px'; out.style.overflow='auto'; out.style.marginBottom='6px'; panel.appendChild(out);
      var btns = document.createElement('div');
      var showBtn = document.createElement('button'); showBtn.textContent='Show'; showBtn.style.marginRight='6px';
      var playBtnDbg = document.createElement('button'); playBtnDbg.textContent='Play'; playBtnDbg.style.marginRight='6px';
      var infoBtn = document.createElement('button'); infoBtn.textContent='Info';
      [showBtn, playBtnDbg, infoBtn].forEach(function(b){ b.style.fontSize='12px'; b.style.padding='4px 6px'; b.style.cursor='pointer'; b.style.marginTop='4px'; b.style.background='rgba(255,255,255,0.06)'; b.style.color='#fff'; b.style.border='1px solid rgba(255,255,255,0.08)'; b.style.borderRadius='4px'; });
      btns.appendChild(showBtn); btns.appendChild(playBtnDbg); btns.appendChild(infoBtn); panel.appendChild(btns);

      document.body.appendChild(panel);
      window._homeBgDebug = {
        panel: panel,
        out: out,
        visible: false,
        log: function(msg){ var d = document.createElement('div'); d.textContent = new Date().toLocaleTimeString() + ' ' + msg; out.insertBefore(d, out.firstChild); },
        show: function(){ panel.style.display='block'; this.visible = true; },
        hide: function(){ panel.style.display='none'; this.visible = false; }
      };

      showBtn.addEventListener('click', function(){ window._homeBgDebug.visible ? window._homeBgDebug.hide() : window._homeBgDebug.show(); });
      playBtnDbg.addEventListener('click', function(){ try{ video.muted = true; video.play().then(function(){ window._homeBgDebug.log('manual play then() ok'); }).catch(function(err){ window._homeBgDebug.log('manual play rejected: '+(err && err.name?err.name:err)); video.controls = true; }); }catch(e){ window._homeBgDebug.log('manual play threw: '+e); video.controls = true; }});
      infoBtn.addEventListener('click', function(){ try{ window._homeBgDebug.log('currentSrc: '+(video.currentSrc||'(none)')); window._homeBgDebug.log('paused: '+video.paused+' muted:'+video.muted+' readyState:'+video.readyState+' networkState:'+video.networkState); }catch(e){ window._homeBgDebug.log('info error: '+e); } });

      // auto-show the panel when user opens page so they can help debug
      window._homeBgDebug.show();
      // initial info
      try{ window._homeBgDebug.log('init currentSrc: '+(video.currentSrc||'(none)')); }catch(e){ }
    })();

    if(playBtn) playBtn.addEventListener('click', startPlayback, { once: true });

    var onFirstInteraction = function(){
      startPlayback();
      window.removeEventListener('touchstart', onFirstInteraction);
      window.removeEventListener('click', onFirstInteraction);
    };
    window.addEventListener('touchstart', onFirstInteraction, { passive: true });
    window.addEventListener('click', onFirstInteraction, { passive: true });
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initBgVideo);
  } else {
    initBgVideo();
  }
})();
