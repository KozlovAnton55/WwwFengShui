document.addEventListener('DOMContentLoaded', function() {

    const favoritesModal = document.getElementById('favoritesModal');
    const overlay = document.createElement('div');
    overlay.className = 'favoritesModal-overlay';
    document.body.appendChild(overlay);

    const showFavoritesButton = document.getElementById('showFavorites');
    const showFavoritesModalIcon = document.getElementById('showFavoritesModal');
    const closeButton = document.querySelector('.closeButtonDescription');


    function showModal() {
        favoritesModal.style.display = 'block';
        overlay.style.display = 'block';
        document.body.style.overflow = 'hidden'; 
    }

    function hideModal() {
        favoritesModal.style.display = 'none'; 
        overlay.style.display = 'none'; 
        document.body.style.overflow = 'auto'; 
    }

    if (showFavoritesButton) {
        showFavoritesButton.addEventListener('click', function(event) {
            event.preventDefault();
            showModal();
        });
    }

    if (showFavoritesModalIcon) {
        showFavoritesModalIcon.addEventListener('click', function(event) {
            event.preventDefault();
            showModal();
        });
    }

    closeButton.addEventListener('click', hideModal);

    document.addEventListener('click', function(event) {
        if (event.target === overlay || !favoritesModal.contains(event.target)) {
            hideModal();
        }
    });


    // Обработчики для кнопок "Удалить" и "Добавить в корзину" (нужно добавить функциональность)
    favoritesModal.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-from-wishlist')) {
            console.log('Удалить из избранного');
        } else if (event.target.classList.contains('add-to-cart')) {
            console.log('Добавить в корзину');
        }
    });
});