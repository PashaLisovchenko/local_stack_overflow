function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
$(document).ready(function(){
    var like = $('a.like-question');
    like.click(function(e){
        e.defaultPrevented;
        $.ajax({
            type: "POST",
            url: '/ajax/like/',
            data: {
                'model_name': $(this).data('model-name'),
                'id': $(this).data('id'),
                'action': $(this).data('action')
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                var previous_action = like.data('action');
                like.data('action', previous_action == 'like' ? 'unlike' : 'like');
                like.text(previous_action == 'like' ? 'Unlike' : 'Like');
                var previous_likes = parseInt($('.statistic-question .tl-question').text());
                $('.statistic-question .tl-question').text(previous_action == 'like' ? previous_likes + 1 : previous_likes - 1);
            }
        });
        return false;
    });
});
$(document).ready(function(){
    var like = $('[class^= like-answer]');
    like.click(function(e) {
        e.defaultPrevented;
        $.ajax({
            type: "POST",
            url: '/ajax/like/',
            data: {
                'model_name': $(this).data('model-name'),
                'id': $(this).data('id'),
                'action': $(this).data('action')
            },
            dataType: 'json',
            success: function (data) {

                var like = $('.like-answer-'+data['id']);
                console.log(like);
                var previous_action = like.data('action');
                like.data('action', previous_action == 'like' ? 'unlike' : 'like');
                like.text(previous_action == 'like' ? 'Unlike' : 'Like');
                var previous_likes = parseInt($('.tl-answer-'+data['id']).text());
                $('.tl-answer-'+data['id']).text(previous_action == 'like' ? previous_likes + 1 : previous_likes - 1);
            }
        });
        return false;
    });
});