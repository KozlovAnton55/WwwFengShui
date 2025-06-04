(function () { 

    // Функция для получения URL из атрибута data-* элемента body
    function getDataUrl(attributeName) {
        const body = document.body;
        if (body && body.dataset && body.dataset[attributeName]) {
            return body.dataset[attributeName];
        }
        console.warn(`Атрибут data-${attributeName} не найден в <body>.`);
        return null; // Или значение по умолчанию, например, пустая строка
    }

    // Получаем URL из шаблона с помощью функции getDataUrl
    const cartDataUrl = getDataUrl('cartDataUrl');
    const wishlistDataUrl = getDataUrl('wishlistDataUrl');
    const currentOrdersUrl = getDataUrl('currentOrdersUrl');
    const processOrderUrl = getDataUrl('processOrderUrl');

    // Функция для отображения модального окна
    function showModal(message, options = {}) {
        const modalContainer = document.getElementById("modalContainer");
        const modalContent = document.getElementById("modalContent");
        const modalYesButton = document.getElementById("modalYes");
        const modalNoButton = document.getElementById("modalNo");

        modalContent.textContent = message;
        modalContainer.style.display = "flex";

        modalYesButton.style.display = "none";
        modalNoButton.style.display = "none";

        if (options.showButtons) {
            modalYesButton.style.display = "inline-block";
            modalNoButton.style.display = "inline-block";

            modalYesButton.onclick = function() {
                options.onYes();
                modalContainer.style.display = "none";
            };

            modalNoButton.onclick = function() {
                options.onNo();
                modalContainer.style.display = "none";
            };
        } else {
            modalYesButton.style.display = "inline-block";
            modalYesButton.textContent = "OK"; 
            modalYesButton.onclick = function() {
                modalContainer.style.display = "none";
            };
        }
    }

    // Функция для получения данных о корзине
    function getCartData() {
        if (!cartDataUrl) return;
    
        return fetch(cartDataUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const basketOfGoodsCount = document.getElementById("BasketOfGoodsCount");
                const totalPriceElement = document.getElementById("totalPrice");
                const cartItemsContainer = document.getElementById("cartItemsContainer");
    
                if (basketOfGoodsCount) {
                    basketOfGoodsCount.textContent = data.cart_items_count;
                }
                if (totalPriceElement) {
                    totalPriceElement.textContent = data.total_price;
                }
    
                if (cartItemsContainer) {
                    cartItemsContainer.innerHTML = "";
    
                    if (data.cart_items_count === 0) {
                        const emptyCartMessage = document.createElement("p");
                        emptyCartMessage.id = "emptyCartMessage";
                        emptyCartMessage.textContent = "Корзина пуста.";
                        cartItemsContainer.appendChild(emptyCartMessage);
                    } else {
                        // Заполняем содержимое корзины
                        data.cart_items.forEach(item => {
                            const itemDiv = document.createElement("div");
                            itemDiv.classList.add("cart-item");
                            itemDiv.style.display = 'flex';
                            itemDiv.style.gap = '60px';
                            itemDiv.style.alignItems = 'center';
    
                            const column1 = document.createElement("div");
                            column1.classList.add("cart-item-column");
                            column1.style.display = 'flex';
                            column1.style.flexDirection = 'column';
                            column1.style.alignItems = 'start';
    
                            const column2 = document.createElement("div");
                            column2.classList.add("cart-item-column");
                            column2.style.display = 'flex';
                            column2.style.flexDirection = 'column';
    
                            // -- Формируем контент для первой колонки --
                            const name = document.createElement("h4");
                            name.textContent = item.product.name;
                            column1.appendChild(name);
    
                            const image = document.createElement("img");
                            image.src = item.product.image;
                            image.alt = item.product.name;
                            column1.appendChild(image);
    
                            const removeButton = document.createElement("button");
                            removeButton.textContent = "Удалить";
                            removeButton.classList.add("remove-from-cart");
                            removeButton.dataset.productId = item.product.id;
                            removeButton.addEventListener("click", function () {
                                const productId = this.dataset.productId;
                                showModal("Вы действительно хотите удалить этот товар?", {
                                    showButtons: true,
                                    onYes: () => {
                                        removeFromCart(productId);
                                    },
                                    onNo: () => {
                                        
                                    }
                                });
                            });
                            column1.appendChild(removeButton);
    
                            // -- Формируем контент для второй колонки --
                            const price = document.createElement("p");
                            price.textContent = `Цена: ${item.product.price} руб.`;
                            column2.appendChild(price);
    
                            // -- Создаем элементы управления для изменения количества --
                            const quantityWrapper = document.createElement("div");
                            quantityWrapper.classList.add("quantity-wrapper");  // Добавлен класс
    
                            const decreaseButton = document.createElement("button");
                            decreaseButton.textContent = "-";
                            decreaseButton.classList.add("quantity-button", "decrease-quantity"); // Добавлены классы
                            decreaseButton.dataset.productId = item.product.id;
    
                            const quantityDisplay = document.createElement("span");
                            quantityDisplay.textContent = item.quantity;
                            quantityDisplay.classList.add("quantity-display"); // Добавлен класс
    
                            const increaseButton = document.createElement("button");
                            increaseButton.textContent = "+";
                            increaseButton.classList.add("quantity-button", "increase-quantity"); // Добавлены классы
                            increaseButton.dataset.productId = item.product.id;
    
                            quantityWrapper.appendChild(decreaseButton);
                            quantityWrapper.appendChild(quantityDisplay);
                            quantityWrapper.appendChild(increaseButton);
                            column2.appendChild(quantityWrapper);
    
                            itemDiv.appendChild(column1);
                            itemDiv.appendChild(column2);
                            cartItemsContainer.appendChild(itemDiv);
                        });
    
                     
                        addQuantityChangeListeners(); 
                    }
                }
    
                // Получаем элементы для отображения информации о доставке
                const deliveryAddressElement = document.querySelector('#checkoutModal #delivery_address_info');
                const deliveryCostInfoElement = document.querySelector('#checkoutModal #delivery_cost_info');
                const totalOrderCostInfoElement = document.getElementById('total_order_cost_info'); //  Использовать id из base.html
                // Проверка на наличие элементов
                if (deliveryAddressElement) {
                    deliveryAddressElement.textContent = data.delivery_address || "Адрес доставки не указан";
                }
                // Рассчитываем общую стоимость
                if (totalPriceElement && totalOrderCostInfoElement && deliveryCostInfoElement) {
                    
                    totalOrderCostInfoElement.textContent = data.total_order_cost + " руб."; // Общая стоимость
                }
    
                return data;
            })
            .catch(error => {
                console.error("Ошибка при получении данных корзины:", error);
                return null;
            });
    }

    // Функция для удаления товара из корзины
    function removeFromCart(productId) {
        fetch(`/cartWishlistOrders/remove_from_cart/${productId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    getCartData();
                } else {
                    showModal("Ошибка при удалении товара из корзины.");
                }
            });
    }

    // Функция для добавления обработчиков событий на кнопки +/-
    function addQuantityChangeListeners() {
        document.querySelectorAll(".increase-quantity").forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.dataset.productId;

                const quantityWrapper = this.closest('.quantity-wrapper'); // Используем closest
                const quantityDisplay = quantityWrapper.querySelector(".quantity-display"); // Ищем quantityDisplay внутри quantityWrapper

                if (!quantityDisplay) {
                    console.error("quantityDisplay not found");
                    return;
                }

                let quantity = parseInt(quantityDisplay.textContent);
                quantity++;
                updateCartItemQuantity(productId, quantity);
            });
        });

        document.querySelectorAll(".decrease-quantity").forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.dataset.productId;

                const quantityWrapper = this.closest('.quantity-wrapper'); // Используем closest
                const quantityDisplay = quantityWrapper.querySelector(".quantity-display"); // Ищем quantityDisplay внутри quantityWrapper
                if (!quantityDisplay) {
                    console.error("quantityDisplay not found");
                    return;
                }

                let quantity = parseInt(quantityDisplay.textContent);
                if (quantity > 1) {
                    quantity--;
                    updateCartItemQuantity(productId, quantity);
                }
            });
        });
    }

    // Функция для обновления количества товара в корзине
    function updateCartItemQuantity(productId, quantity) {
        //  Добавьте проверку, что quantity является числом и больше 0.
        if (isNaN(quantity) || quantity <= 0) {
            console.error("Недопустимое количество:", quantity);
            return;
        }

        fetch(`/cartWishlistOrders/update_cart_item_quantity/${productId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: `quantity=${quantity}`
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    getCartData(); // Обновляем корзину
                } else {
                    showModal("Ошибка при обновлении количества товара.");
                }
            })
            .catch(error => {
                console.error("Ошибка при обновлении количества:", error);
                showModal("Произошла ошибка при обновлении количества товара.");
            });
    }

    // Функция для получения данных об избранном
    function getWishlistData() {
            if (!wishlistDataUrl) return;
    
            fetch(wishlistDataUrl)
                .then(response => response.json())
                .then(data => {
                    const favoritesCount = document.getElementById("favoritesCount");
                    const wishlistItemsContainer = document.getElementById("wishlist-items");
                    const wishlistTemplate = document.getElementById("wishlist-item-template"); // Получаем элемент, а не template
    
                    if (favoritesCount) {
                        favoritesCount.textContent = data.wishlist_items_count;
                    }
    
                    if (wishlistItemsContainer) {
                        wishlistItemsContainer.innerHTML = ""; // Очищаем контейнер
    
                        if (data.wishlist_items_count === 0) {
                            const emptyMessage = document.createElement("p");
                            emptyMessage.textContent = "Список избранного пуст.";
                            wishlistItemsContainer.appendChild(emptyMessage);
                        } else {
                            data.wishlist_items.forEach(item => {
                                // Клонируем элемент, а не template.content
                                const itemDiv = wishlistTemplate.cloneNode(true);
                                itemDiv.classList.remove("wishlist-item-hidden"); // Делаем элемент видимым
    
                                // Заполняем данные
                                const image = itemDiv.querySelector("img");
                                image.src = item.product.image;
                                image.alt = item.product.name;
    
                                const link = itemDiv.querySelector("h3 a"); // Исправленный селектор
                                link.href = `/product/${item.product.id}/`; // Устанавливаем URL карточки товара
                                link.textContent = item.product.name;
    
                                const price = itemDiv.querySelector(".price");
                                price.textContent = `${item.product.price} руб.`;
    
                                // Заполняем data-product-id для кнопок
                                const addToCartButton = itemDiv.querySelector(".add-to-cart-from-wishlist");
                                addToCartButton.dataset.productId = item.product.id;
    
                                const removeButton = itemDiv.querySelector(".remove-from-wishlist");
                                removeButton.dataset.productId = item.product.id;
                                removeButton.addEventListener("click", function () {
                                    const productId = this.dataset.productId;
                                    // Подтверждение удаления через модальное окно
                                    showModal("Вы действительно хотите удалить этот товар из избранного?", {
                                        showButtons: true,
                                        onYes: () => {
                                            removeFromWishlist(productId);
                                        },
                                        onNo: () => {
                                            // Ничего не делаем, просто закрываем окно
                                        }
                                    });
                                });
    
                                // Добавляем в контейнер
                                wishlistItemsContainer.appendChild(itemDiv);
                            });
                        }
                    }
                })
                .catch(error => {
                    console.error("Ошибка при получении данных избранного:", error);
                });
    }
    
    // Функция для удаления товара из избранного
    function removeFromWishlist(productId) {
            fetch(`/cartWishlistOrders/remove_from_wishlist/${productId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        // Находим элемент по ID или классу и удаляем его из DOM
                        const wishlistItem = document.querySelector(`.wishlist-item[data-product-id="${productId}"]`); // Правильный селектор!
                        if (wishlistItem) {
                            wishlistItem.remove();
                        }
    
                        // Обновляем счетчик избранного
                        getWishlistData();
    
                        // Проверяем, не пуст ли список, и показываем сообщение, если пуст
                        const wishlistItemsContainer = document.getElementById("wishlist-items");
                        if (wishlistItemsContainer && wishlistItemsContainer.children.length === 0) {
                            const emptyMessage = document.createElement("p");
                            emptyMessage.textContent = "Список избранного пуст.";
                            wishlistItemsContainer.appendChild(emptyMessage);
                        }
    
                    } else {
                        showModal("Ошибка при удалении товара из избранного."); // Модальное окно
                    }
                });
    }

    // Функция для добавления товара в корзину
    function addToCart(productId, removeFromWishlistAfterAdd = false) {
            fetch(`/cartWishlistOrders/add_to_cart/${productId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === "success") {
                        getCartData();
                        showModal("Товар добавлен в корзину!");
                        if (removeFromWishlistAfterAdd) {
                            removeFromWishlist(productId);
                        }
                    } else {
                        showModal("Ошибка при добавлении товара в корзину: " + data.message); // Модальное окно
                    }
                })
                .catch(error => {
                    console.error("Ошибка при добавлении в корзину:", error);
                    showModal("Произошла ошибка при добавлении товара в корзину. Пожалуйста, попробуйте позже."); // Модальное окно
                });
    }
    
    // Функция для добавления товара в избранное
    function addToWishlist(productId) {
            fetch(`/cartWishlistOrders/add_to_wishlist/${productId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === "success") {
                        getWishlistData();
                        showModal("Товар добавлен в избранное!"); // Модальное окно
                    } else {
                        showModal("Ошибка при добавлении товара в избранное: " + data.message); // Модальное окно
                    }
                })
                .catch(error => {
                    console.error("Ошибка при добавлении в избранное:", error);
                    showModal("Произошла ошибка при добавлении товара в избранное. Пожалуйста, попробуйте позже."); // Модальное окно
                });
    }
    
    // Делегирование событий
    function setupEventListeners() {
            document.addEventListener("click", function (event) {
                // Добавление в корзину
                if (event.target.classList.contains("addToCartButton") ||
                    event.target.classList.contains("addToCartProduct")) { // Убрали add-to-cart-from-wishlist отсюда
                    const productId = event.target.dataset.productId;
                    if (productId) {
                        addToCart(productId); // Вызываем просто addToCart, удалять из избранного не нужно, т.к. это не из модалки избранного
                    }
                }
                // Добавление в корзину из модалки избранного
                if (event.target.classList.contains("add-to-cart-from-wishlist")) {
                    const productId = event.target.dataset.productId;
                    if (productId) {
                        addToCart(productId, true); // Вызываем addToCart с параметром true, чтобы удалить из избранного
                    }
                }
    
                // Добавление в избранное
                if (event.target.classList.contains("favoriteButtonModal") ||
                    event.target.classList.contains("favoriteButtonProduct")) {
                    const productId = event.target.dataset.productId;
                    if (productId) {
                        addToWishlist(productId);
                    }
                }
            });
    }

    // Получение текущих заказов
    function getCurrentOrders() {
        if (!currentOrdersUrl) return;
    
        fetch(currentOrdersUrl)
            .then(response => response.json())
            .then(data => {
                const ordersList = document.getElementById("currentOrdersList");
                if (ordersList) {
                    ordersList.innerHTML = "";
    
                    data.orders.forEach(order => {
                        const orderDiv = document.createElement("div");
                        orderDiv.innerHTML = `
                            <div class="currentOrdersDescription">
                                <div class="currentOrdersStatus">
                                    <h4>Статус</h4>
                                    <span class="status">${order.status}</span>
                                </div>
                                <div class="currentOrdersNumber">
                                    <h4>Номер заказа</h4>
                                    <span class="number">${order.order_number}</span>
                                </div>
                                <div class="orderCreationDate">
                                    <h4>Дата создания</h4>
                                    <span class="Date">${order.created_at}</span>
                                </div>
                                <div class="orderDeliveryDate">
                                    <h4>Адрес</h4>
                                    <span>${order.delivery_address}</span>
                                </div>
                                <div class="theCostOfTheOrder">
                                    <h4>Стоимость</h4>
                                    <span class="costOrder">${order.total_order_cost} руб.</span>  <! --  изменили -->
                                </div>
                            </div>
                        `;
                        ordersList.appendChild(orderDiv);
                    });
                }
            })
            .catch(error => {
                console.error("Ошибка при получении текущих заказов:", error);
            });
    }

    // Функция для закрытия сообщения об успехе/ошибке
    function closeMessage() {
    const messageContainer = document.getElementById("reviewMessageContainer");
    if (messageContainer) {
        messageContainer.style.display = 'none';
    }
    }
    
    // Добавляем обработчик для кнопки "OK"
    function setupCloseReviewMessageButton() {
            var closeReviewMessageButton = document.getElementById("closeReviewMessage");
            if (closeReviewMessageButton) {
                closeReviewMessageButton.addEventListener("click", closeMessage);
            }
    }

    // Оформление заказа
    function setupCheckoutButton() {
        const checkoutButton = document.getElementById("checkoutButton");
        if (checkoutButton) {
            checkoutButton.addEventListener("click", function (event) {
                //  Добавляем проверку и сообщение здесь
                getCartData().then(cartData => {
                    if (!cartData || cartData.cart_items_count === 0) {
                        showModal("Ваша корзина пуста. Пожалуйста, добавьте товары в корзину.");
                    } else {
                        // Открываем окно оформления заказа (если нужно)
                        const checkoutModal = document.getElementById("checkoutModal");
                        if (checkoutModal) {
                            checkoutModal.style.display = "block";
                            // Вызываем функцию обновления данных о доставке
                            updateCheckoutModal(cartData);
                        }
                    }
                });
            });
        }
    }

    // Функция для обновления модального окна оформления заказа
    function updateCheckoutModal(cartData) {
        const checkoutMessageTextarea = document.getElementById('checkoutMessage'); // Получаем textarea
    
        let message = ""; // Создаем пустую строку для сообщения
    
        if (cartData.delivery_address) {
            message += "Адрес доставки: " + cartData.delivery_address + "\n";
        } else {
            message += "Адрес доставки: Не указан\n";
        }
    
        if (cartData.delivery_cost && cartData.delivery_cost !== "Не рассчитано" && cartData.delivery_cost !== "Ошибка") {
            message += "Стоимость доставки: " + cartData.delivery_cost + " руб.\n";
        } else {
            message += "Стоимость доставки: Не рассчитана\n";
        }
    
        if (cartData.total_order_cost) {
            message += "Общая стоимость заказа: " + cartData.total_order_cost + " руб.\n";
        }
    
        if (checkoutMessageTextarea) {
            checkoutMessageTextarea.value = message; // Записываем сформированное сообщение в textarea
        }
    }
    
    function setupCheckoutForm() {
        const checkoutForm = document.getElementById("checkoutForm");
        if (checkoutForm) {
            checkoutForm.addEventListener("submit", function (event) {
                event.preventDefault();
                const deliveryAddress = document.getElementById("checkoutMessage").value; //  <---  Важно!
    
                getCartData().then(cartData => {
                    if (!cartData || cartData.cart_items_count === 0) {
                        showModal("Ваша корзина пуста. Пожалуйста, добавьте товары в корзину.");
                        const checkoutModal = document.getElementById("checkoutModal");
                        if (checkoutModal) {
                            checkoutModal.style.display = "none";
                        }
                    } else {
                        fetch(processOrderUrl, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/x-www-form-urlencoded",
                                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                            },
                            body: `delivery_address=${encodeURIComponent(deliveryAddress)}`
                        })
                            .then(response => response.json())
                            .then(data => {
                                // Закрываем окно оформления заказа
                                const checkoutModal = document.getElementById("checkoutModal");
                                if (checkoutModal) {
                                    checkoutModal.style.display = "none";
                                }
                                if (data.status === "success") {
                                    showModal(`Заказ успешно оформлен! Номер вашего заказа: ${data.order_number}`); // Модальное окно
                                    getCurrentOrders();
                                    getCartData();
                                } else {
                                    showModal("Произошла ошибка при оформлении заказа."); // Модальное окно
                                }
                            });
                    }
                });
            });
        }
    }

    // Функция проверки авторизации пользователя (проверка наличия куки csrftoken)
    function isUserAuthenticated() {
        return document.cookie.includes('csrftoken=') && document.querySelector('.loggedInUser') !== null;
    }

    // Функция для управления модальным окном редактирования данных пользователя
    function setupPersonalDataModal() {
        const showPersonalDataButton = document.getElementById('showPersonalData');
        const editPersonalDataModal = document.getElementById('editPersonalDataModal');
        const closeModalButton = editPersonalDataModal.querySelector('.close');
        const passwordField = document.getElementById('editPassword');
    
        showPersonalDataButton.addEventListener('click', function(event) {
            event.preventDefault();
            // Устанавливаем пароль в читаемом виде
            passwordField.type = 'text';
            editPersonalDataModal.style.display = 'flex';
        });
    
        closeModalButton.addEventListener('click', function() {
            // Возвращаем тип поля пароля обратно в password
            passwordField.type = 'password';
            editPersonalDataModal.style.display = 'none';
        });
    
        window.addEventListener('click', function(event) {
            if (event.target === editPersonalDataModal) {
                passwordField.type = 'password';
                editPersonalDataModal.style.display = 'none';
            }
        });
    }

    // Модальное окно профиля доставки
    function setupDeliveryProfileModal() {
        const deliveryProfilesButton = document.querySelector('.deliveryProfiles .toChange');
        const editDeliveryProfileModal = document.getElementById('editDeliveryProfileModal');
        const deliveryProfileCloseButton = editDeliveryProfileModal.querySelector('.close');
        const editCity = document.querySelector('#editCity');  // Получаем элемент поля Город
        const editFloor = document.querySelector('#editFloor');
        const needsElevatorInput = document.querySelector('#editNeedsElevator');
        const hasLiftInput = document.querySelector('#editHasLift'); //  Получаем элемент "Наличие лифта"
        const deliveryCostSpan = document.getElementById('delivery_cost');
    
    
        if (deliveryProfilesButton && editDeliveryProfileModal && deliveryProfileCloseButton && editCity && deliveryCostSpan && editFloor && needsElevatorInput && hasLiftInput) {
            // Открываем модальное окно только при клике на кнопку "Изменить"
            deliveryProfilesButton.addEventListener('click', function(event) {
                event.preventDefault(); // Предотвращаем переход по ссылке
                editDeliveryProfileModal.style.display = 'block';
            });
    
            deliveryProfileCloseButton.addEventListener('click', function() {
                editDeliveryProfileModal.style.display = 'none';
            });
    
            //  Добавляем обработчик события для изменения города
            editCity.addEventListener('change', function() {
                const city = this.value; // Получаем новый город
                const floor = editFloor.value;
                const needsElevator = needsElevatorInput.checked;
                const hasLift = hasLiftInput.checked;
                fetchAndDisplayDeliveryCost(city, floor, needsElevator, hasLift, deliveryCostSpan); // Вызываем функцию для расчета стоимости
            });
    
            window.addEventListener('click', function(event) {
                if (event.target === editDeliveryProfileModal) {
                    editDeliveryProfileModal.style.display = 'none';
                }
            });
        } else {
            console.error('Не удалось найти элементы для модального окна профиля доставки.');
        }
    }

    // Инициализация
    function initialize() {
        setupEventListeners();
        if (isUserAuthenticated()) {
            getCartData();
            getWishlistData();
            getCurrentOrders();
            if (document.getElementById('editPersonalDataModal')) {
                setupPersonalDataModal();
            }
            if (document.querySelector('.deliveryProfiles .toChange')) {
                setupDeliveryProfileModal();
            }
        }
        setupCloseReviewMessageButton();
        setupCheckoutButton();
        setupCheckoutForm();
    }

    
    document.addEventListener("DOMContentLoaded", initialize);

})();