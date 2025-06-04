function openProductModal(productId, productName, productSlug, productImage, article, height, width, depth, material, color, hardware, productPrice) {

    // Обработчик для кнопки "Описание"
    const showDescriptionButton = document.getElementById('showDescriptionButton');

    showDescriptionButton.addEventListener('click', () => {

        // Отображение модального окна описания товара
        document.getElementById('descriptionModal').style.display = 'block';

        // Закрытие модального окна описания по клику на крестик
        document.querySelector('.closeButtonDescription').addEventListener('click', () => {
            document.getElementById('descriptionModal').style.display = 'none';
        });

        // Закрытие модального окна описания кликом вне него
        window.addEventListener('click', (event) => {
            if (event.target == document.getElementById('descriptionModal')) {
                document.getElementById('descriptionModal').style.display = 'none';
            }
        });

        // Заполнение данных в модальном окне описания
        document.querySelector('.headerModalProductDescript h2').textContent = productName;
        document.getElementById('ProductArticle').innerHTML = 'Артикул: ' + article;
        document.getElementById('ProductHeight').innerHTML = 'Высота: ' + (height !== null ? height + ' м' : 'Не указано');
        document.getElementById('ProductWidth').innerHTML = 'Ширина: ' + (width !== null ? width + ' м' : 'Не указано');
        document.getElementById('ProductDepth').innerHTML = 'Глубина: ' + (depth !== null ? depth + ' м' : 'Не указано');
        document.getElementById('ProductMaterial').innerHTML = 'Материал: ' + (material !== null ? material : 'Не указано');
        document.getElementById('ProductColor').innerHTML = 'Цвет: ' + (color !== null ? color : 'Не указано');
        document.getElementById('ProductHardware').innerHTML = 'Фурнитура: ' + (hardware !== null ? hardware : 'Не указано');
        document.getElementById('ProductPrice').innerHTML = 'Цена: ' + (productPrice !== null ? productPrice + ' руб.' : 'Не указано');
    });

    // Заполнение данных в основном модальном окне
    document.getElementById('modalProductCategory').innerHTML = productName;
    document.getElementById('modalProductName').innerHTML = productName;
    document.querySelector('.modalImage').src = productImage;
    document.getElementById('modalProductArticle').innerHTML = 'Артикул: ' + article;
    document.getElementById('modalProductHeight').innerHTML = 'Высота: ' + (height !== null ? height + ' м' : 'Не указано');
    document.getElementById('modalProductWidth').innerHTML = 'Ширина: ' + (width !== null ? width + ' м' : 'Не указано');
    document.getElementById('modalProductDepth').innerHTML = 'Глубина: ' + (depth !== null ? depth + ' м' : 'Не указано');
    document.getElementById('modalProductMaterial').innerHTML = 'Материал: ' + (material !== null ? material : 'Не указано');
    document.getElementById('modalProductColor').innerHTML = 'Цвет: ' + (color !== null ? color : 'Не указано');
    document.getElementById('modalProductHardware').innerHTML = 'Фурнитура: ' + (hardware !== null ? hardware : 'Не указано');
    document.getElementById('modalProductPrice').innerHTML = 'Цена: ' + (productPrice !== null ? productPrice + ' руб.' : 'Не указано');

    // Получаем ссылки на кнопки
    const addToCartButton = document.querySelector('#productModal .addToCartButton');
    const favoriteButtonModal = document.querySelector('#productModal .favoriteButtonModal');

    if (addToCartButton) {
        addToCartButton.setAttribute('data-product-id', productId);
    }
    if (favoriteButtonModal) {
        favoriteButtonModal.setAttribute('data-product-id', productId);
    }

    // Отображение модального окна
    document.getElementById('productModal').style.display = 'block';

    // Закрытие модального окна по клику на крестик
    document.querySelector('.closeButtonCategory').addEventListener('click', () => {
        document.getElementById('productModal').style.display = 'none';
    });

    // Закрытие модального окна кликом вне него
    window.addEventListener('click', (event) => {
        if (event.target == document.getElementById('productModal')) {
            document.getElementById('productModal').style.display = 'none';
        }
    });
}