document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('callbackForm');
    const successModal = document.getElementById('successModal');
    const closeModalButton = document.querySelector('.close-button');
    const modalClose = document.getElementById('modal-close');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    successModal.style.display = 'block';
                    form.reset();
                } else if (data.status === 'error') {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                alert('Произошла ошибка при отправке запроса.');
            });
    });

    modalClose.addEventListener('click', function () {
        successModal.style.display = 'none';
    });

});