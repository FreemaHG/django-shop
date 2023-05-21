const loadBtn = document.getElementById('add-to-cart');  // Получаем элемент по id (кнопка "Добавить в корзину")
const spinner = document.getElementById('spinner-product');  // Получаем элемент по id = spinner (сообщение "Загрузка...")
const alert = document.getElementById('alert-product');  // Получаем элемент по id = alert (сообщение "Товаров больше нет")
const count = document.getElementById('product-count').value;

const blockNotInCart = document.getElementById('product-not-in-cart')
const blockInCart = document.getElementById('product-in-cart')

function addToCart() {
  console.log('Сработала функция addToCart');
  var _product_id = {{ object.id }}
  console.log(`Переменная _product_id - ${_product_id}`);
  console.log(`Переменная count - ${count}`);
  $.ajax({
    url: '{% url "shop:add_to_cart" %}',  // Выполняем ajax-запрос на указанный URL

    // СДЕЛАТЬ POST-ЗАПРОС!!!
    type: 'GET',  // Тип запроса
    data: {  // Отправляемые данные
      'product_id': _product_id,
      'count': count
    },

    beforeSend: function () {  // Функция отправки
      blockNotInCart.classList.add('not-visible');  // Скрываем кнопку "Загрузить еще" при отправке запроса, добавив класс для скрытия блока
      spinner.classList.remove('not-visible');  // Выводим иконку "Загрузка.."
    },

    success: function (response) {  // Функция успеха, принимает объект ответа из функции
      const data = response.res  // Сохраняем полученные данные (новые загружаемые товары)
      console.log(`Переменная data - ${data}`);
      spinner.classList.add('not-visible')  // Скрываем сообщение о загрузке, добавив класс для скрытия блока
      blockInCart.classList.remove('not-visible');
      blockNotInCart.classList.add('not-visible');
    },

    error: function (err) {  // Функция, вызываемая при ошибке. Принимает текст ошибки
      console.log(err);
    },
  });
}

loadBtn.addEventListener('click', () => {  // При событии "нажатие" вызовется функция loadmorePost()
  console.log('Сработал клик');
  addToCart()
});