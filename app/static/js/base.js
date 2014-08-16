$(document).ready(function () {
    $('#submit').click(function() {
        $.ajax({
            method: 'POST',
            url: '/ajax/test',
            data: {
                first: $('input[name="first"]').val(),
                second: $('input[name="second"]').val()
            },
            dataType: 'JSON',
            success: function(resp) {
                if (resp.success) {
                    $("#result").text(resp.result);
                }
                else {
                    alert("error!")
                }
            },
            error: function(resp) {
                alert("server no response!")
            }
        });
    });
});