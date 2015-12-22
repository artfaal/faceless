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
});

$(document).ready(function() {
  // Функция, что бы перескакивать на доп. категорию. Показывается только
  // для групп, в которых есть дочерние
  $('a[href*=#]').click(function(){

    var target_top= $('a[name="'+this.href.split("#")[1]+'"]').offset().top;
    $('html, body').animate({scrollTop:target_top}, 'slow');
  });
})

// Трюк, что бы боковое меню шло до конца страницы
$(document).ready(function() {
    $('.matchheight').matchHeight();
});

$(function accordion() {
  $( "#accordion" ).accordion({
    collapsible: true,
    active: false,
    animate: 200,
    heightStyle: "content"
  });
});