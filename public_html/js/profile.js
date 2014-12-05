

$(document).ready(function() {
    var cook_email;  //user who is logged in, if any
    var is_home_profile = false;   //stores whether or not this is the logged in user's profile or not
    $.ajax({
        url: "cgi-bin/check_session.py",
        type: "GET",
        data: {
            email: user
        },
        dataType: "json",
        
        success: function(dat) {
            console.dir(dat);
            if (dat.logged_in) {
                $("#session_info").append('<a href=index.html>Home</a> | ');
                $("#session_info").append("<a href=profile.html?u=" + dat.email + ">" + dat.first_name + "'s Profile</a> | ");
                $("#session_info").append("<a href=contest.html>Weekly Contest</a> | ");
                $("#session_info").append('<a href=cgi-bin/logout.py>Log Out</a>');

                cook_email = dat.email;
                is_home_profile = (cook_email === user);   //user is from query string in profile.html
            }

            else {
                $("#session_info").append('<a href=index.html>Home</a> | ');
                $("#session_info").append('<a href=cgi-bin/login.py>Log In</a>');
            }
                
            $("#user_info").append('<h2>' + dat.user_first_name + ' ' + dat.user_last_name + '</h2>');
            $("#user_info").append('<p>' + dat.user_email + '<br/>Fan of the ' + dat.user_fav_team);
            $("#user_info").append('</p>');
                


            $('#my_picks').css('font-weight', 'Bold');

            session_deferred.resolve();
            displayRank(user);

            promise1.done(function() {
                promise2.done(function() {
                    var nav_string = '<a id = "my_picks" href="#">PICKS</a>';
                    nav_string += '<a id="current_odds" href="#"> | CURRENT ODDS</a>';
                    $("#nav").prepend(nav_string);
                    if (!(is_home_profile)) {
                        $('table a.delete').hide();
                        $('#current_odds').hide();
                    }

                    var $picks = $('#picks tr[id]');
                    for (var i = 0; i < $picks.length; i++) {
                        addPick($picks[i].id);
                    }
                    $('#odds').hide();
                    $('#my_picks').css('font-weight', 'Bold');
                    clickHandlers();
                });
            });   
        }
    });
});

function displayRank(user_email) {
    $.ajax({
        url: "cgi-bin/leaderboard.py",
        type: "GET",
        data: {
            email: user_email
        },
        dataType: "json",

        success: function(dat) {
            console.dir(dat);
            var rank_string;
            if (dat.rank) {
                rank_string = '<p>Total winnings: ' + dat.total_winnings + '<br/>';
                rank_string += 'Winnings per bet: ' + dat.average_winnings + '<br/>';
                rank_string += 'Rank: ' + dat.rank + ' of ' + dat.user_count + '<br/></p>';
            }
            else {
                rank_string = '<p>No winnings yet...</p>';
            }
            $('#user_info').append(rank_string);
        }
    });
}

function clickHandlers() {
    
    $('#my_picks').on('click', function(e) {
        e.preventDefault();
        $(this).css('font-weight', 'Bold');
        $('#current_odds').css('font-weight', 'Normal');
        $('#odds').hide();
        $('#picks').show();
    });
    
    $('#current_odds').on('click', function(e) {
        e.preventDefault();
        $(this).css('font-weight', 'Bold');
        $('#my_picks').css('font-weight', 'Normal');
        $('#picks').hide();
        $('#odds').show();
    });                
    
    $('#odds a').on('click', function(e) {
        e.preventDefault();
        var b_id = $(this).parent().attr('id');
        $.ajax({
            url: "cgi-bin/make_pick.py",
            type: "POST",
            data: {
                contest: is_contest,
                bet_id: b_id,
                num: $(this).text(),
                action: "add"
            },
            dataType: "json",

            success: function(dat) {
                console.log('here');
                console.dir(dat);
                if (dat.bets.length > 0) {
                    displayPick(dat.bets[0], $('#picks'));
                    addPick(b_id);
                    clickHandlers();
                }
            }
        });
    });
    
    $('table a.delete').on('click', function(e) {
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
                deletePick(b_id);
                clickHandlers();
                }
        });
    });
}

function addPick(bet_id) {
    var $entry = $('#odds #' + bet_id);
    if ($entry.length > 0) {
        if ($entry.has('a').length > 0) {
            var temp = $entry.children().text();
            $entry.empty();
            $entry.append(temp);
            $entry.css('font-weight', 'Bold');
            
            var $opposite_entry = $entry.siblings().has('a');
            if ($opposite_entry.length > 0) {
                temp = $opposite_entry.children().text();
                $opposite_entry.empty();
                $opposite_entry.append(temp);
            }
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
    
    var $opposite_entry = $entry.siblings('[id]');
    if ($opposite_entry.length > 0) {
        var temp = $opposite_entry.text();
        $opposite_entry.text('');
        $opposite_entry.append('<a href="#">' + temp + '</a>');
    }
    
    //$entry.siblings('.delete').remove();
}