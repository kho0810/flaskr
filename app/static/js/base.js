// $(document).ready(function () {
//     $('#submit').click(function() {
//         $.ajax({
//             method: 'POST',
//             url: '/ajax/test',
//             data: {
//                 first: $('input[name="first"]').val(),
//                 second: $('input[name="second"]').val()
//             },
//             dataType: 'JSON',
//             success: function(resp) {
//                 if (resp.success) {
//                     $("#result").text(resp.result);
//                 }
//                 else {
//                     alert("error!")
//                 }
//             },
//             error: function(resp) {
//                 alert("server no response!")
//             }
//         });
//     });

//     var current_row = 3;
//     var count = 0;

//     $.ajax({
//         url: '/ajax/article_count',
//         dataType: 'json',
//         success: function(resp) {
//             if (resp.count) {
//                 count = resp.count;
//                 $('#more').append(resp.count);
//             }
//             else {
//                 console.log("Invalid response")
//             }
//         },
//         error: function(resp) {
//             console.log("No response")
//         }
//     });

//     $('#more_btn').click(function() {
//         $.ajax({
//             url: '/ajax/article_more',
//             dataType: 'json',
//             data: {
//                 current_row: current_row,
//                 count: count
//             },
//             success: function(resp) {
//                 current_row += 3;
//                 article_list = resp.data;
//                 for (var i in article_list) {
//                     article = article_list[i]
//                     string = "<div class='well' id='article_" + article.id
//                     + "''><h1><a href='article/detail/'" + article.id + ">"
//                     + article.title + "</a></h1><h3>" + article.author + "</h3><h6>"
//                     + article.content + "</h6></div>";
//                     $('#more_data').append(string);
//                 }

//             },
//             error: function(resp) {
//                 console.log("Invalid response!!!")
//             }
//         });
//     });
// });

$(document).ready(function () {
    $('#login_send').click(function() {
        $.ajax({
            url: '/login_chat',
            method: 'post',
            dataType: 'json',
            data: {
                id: $('#chat_name').val()
            },
            success: function(data) {
                if(data.success) {
                    console.log("success: " + data.chat_name);
                    $("#chat_login").css("display", "none");
                    $("#chat_display").css("display", "block");

                    var pusher = new Pusher('62270f36d7ecf7bf7ef0');
                    var channel = pusher.subscribe('presence-hyu');

                    channel.bind('pusher:subscription_succeeded', function(members) {
                        console.log('subscription_succeeded');
                        members.each(function(member) {
                            $('#members').append('<li id=member_"' + member.id + '">' + member.info.username + '</li>');
                        })
                    })
                    channel.bind('pusher:member_added', function(member) {
                        console.log("member_added");
                        $('#chat_room').append('<p>' + member.info.username + '님이 입장하셨습니다. </p>');
                        $('#members').append('<li id=member_' + member.id + '>' + member.info.username + '</li>');
                    })
                    channel.bind('pusher:member_removed', function(member) {
                        console.log("member_removed");
                        $('#chat_room').append('<p>' + member.info.username + '님이 퇴장하셨습니다. </p>');
                        $('#member_' + member.id).remove();
                    })

                    channel.bind('my_event', function(data) {
                        $("#chat_room").append("<div>"
                            + data.name + ": " + data.msg
                            + "<br>" + data.time
                            + "</div>");
                        // console.log(data.name + ' ' + data.msg);
                    });

                    $("#send").click(function() {
                        $.ajax({
                            url: '/chat2',
                            dataType: 'json',
                            data: {
                                msg_data: $('#chat_msg').val()
                            },
                            success: function(data) {
                                console.log("success send");
                            },
                            error: function(data) {
                                console.log("error send");
                            }

                        });
                    });

                }
                else {
                    console.log("Invalid response");
                }
            },
            error: function(data) {
                console.log("fuck");
            }

        })
    });
});