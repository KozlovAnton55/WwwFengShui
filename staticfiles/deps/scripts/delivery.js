// Объект карты
let myMap;
// Координаты центра Обнинска
const CITY_CENTER_COORDINATES = [55.117082, 36.597014];
// Радиус 20 км в метрах
const DELIVERY_RADIUS_1 = 20000;
// Радиус 40 км в метрах
const DELIVERY_RADIUS_2 = 40000;
// Данные о ценах, полученные из API
let pricingData = {};

// Функция инициализации карты
function initMap() {
    ymaps.ready(init);
    function init() {
        myMap = new ymaps.Map('deliveryMap', {
            center: CITY_CENTER_COORDINATES,
            zoom: 10,
        });

        const circle1 = new ymaps.Circle(
            [CITY_CENTER_COORDINATES, DELIVERY_RADIUS_1],
            {
                fillColor: 'transparent',
                strokeColor: '#007bff',
                strokeOpacity: 1,
                strokeWidth: 2,
            }
        );

        const circle2 = new ymaps.Circle(
            [CITY_CENTER_COORDINATES, DELIVERY_RADIUS_2],
            {
                fillColor: 'transparent',
                strokeColor: '#007bff',
                strokeOpacity: 1,
                strokeWidth: 2,
            }
        );

        myMap.geoObjects.add(circle1).add(circle2);
    }
}

// Функция для получения данных о ценах из API
function fetchPricingData() {
    return fetch('/delivery/api/pricing/')
        .then((response) => response.json())
        .then((data) => {
            pricingData = {
                zone_1_price: parseFloat(data.zone_1_price),
                zone_2_price: parseFloat(data.zone_2_price),
                price_per_floor_with_lift: parseFloat(data.price_per_floor_with_lift),
                price_per_floor_without_lift: parseFloat(data.price_per_floor_without_lift),
                heavy_furniture_price: parseFloat(data.heavy_furniture_price),
                light_furniture_price: parseFloat(data.light_furniture_price),
            };
        })
        .catch((error) => {
           
        });
}

// Функция для получения данных профиля доставки из атрибутов data-*
function getDeliveryProfileFromDOM() {
    const personalAccountSection = document.getElementById('personalAccount');
    if (!personalAccountSection) {
        return null;
    }
    const city = personalAccountSection.dataset.deliveryCity;
    return city;
}

// Функция расчета стоимости доставки
function calculateDelivery() {
    const deliveryProfile = getDeliveryProfileFromDOM();
  

    let city;
    if (deliveryProfile) {
        city = deliveryProfile;
       
    } else {
        city = document.getElementById('city').value;
      
    }

    if (!city) {
       
        return;
    }

    if (!pricingData || Object.keys(pricingData).length === 0) {
      
        return;
    }

    // Получаем тип подъема (с этажом или без)
    const floorType = document.querySelector('input[name="floorType"]:checked')?.value;
    if (!floorType) {
        
        return;
    }

    // Получаем этаж, если выбран "с этажом"
    let floor = 0; 
    if (floorType === 'withFloor') {
        floor = parseInt(document.getElementById('floor').value);
        if (isNaN(floor) || floor <= 0) {
            
            return;
        }
    }

    // Получаем информацию о наличии лифта
    const hasLift = document.querySelector('input[name="hasLift"]:checked')?.value;
    if (!hasLift) {
      
        return;
    }

    // Получаем выбранную категорию мебели
    const category = document.getElementById('category').value;

    // Геокодирование города
    ymaps.geocode(city)
        .then(function (res) {
            const firstGeoObject = res.geoObjects.get(0);
            if (!firstGeoObject) {
                
                return;
            }
            const cityCoordinates = firstGeoObject.geometry.getCoordinates();

            // Расстояние до города
            const distance = ymaps.coordSystem.geo.getDistance(
                CITY_CENTER_COORDINATES,
                cityCoordinates
            );

            // Расчет стоимости доставки
            let deliveryCost = 0;

            // Расчет базовой стоимости в зависимости от расстояния
            if (distance <= DELIVERY_RADIUS_1) {
                deliveryCost = pricingData.zone_1_price;
            } else if (distance <= DELIVERY_RADIUS_2) {
                deliveryCost = pricingData.zone_2_price;
            } else {
                
                return;
            }

            // Расчет стоимости подъема на этаж
            if (floorType === 'withFloor' && floor > 0) {
                let floorCost = 0;
                if (hasLift === 'yes') {
                    floorCost = pricingData.price_per_floor_with_lift * floor;
                } else {
                    floorCost = pricingData.price_per_floor_without_lift * floor;
                }
                deliveryCost += floorCost;
            }

            // Расчет стоимости в зависимости от категории мебели
            let categoryCost = 0;
            if (['sofas', 'designer_furniture', 'dressers', 'bathroom_furniture', 'children_furniture', 'office_furniture', 'bedroom_furniture', 'living_room_furniture', 'tables', 'kitchen_furniture', 'halls'].includes(category)) {
                categoryCost = pricingData.heavy_furniture_price;
            } else if (['rugs', 'shelves', 'chairs'].includes(category)) {
                categoryCost = pricingData.light_furniture_price;
            } else {
                
                return;
            }
            deliveryCost += categoryCost;

            
            showModal(deliveryCost);
        })
        .catch((err) => {
            
        });
}

// Получаем модальное окно
const modal = document.getElementById('deliveryModal');

// Получаем элемент <span>, который закрывает модальное окно
const span = document.getElementsByClassName('close')[0];

// Функция для отображения модального окна
function showModal(cost) {
    document.getElementById('deliveryCostText').innerText =
        'Предварительная стоимость доставки: ' + cost.toFixed(2) + ' рублей.';
    modal.style.display = 'block';
}

// Закрываем модальное окно при клике на крестик
span.onclick = function () {
    modal.style.display = 'none';
};

// Закрываем модальное окно при клике вне его области
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

// Инициализация формы
function initForm() {
    // Обработчик для radio button "С подъемом" (включаем/выключаем поле этажа)
    const floorTypeRadios = document.querySelectorAll('input[name="floorType"]');
    floorTypeRadios.forEach((radio) => {
        radio.addEventListener('change', function () {
            const floorInput = document.getElementById('floor');
            floorInput.disabled = this.value === 'noFloor';
            if (this.value === 'noFloor') {
                floorInput.value = '';
            }
        });
    });

    // Обработчик для кнопки "Рассчитать стоимость"
    const calculateButton = document.querySelector(
        '#deliveryForm > button[type="button"]'
    );
    if (calculateButton) {
        calculateButton.addEventListener('click', calculateDelivery);
    }
}

// Инициализация карты и формы
ymaps.ready(initMap);
fetchPricingData().then(() => {
    initForm();
});

