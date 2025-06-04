(function () { 

    // Функция для получения элементов (модальные окна и кнопки)
    function getBasketModal() { return document.getElementById("basketOfGoods"); }
    function getFavoritesModal() { return document.getElementById("favoritesModal"); }
    function getBasketBtn() { return document.querySelector(".goToTheHoppingCart"); }
    function getHeaderBasketIcon() { return document.querySelector(".basketWrapper a"); }
    function getFavoritesBtn() { return document.getElementById("showFavorites"); }
    function getProductModal() { return document.getElementById("productModal"); }

    // Функция для открытия модального окна
    function openModal(modal) {
        if (modal && modal.style) {
            modal.style.display = "block";
        }
    }

    // Функция для закрытия модального окна
    function closeModal(modal) {
        if (modal && modal.style) {
            modal.style.display = "none";
        }
    }

    // Функция открытия корзины по клику на иконку в header
    function setupHeaderBasketIcon() {
        const headerBasketIcon = getHeaderBasketIcon();
        if (headerBasketIcon) {
            headerBasketIcon.addEventListener("click", function (event) {
                event.preventDefault();
                const basketModal = getBasketModal();
                openModal(basketModal);
            });
        }
    }

    // Функция открытия корзины по клику на кнопку "Перейти в корзину"
    function setupBasketBtn() {
        const basketBtn = getBasketBtn();
        if (basketBtn) {
            basketBtn.onclick = function () {
                const basketModal = getBasketModal();
                openModal(basketModal);
            }
        }
    }

    // Функция открытия избранного по клику на кнопку "Посмотреть все"
    function setupFavoritesBtn() {
        const favoritesBtn = getFavoritesBtn();
        if (favoritesBtn) {
            favoritesBtn.onclick = function () {
                const favoritesModal = getFavoritesModal();
                openModal(favoritesModal);
            }
        }
    }

    // Функция по нахождению всех элементов с классом "close" (для всех модальных окон)
    function setupCloseButtons() {
        const closeButtons = document.querySelectorAll(".close, .basketCloseButton");
        closeButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                const modal = this.closest(".modal, .basketModal");
                if (modal) {
                    closeModal(modal);
                }
            });
        });
    }

    // Закрытие модальных окон при клике вне окна
    function setupModalCloseOnClickOutside() {
        window.addEventListener("click", function (event) {
            if (event.target.classList.contains('modal') || event.target.classList.contains('basketModal')) {
                closeModal(event.target);
            }
        });
    }

    // Функция для открытия корзины и избранного из модального окна товара
    function setupProductModalIcons() {
        const productModal = getProductModal();
        if (productModal) {
            const cartIcon = productModal.querySelector(".cart-icon");
            const wishlistIcon = productModal.querySelector(".wishlist-icon");

            if (cartIcon) {
                cartIcon.addEventListener("click", function (event) {
                    event.preventDefault();
                    const basketModal = getBasketModal();
                    openModal(basketModal);
                });
            }

            if (wishlistIcon) {
                wishlistIcon.addEventListener("click", function (event) {
                    event.preventDefault();
                    const favoritesModal = getFavoritesModal();
                    openModal(favoritesModal);
                });
            }
        }
    }

    // Инициализация
    function initialize() {
        setupHeaderBasketIcon();
        setupBasketBtn();
        setupFavoritesBtn();
        setupCloseButtons();
        setupModalCloseOnClickOutside();
        setupProductModalIcons();
    }

    document.addEventListener("DOMContentLoaded", initialize);

})();