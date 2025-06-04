document.addEventListener('DOMContentLoaded', function() {
    // Элементы для модального окна авторизации
    const authModal = document.getElementById('authorisationModal');
    const authOpenButtons = document.querySelectorAll('.loginButton');
    const authCloseButton = authModal ? authModal.querySelector('.close') : null;
    const authForm = authModal ? document.getElementById('authorisationModalForm') : null; 

    // Элементы для модального окна регистрации
    const registerModal = document.getElementById('registrationModal');
    const registerOpenButtons = document.querySelectorAll('.registerButton');
    const registerCloseButton = registerModal ? registerModal.querySelector('.close') : null;
    const registerForm = registerModal ? document.getElementById('registrationModalForm') : null; 

    // Функция открытия модального окна
    function openModal(modal) {
        modal.style.display = 'block';
    }

    // Функция закрытия модального окна
    function closeModal(modal) {
        modal.style.display = 'none';
    }

    // Функция отображения сообщений
    function displayMessage(modal, message, isError = false) {
        const messageElement = document.createElement('p');
        if (typeof message === 'string') {
            messageElement.textContent = message;
        } else {
           
            messageElement.textContent = JSON.stringify(message);
        }
        messageElement.style.color = isError ? 'red' : 'green';
        modal.querySelector('.authorisationModalContent, .registrationModalContent').appendChild(messageElement);
    }

    // Обработчики для модального окна авторизации
    authOpenButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            openModal(authModal);
        });
    });

    authCloseButton && authCloseButton.addEventListener('click', function() {
        closeModal(authModal);
    });

    // Обработчики для модального окна регистрации
    registerOpenButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            openModal(registerModal);
        });
    });

    registerCloseButton && registerCloseButton.addEventListener('click', function() {
        closeModal(registerModal);
    });

    // Закрытие модального окна при клике вне его
    window.addEventListener('click', function(event) {
        if (event.target === authModal) {
            closeModal(authModal);
        }
        if (event.target === registerModal) {
            closeModal(registerModal);
        }
    });

    // Обработчик отправки формы авторизации
    if (authForm) {
        authForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(authForm);

            fetch(loginUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayMessage(authModal, data.message);
                    setTimeout(function() {
                        window.location.reload(); // Перезагружаем страницу после успешной авторизации
                    }, 1500);
                } else {
                    displayMessage(authModal, data.message, true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                displayMessage(authModal, 'Произошла ошибка при отправке запроса.', true);
            });
        });
    }

    // Обработчик отправки формы регистрации
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(registerForm);

            fetch(registrationUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayMessage(registerModal, data.message);
                    setTimeout(function() {
                        window.location.reload(); 
                    }, 1500);
                } else {
                    displayMessage(registerModal, data.message, true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                displayMessage(registerModal, 'Произошла ошибка при отправке запроса.', true);
            });
        });
    }

    // Функция для получения значения CSRF-токена из cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});