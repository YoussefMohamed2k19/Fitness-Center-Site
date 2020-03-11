

(function ($) {
  "use strict";

  /*==================================================================
  [ Change Value room name input ]*/
  //$('#room_input').val($('#room_input').val() + 'General');
  $('#input').on("click", function(){

      var text = "01";
      var input = $('#input');
      var textLocation = $(input).val().indexOf(text);
    
      if(textLocation === -1){
        $(input).val( $(input).val() + text );
      }else{
        $(input).val( $(input).val().substr(0, textLocation) + text );
      }
    
    });

    

})(jQuery);


$(document).ready(function(){

/* default settings */
$('.venobox').venobox({
  overlayColor: 'rgba(6, 12, 34, 0.9)',
  closeBackground: 'rgba(6, 12, 34, 0.1)',
  closeColor: '#fff',
  titleattr: 'data-title',    // default: 'title'
  infinigall: false,          // default: false
  spinner: 'double-bounce'
}); 
$(".vbox-prev").hide();
$(".vbox-next").hide();
// 
});