// site.js - hamburger, smooth scroll, active link, and mouse parallax

document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('main-nav');

  // hamburger toggle for mobile
  hamburger?.addEventListener('click', function () {
    const open = nav.classList.toggle('open');
    this.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Smooth scroll for internal anchors (#)
  document.querySelectorAll('a[href^="#"]').forEach(a=>{
    a.addEventListener('click', function(e){
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({behavior:'smooth', block:'start'});
        if (nav.classList.contains('open')) nav.classList.remove('open');
      }
    });
  });

  // highlight nav link based on scroll position
  const sections = Array.from(document.querySelectorAll('section[id]'));
  function onScroll(){
    const scroll = window.scrollY + 140;
    let current = sections.find(s => s.offsetTop <= scroll && s.offsetTop + s.offsetHeight > scroll);
    document.querySelectorAll('.nav-link').forEach(link=>{
      link.classList.remove('active');
      if (current){
        const id = current.id;
        if (link.getAttribute('href') && link.getAttribute('href').includes(`#${id}`)) link.classList.add('active');
      }
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  // Mouse parallax for planets (subtle)
  const universe = document.getElementById('universe');
  if (universe){
    // select planets by class 'planet' (your homepage script creates them)
    document.addEventListener('mousemove', function(e){
      const cx = window.innerWidth / 2;
      const cy = window.innerHeight / 2;
      const dx = (e.clientX - cx) / cx;
      const dy = (e.clientY - cy) / cy;
      const planets = universe.querySelectorAll('.planet');
      planets.forEach((pl, i) => {
        // different intensity per planet
        const intensity = 6 + (i * 4);
        pl.style.transform = `translate3d(${dx * intensity}px, ${dy * intensity}px, 0)`;
      });
    }, {passive: true});
  }

  // small performance: reduce animations when user prefers reduced-motion
  const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (mq.matches){
    document.querySelectorAll('.planet, .star').forEach(el => el.style.animation = 'none');
  }
});
