// Инициализация глобальных переменных
let countdown;  // Глобальная переменная для хранения ID таймера
let timeLeft = 30;  // Таймер на 30 секунд
const timerElement = document.getElementById("timer");
const resendButton = document.getElementById("resend-button");
const timerText = document.getElementById("timer-text");

// Функция для запуска таймера
function startCountdown() {
    timeLeft = 30;  // Сброс времени до 30 секунд
    timerElement.textContent = timeLeft;  // Отображаем начальное время
    timerText.style.display = "block";  // Показываем текст с таймером
    resendButton.style.display = "none";  // Скрываем кнопку повторной отправки

    // Если таймер уже был запущен, очищаем его перед запуском нового
    if (countdown) {
        clearInterval(countdown);
    }

    // Запускаем новый таймер
    countdown = setInterval(() => {
        timeLeft--;
        timerElement.textContent = timeLeft;  // Обновляем отображение таймера

        // Когда время истекает, останавливаем таймер и показываем кнопку
        if (timeLeft <= 0) {
            clearInterval(countdown);  // Останавливаем таймер
            resendButton.style.display = "block";  // Показываем кнопку повторной отправки
            timerText.style.display = "none";  // Скрываем текст с таймером
        }
    }, 1000);  // Таймер обновляется каждую секунду
}

// Функция для получения CSRF-токена из cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для повторной отправки письма с AJAX запросом
function resendEmail() {
    const csrftoken = getCookie('csrftoken');  // Получаем CSRF токен
    console.log("CSRF Token: ", csrftoken);    // Проверяем, что CSRF токен не пустой

    fetch("http://31.129.102.58:8000/users/resend-verification-email/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})  // Можно передавать необходимые данные в теле запроса
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message);  // Сообщение об успехе
            startCountdown();  // Перезапуск таймера после успешной отправки
        } else if (data.error) {
            console.error('Ошибка:', data.error);  // Сообщение об ошибке
        }
    })
    .catch(error => {
        console.error('Ошибка запроса:', error);  // Логируем ошибки в консоль
    });
}

// Запуск таймера при загрузке страницы
startCountdown();