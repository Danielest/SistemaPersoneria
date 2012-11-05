(function($) {
   
   alert("a");
   $("#id_fecha_envio" ).datepicker( "option", "showAnim", "Drop");
  
$( "#id_fecha_envio" ).datepicker({
            changeMonth: true,
            changeYear: true
        });     

        alert("aaa");      
   
})(django.jQuery);
