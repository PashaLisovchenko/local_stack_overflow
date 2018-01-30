$(document).ready(function() {
    var btn = $('#q-list-toggle');
    var count = $("#q-comment-list").find($('.comment')).length;
    console.log(count);
    if(count <= 3){
        btn.hide();
    }
    btn.click(function(){
        $('#q-comment-list').toggleClass('open');
    });
});

$(document).ready(function() {
    var lists = $('[id^= a-comment-list]');
    var btn =  $('[id^= a-list-toggle]');
    lists.each(function() {
        var count = $(this).find($('.comment')).length;
        if(count <= 3){
            $(this).find(btn).hide();
    }
    });
    btn.click(function() {
        var id = $(this).data('id');
        $('#a-comment-list-'+id).toggleClass('open');
     })
});