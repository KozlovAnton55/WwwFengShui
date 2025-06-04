ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map('map', {
        center: [55.109299, 36.614356],
        zoom: 9
    }, {
        searchControlProvider: 'yandex#search'
    });

    var myGeoObjects = [];
    myGeoObjects[0] = new ymaps.GeoObject({
        geometry: {
            type: 'Point',
            coordinates: [55.116902, 36.593277]
        },
        properties: {
            iconContent: 'Feng Shui',
            hintContent: 'Подсказка для маркера'
        }
    }, {
        preset: 'islands#redStretchyIcon',
        draggable: false
    });

    myMap.geoObjects.add(myGeoObjects[0]);
}