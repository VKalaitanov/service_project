document.querySelectorAll('.purchase-form').forEach(function(form) {
    var quantityInput = form.querySelector('input[name="quantity"]');
    var totalPriceElement = form.querySelector('[id^="total-price"]');
    var pricePerUnit = parseFloat(form.getAttribute('data-price-per-unit').replace(',', '.').trim());

    // Общая скидка
    var discountPercentage = parseFloat(form.getAttribute('data-discount-percentage').replace(',', '.').trim()) || 0;

    // Индивидуальная скидка
    var userDiscountPercentage = parseFloat(form.getAttribute('data-user-discount-percentage').replace(',', '.').trim()) || 0;

    // Применяем максимальную из скидок
    var effectiveDiscountPercentage = Math.max(discountPercentage, userDiscountPercentage);

    quantityInput.addEventListener('input', function() {
        var quantity = parseInt(quantityInput.value) || 0;
        var totalPrice = pricePerUnit * quantity;

        var discount = (totalPrice * effectiveDiscountPercentage) / 100;
        var finalPrice = totalPrice - discount;

        totalPriceElement.textContent = finalPrice.toFixed(2) + ' $';
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const errorMessage = document.getElementById("error-message");
    if (errorMessage) {
        setTimeout(() => {
            errorMessage.style.display = "none"; // Скрыть сообщение через 4 секунды
        }, 4000);
    }
});

// Функция для установки cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Функция для получения cookie
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Функция для скрытия блока, если все сообщения закрыты
function checkAndHideGlobalMessages() {
    var visibleMessages = document.querySelectorAll('.global-message:not([style*="display: none"])');
    if (visibleMessages.length === 0) {
        document.getElementById('global-messages').style.display = 'none';
    }
}

// Скрытие сообщений, если они уже закрыты
document.querySelectorAll('.global-message').forEach(function (message) {
    var messageId = message.getAttribute('data-message-id');
    if (!getCookie('message_' + messageId)) {
        message.style.display = 'block'; // Показываем только те сообщения, которых нет в cookies
    }
});

// Обработка клика по кнопке "крестик"
document.querySelectorAll('.close-message').forEach(button => {
    button.addEventListener('click', function () {
        var message = this.parentElement;
        var messageId = message.getAttribute('data-message-id');
        message.style.display = 'none'; // Скрываем сообщение
        setCookie('message_' + messageId, 'hidden', 30); // Сохраняем в cookie на 30 дней
        checkAndHideGlobalMessages(); // Проверяем, скрыты ли все сообщения
    });
});

// Проверяем сразу, нужно ли скрыть весь блок глобальных сообщений
checkAndHideGlobalMessages();
