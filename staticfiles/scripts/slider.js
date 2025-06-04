document.addEventListener('DOMContentLoaded', function() {
    const sliderWrapper = document.querySelector('.sliderWrapp');
    const slides = document.querySelectorAll('.slider');
    const sliderIndicators = document.querySelector('.sliderIndicators');
    const slideCount = slides.length;
    let currentIndex = 0;
    let intervalId;

    // Создаем и добавляем индикаторы
    for (let i = 0; i < slideCount; i++) {
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'sliderIndicator';
        radio.value = i;
        radio.id = `slide-${i}`;
        radio.addEventListener('change', () => goToSlide(i)); // Используем лямбда-функцию
        sliderIndicators.appendChild(radio);
    }
    sliderIndicators.querySelector('input[type="radio"]').checked = true; // Первый активен

    // Функция перехода к слайду

    const goToSlide = (index) => {
        currentIndex = index;
        sliderWrapper.style.transform = `translateX(-${currentIndex * 100}%)`; // Шаблонная строка
        sliderIndicators.querySelectorAll('input[type="radio"]').forEach(radio => radio.checked = false);
        document.getElementById(`slide-${currentIndex}`).checked = true;
    };

    // Автоматическая прокрутка
    
    const startSlider = () => {
        intervalId = setInterval(() => { // Лямбда для краткости
            currentIndex = (currentIndex + 1) % slideCount; // Упрощенная логика "бесконечности"
            goToSlide(currentIndex);
        }, 3000);
    };

    const stopSlider = () => clearInterval(intervalId);

    // Запуск и остановка при наведении
    startSlider();
    sliderWrapper.addEventListener('mouseenter', stopSlider);
    sliderWrapper.addEventListener('mouseleave', startSlider);
});