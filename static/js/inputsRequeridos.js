$(document).ready(function(){
  $('input[name=csrfmiddlewaretoken]').after('<label>Todos los campos con <span style="color:red;">* </span>son requeridos</label>');
  $('form').find(':input, select').each(function(key, val){
    if($(this).attr('name') != 'csrfmiddlewaretoken' && $(this).attr('type') != 'submit' && $(this).attr('type') != 'button' ){
      if($(this).attr('required') == 'required' ){
        $(this).closest('div.form-group').find('label').append('<span style="color:red;">*</span>');
      }  
    }
  });

});