// Функция для переключения видимости формы
function toggleForm(formId) {
    const forms = document.querySelectorAll('.service-form');

    // Скрываем все формы
    forms.forEach(form => {
        form.style.display = 'none';
    });

    // Показываем только выбранную форму
    const form = document.getElementById(formId);
    if (form) {
        form.style.display = 'block';
    }
}

// Функция для подтверждения покупки
function confirmPurchase(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    const userConfirmed = confirm("Are you sure you want to buy this service?");
    if (userConfirmed) {
        this.submit(); // Отправляем форму
    } else {
        alert("Purchase canceled."); // Отмена покупки
    }
}

// Обработчик для всех форм
document.querySelectorAll('.purchase-form').forEach(form => {
    form.addEventListener('submit', confirmPurchase);
});
