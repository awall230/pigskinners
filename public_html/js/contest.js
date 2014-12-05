

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

            session_deferred.resolve();              

            promise1.done(function() {
                promise2.done(function() {
                    var nav_string = '<a id = "current_week" href="#">CURRENT WEEK</a>';
                    nav_string += '<a id="last_week" href="#"> | LAST WEEK</a>';
                    $("#nav").prepend(nav_string);
                    var $picks = $('#picks tr[id]');
                    for (var i = 0; i < $picks.length; i++) {
                        addPick($picks[i].id);
                    }
                    get_leaderboard();
                    $('#leaderboard').hide();
                    $('#past_picks').hide();
                    $('#current_week').css('font-weight', 'Bold');
                    eventHandlers();
                });
            });   
        }
    });
});

function get_leaderboard() {    
    $.ajax({
        url: "cgi-bin/contest_results.py",
        type: "GET",
        dataType: "json",

        success: function(dat) {
            console.dir(dat);
            $('#leaderboard').append('<h3>Results</h3>');
            $('#leaderboard').append('<table></table>');
            var $leaderboard = $('#leaderboard table');
            var str, user;
            str = '<tr><th>Rank</th><th>Email</th>';
            str += '<th>Total winnings</th><th>Number of picks</th></tr>';
            $leaderboard.append(str);
            for (var i=0; i<dat.leaders.length; i++) {
                str = '';
                user = dat.leaders[i];
                str += '<tr><td>' + String(i+1) + '</td>';
                //str += '<td><a class="user_link" href="#">' + user.email + '</a></td>';
                str += '<td>' + user.email + '</td>';
                str += '<td>' + user.total_winnings + '</td>';
                str += '<td>' + user.bet_count + '</td></tr>';

                $leaderboard.append(str);
            }
        }
    });
}

function eventHandlers() {

    $('#current_week').on('click', function(e) {
        e.preventDefault();
        $(this).css('font-weight', 'Bold');
        $('#last_week').css('font-weight', 'Normal');
        $('#leaderboard').hide();
        $('#past_picks').hide();
        $('#odds').show();
        $('#picks').show();
    });
    
    $('#last_week').on('click', function(e) {
        e.preventDefault();
        $(this).css('font-weight', 'Bold');
        $('#current_week').css('font-weight', 'Normal');
        $('#picks').hide();
        $('#odds').hide();
        $('#leaderboard').show();
        $('#past_picks').show();
    });               
    
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
                    displayPick(dat.bets[0], $('#picks'));
                    addPick(b_id);
                    //remove form
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
    
    $('table').on('click', 'a.delete', function(e) {
        e.preventDefault();
        var b_id = $(this).parent().parent().attr('id');
        $.ajax({
            url: "cgi-bin/make_pick.py",
            type: "POST",
            data: {
                contest: is_contest,
                bet_id: b_id,
                num: null,
                action: "delete"
            },
            dataType: "json",

            success: function(dat) {
                deletePick(b_id);                }
        });
    });
}

function addPick(bet_id) {
    var $entry = $('#odds #' + bet_id);
    if ($entry.length > 0) {
        if ($entry.has('a').length > 0) {
            var temp = $entry.children().text();
            $entry.empty();
            if (temp.charAt(temp.length-1) === "x") {
                $entry.append(temp.slice(0,-1));    //get rid of x at end
            }
            else {
                $entry.append(temp);
            }
            $entry.css('font-weight', 'Bold');
        }
    }
}

function deletePick(bet_id) {
    var $entry = $('#picks #' + bet_id);
    var amount = $entry.next().children('.amount').text();
    amount_spent -= parseFloat(amount);
    $('#bankroll').text(String(1000.0 - amount_spent));
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