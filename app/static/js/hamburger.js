// hamburger.js - menu responsivo

document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.getElementById('hamburger-btn');
  const menu = document.getElementById('main-menu');
  if (!hamburger || !menu) return;

  hamburger.addEventListener('click', function () {
    menu.classList.toggle('open');
    hamburger.classList.toggle('active');
  });

  // Fecha o menu ao clicar fora
  document.addEventListener('click', function (e) {
    if (!menu.contains(e.target) && !hamburger.contains(e.target)) {
      menu.classList.remove('open');
      hamburger.classList.remove('active');
    }
  });
});
