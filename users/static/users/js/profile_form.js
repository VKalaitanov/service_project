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