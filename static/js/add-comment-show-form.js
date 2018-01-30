$(document).ready(function() {
     $('[id^= comment_form]').hide();
     $('[id^= add-comment_btn]').click(function() {
         var id = $(this).data('id');
         $('#comment_form-'+id).toggle();
     })
});

$(document).ready(function() {
     $('#q-comment_form').hide();
     $('#q-add-comment_btn').click(function() {
         $('#q-comment_form').toggle();
     })
});