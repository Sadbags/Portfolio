document.addEventListener('DOMContentLoaded', function() {
  const mobileMenuButton = document.getElementById('mobile-menu');
  const navbarMenu = document.getElementById('navbar__menu');

  mobileMenuButton.addEventListener('click', function() {
    navbarMenu.classList.toggle('active');
  });
});