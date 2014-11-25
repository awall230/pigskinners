

$(document).ready(function() {
    $.ajax({
        url: "cgi-bin/check_session.py",
        type: "GET",
        dataType: "json",
        
        success: function(dat) {
            console.dir(dat);
            if (dat.logged_in) {
                $("#session_info").append('<a href=index.html>Home</a> | ');
                $("#session_info").append("<a href=profile.html?u=" + dat.email + ">" + dat.first_name + "'s Profile</a> | ");
                $("#session_info").append('<a href=cgi-bin/logout.py>Log Out</a>');
                $("#session_info").after('<h2>Weekly Contest</h2>');


                user = dat.email;   //defined in script in contest.html
            }

            else {
                console.log('not logged in');
                $('div').hide();
                $("#redirect").append('<meta http-equiv="refresh" content="1; url=cgi-bin/login.py" />');
            }              

            promise1.done(function() {
                promise2.done(function() {
                    // var $picks = $('#picks tr[id]');
                    // for (var i = 0; i < $picks.length; i++) {
                    //     addPick($picks[i].id);
                    // }
                    eventHandlers();
                });
            });   
        }
    });
});

function eventHandlers() {               
    
    $('#odds').on('click', 'a', function(e) {
        e.preventDefault();
        var b_id = $(this).parent().attr('id');
        console.log(b_id);
        var bet_form = '<button type="button" class="cancel">x</button>' 
        bet_form += '<form class="wager"><input type="text" placeholder="Enter amount..." />';
        bet_form += '<input type="submit" value="OK" /></form>';
        $(this).after(bet_form);
    });

    $('#odds').on('submit', 'form.wager', function(e) {
        console.log('eeeee');
        e.preventDefault();
        var amt = $('input:text').val();
        var b_id = $(this).parent().attr('id');
        $.ajax({
            url: "cgi-bin/make_pick.py",
            type: "POST",
            data: {
                contest: is_contest,
                bet_id: b_id,
                num: $(this).siblings('a').text(),
                action: "add",
                amount: amt
            },

            success: function(dat) {
                console.dir(dat);
                if (dat.bets.length > 0) {
                    ///////TODO: display pick
                    addPick(b_id);
                    $(this).prev().remove();
                    $(this).remove();
                }
            }
        });
    });

    $('#odds').on('click', 'button.cancel', function(e) {
        $(this).next().remove();
        $(this).remove();
    });
    
    // $('table a.delete').on('click', function(e) {
    //     e.preventDefault();
    //     var b_id = $(this).parent().parent().attr('id');
    //     $.ajax({
    //         url: "cgi-bin/make_pick.py",
    //         type: "POST",
    //         data: {
    //             bet_id: b_id,
    //             num: null,
    //             action: "delete"
    //         },
    //         dataType: "json",

    //         success: function(dat) {
    //             deletePick(b_id);
    //             eventHandlers();
    //             }
    //     });
    // });
}

function addPick(bet_id) {
    var $entry = $('#odds #' + bet_id);
    if ($entry.length > 0) {
        if ($entry.has('a').length > 0) {
            var temp = $entry.children().text();
            $entry.empty();
            $entry.append(temp);
            $entry.css('font-weight', 'Bold');
        }
    }
}

function deletePick(bet_id) {
    var $entry = $('#picks #' + bet_id);
    if ($entry.length > 0) {
        $entry.nextAll(':lt(2)').remove();
        $entry.remove();
    }
    
    var $entry = $('#odds #' + bet_id);
    if ($entry.length > 0) {
        var temp = $entry.text();
        $entry.text('');
        $entry.append('<a href="#">' + temp + '</a>');
        $entry.removeAttr('style');
    }
    //$entry.siblings('.delete').remove();
}