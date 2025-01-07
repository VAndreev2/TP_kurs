// Инициализируем переменные
let total = 0;
const cartItems = new Set(); // Используем Set для хранения уникальных идентификаторов товаров

// Находим все кнопки "В корзину"
const addToCartButtons = document.querySelectorAll('.add-to-cart');
const makePurchaseButton = document.querySelector('.make-purchase');

// Обрабатываем клик по каждой кнопке "В корзину"
addToCartButtons.forEach(button => {
    button.addEventListener('click', function(event) {
    event.preventDefault();  // Предотвращаем переход по ссылке
    // Получаем цену товара из атрибута data-price
    const price = parseInt(this.getAttribute('data-price'));
    const buy_id = parseInt(this.getAttribute('buy-id'));

    // Проверяем, добавлен ли товар в корзину
    if (cartItems.has(buy_id)) {
        alert("Экземпляр товара уже находится в корзине. Повторное добавление невозможно.");
    } else {
    // Добавляем товар в корзину
        cartItems.add(buy_id);
        console.log(cartItems);
        total += price; // Суммируем стоимость

        // Обновляем текст в элементе с id="cart-total"
        document.getElementById('cart-total').textContent = total + ' ₽';
    }
    });
});

// Обрабатываем клик по кнопке "Оформить покупку"
makePurchaseButton.addEventListener('click', function(event) {
    event.preventDefault();
    if (cartItems.size > 0) {
        // Преобразуем Set в массив и создаем строку с идентификаторами товаров
        const productIds = Array.from(cartItems).join(',');
        // Переход по ссылке с использованием идентификаторов товаров
        console.log(total)
        window.location.href = `/buy/${productIds}&${total}`;
    } else {
        alert("Выберите товар для покупки.");
    }
});