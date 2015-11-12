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
    // Функция, что бы перескакивать на доп. категорию. Показывается только
    // для групп, в которых есть дочерние
    $('a[href*=#]').click(function(event){
      event.preventDefault();
      var target_top= $('a[name="'+this.href.split("#")[1]+'"]').offset().top;
      $('html, body').animate({scrollTop:target_top}, 'slow');
    });
})