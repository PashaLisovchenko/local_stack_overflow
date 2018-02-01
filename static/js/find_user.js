$(document).ready( function(){
    $('#suggestion').keyup(function(){
        var target = $(this).data('target');
        var query = $(this).val();
        console.log(target);
        console.log(query);
        if(target=="user"){
            $.ajax({
                type: "GET",
                url: "/users/ajax/user_search/",
                data: {'suggestion': query},
                dataType: 'html',
                success: searchUserSuccess,
                failure: function(data){
                    console.log("FAIL");
                    console.log(data);
                }
            });
        }
        if(target=="tag") {
            $.ajax({
                type: "GET",
                url: "/ajax/find-tags/",
                data: {'suggestion': query},
                dataType: 'html',
                success: searchTagSuccess,
                failure: function(data){
                    console.log("FAIL");
                    console.log(data);
                }
            });
        }
    });
});
function searchUserSuccess(data) {
    console.log("SUCCESS");
    console.log(data);
    $('.user-list').css({display: 'none'});
    $('.search_result').html(data);
}
function searchTagSuccess(data) {
    console.log("SUCCESS");
    console.log(data);
    $('.tags-list').css({display: 'none'});
    $('.search_result').html(data);
}