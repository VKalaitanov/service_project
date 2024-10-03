// Функция для переключения видимости формы
function toggleForm(formId) {
    var forms = document.getElementsByClassName('service-form');
    // Скрываем все формы
    for (var i = 0; i < forms.length; i++) {
        forms[i].style.display = 'none';
    }
    // Показываем только выбранную форму
    var form = document.getElementById(formId);
    if (form) {
        form.style.display = 'block';
    }
}

// Обработчик для всех форм
document.querySelectorAll('.purchase-form').forEach(function(form) {
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Останавливаем стандартную отправку формы

        // Окно подтверждения
        var userConfirmed = confirm("Are you sure you want to buy this service?");

        if (userConfirmed) {
            // Если пользователь подтвердил, отправляем форму
            form.submit();
        } else {
            // Если отменил — выводим сообщение или просто не отправляем
            alert("Purchase canceled.");
        }
    });
});