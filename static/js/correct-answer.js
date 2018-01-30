$(document).ready(function() {
    $('[id^= correct-answer]').change(function () {
        var answer_id = $(this).data('id');
        var chb = $(this);
        console.log(answer_id, $(this).is(":checked"));
        $.ajax({
            url: '/ajax/correct-answer/',
            data: {
                'answer_id': answer_id,
                'correct': $(this).is(":checked")
            },
            dataType: 'json',
            success: function (data) {
                // if (data.is_correct) {
                //     // alert("");
                // }
            }
        });
    })
});