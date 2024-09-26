document.addEventListener('DOMContentLoaded', function() {
    const categoryForm = document.getElementById('category-form');
    const tagForm = document.getElementById('tags-form');

    function loadServices(categoryId, tagId) {
        let url = '/load_services/?';
        if (categoryId) url += `category=${categoryId}&`;
        if (tagId) url += `tag=${tagId}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                document.querySelector('.service-list').innerHTML = data.html;
                attachBuyNowButtons(); // Привязываем обработчики к новым кнопкам
                attachCloseFormButtons(); // Обработчики закрытия форм
            })
            .catch(error => console.error('Ошибка при загрузке услуг:', error));
    }

    // Обработка выбора категории и тега
    categoryForm.addEventListener('change', function(event) {
        const selectedCategoryId = event.target.value;
        const selectedTagId = tagForm.querySelector('input[name="tag"]:checked')?.value;

        loadServices(selectedCategoryId, selectedTagId);
    });

    tagForm.addEventListener('change', function(event) {
        const selectedTagId = event.target.value;
        const selectedCategoryId = categoryForm.querySelector('input[name="category"]:checked')?.value;

        loadServices(selectedCategoryId, selectedTagId);
    });

    // Инициализация загрузки услуг при первой загрузке страницы
    const initialCategoryId = categoryForm.querySelector('input[name="category"]:checked')?.value;
    const initialTagId = tagForm.querySelector('input[name="tag"]:checked')?.value;
    loadServices(initialCategoryId, initialTagId);
});
