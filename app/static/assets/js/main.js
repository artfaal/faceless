// Мой пользовательский JS файл
$(document).ready(function() {
    // Функция для затемнения фона, при наведении на меню.
    // Когда наводишь мышкой, активируется специальный фон, полупрозрачный
    // который находится под меню, но над всем остальным
    $( "#top-line-navigation" ).hover(
      function() {
        $('#lightbox-shadow').css('display', 'block');
      }, function() {
        $('#lightbox-shadow').css('display', 'none');
      }
    );
})