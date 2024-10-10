document.querySelectorAll('.purchase-form').forEach(function(form) {
        var quantityInput = form.querySelector('input[name="quantity"]');
        var totalPriceElement = form.querySelector('[id^="total-price"]');
        var pricePerUnit = parseFloat(form.getAttribute('data-price-per-unit').replace(',', '.').trim());
        var discountPercentage = parseFloat(form.getAttribute('data-discount-percentage').replace(',', '.').trim()) || 0;

        quantityInput.addEventListener('input', function() {
            var quantity = parseInt(quantityInput.value) || 0;
            var totalPrice = pricePerUnit * quantity;

            var discount = (totalPrice * discountPercentage) / 100;
            var finalPrice = totalPrice - discount;

            totalPriceElement.textContent = finalPrice.toFixed(2) + ' $';
        });
    });

    // Переключение видимости чата
    const chatBox = document.getElementById('chat-box');
    const chatToggleBtn = document.getElementById('chat-toggle-btn');
    const closeChatBtn = document.getElementById('close-chat');

    chatToggleBtn.addEventListener('click', function() {
        chatBox.style.display = 'flex';
        chatToggleBtn.style.display = 'none'; // Скрыть иконку
    });

    closeChatBtn.addEventListener('click', function() {
        chatBox.style.display = 'none';
        chatToggleBtn.style.display = 'block'; // Показать иконку снова
    });

    // Логика для отправки сообщений
    const chatBody = document.getElementById('chat-body');
    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message');

    sendMessageBtn.addEventListener('click', function() {
        const message = chatInput.value;
        if (message.trim() !== '') {
            const messageElement = document.createElement('p');
            messageElement.textContent = message;
            chatBody.appendChild(messageElement);
            chatInput.value = '';
            chatBody.scrollTop = chatBody.scrollHeight; // Прокрутить чат вниз
        }
    });