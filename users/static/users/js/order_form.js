document.addEventListener('DOMContentLoaded', function() {
    // Показ модального окна
    document.querySelector('.add-funds-btn').addEventListener('click', function() {
        var modal = document.getElementById('modal');
        modal.style.display = 'flex'; // Показываем модальное окно
    });

    // Закрытие модального окна
    document.querySelector('.close-btn').addEventListener('click', function() {
        var modal = document.getElementById('modal');
        modal.style.display = 'none'; // Скрываем модальное окно
    });

    // Обработка формы с помощью AJAX и подтверждением
    document.getElementById('balance-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Останавливаем стандартную отправку формы

        // Показываем диалог подтверждения
        var userConfirmed = confirm("Are you sure you want to submit this balance replenishment request?");

        if (userConfirmed) {
            var form = this;
            var formData = new FormData(form);
            var csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;

            // Получаем URL из атрибута data-url
            var url = form.getAttribute('data-url');

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Показываем сообщение об успешной отправке
                    var successMessage = document.getElementById('success-message');
                    successMessage.innerText = 'Balance replenished successfully!';
                    successMessage.style.display = 'block'; // Показываем сообщение
                    form.reset();  // Очищаем форму после успешной отправки

                    // Скрываем модальное окно
                    document.getElementById('modal').style.display = 'none';

                    // Скрываем сообщение через 4 секунды
                    setTimeout(function() {
                        successMessage.style.display = 'none';
                    }, 4000);
                } else {
                    document.getElementById('balance-form-message').innerText = 'Error: ' + JSON.stringify(data.errors);
                    document.getElementById('balance-form-message').style.display = 'block'; // Показываем сообщение об ошибке
                }
            })
            .catch(error => {
                document.getElementById('balance-form-message').innerText = 'Error: ' + error;
                document.getElementById('balance-form-message').style.display = 'block'; // Показываем сообщение об ошибке
            });
        } else {
            // Если пользователь отменил действие, выводим сообщение
            document.getElementById('balance-form-message').innerText = 'Action canceled.';
            document.getElementById('balance-form-message').style.display = 'block'; // Показываем сообщение
        }
    });
});
