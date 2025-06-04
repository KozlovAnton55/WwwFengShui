document.addEventListener('DOMContentLoaded', function() {
  const burgerMenu = document.querySelector('.burgerMenu');
  const mobileMenu = document.querySelector('.mobileMenu');
  const closeButton = document.querySelector('.closeButton');

  burgerMenu.addEventListener('click', function() {
      mobileMenu.classList.add('open');
  });

  closeButton.addEventListener('click', function() {
      mobileMenu.classList.remove('open'); 
  });
});