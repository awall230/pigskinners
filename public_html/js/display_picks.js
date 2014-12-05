$(document).ready(function() {
    //var deferred = new $.Deferred();
    session_promise.done(function() {   //wait until we get user info
        $.ajax({
            url: "cgi-bin/get_picks.py",
            type: "GET",
            data: {
                email: user,
                contest: is_contest
            },
            dataType: "json",
            
            success: function(dat) {
                $("#bet_info").append('<table id="picks"></table>');
                if (is_contest) {
                    $("#picks").prepend('<h3>Remaining bankroll: <span id="bankroll">1000</span></h3>');
                    $("#bet_info").append('<table id="past_picks"></table>');
                }
                console.dir(dat);
                var str, bet, bet_id;
                for (var i = 0; i < dat.bets.length; i++) {
                    if (is_contest){
                        if (dat.bets[i].week === "current") {
                            displayPick(dat.bets[i], $("#picks"));
                        }
                        else {
                            displayPick(dat.bets[i], $("#past_picks"));
                        }
                    }
                    else {
                        displayPick(dat.bets[i],$("#picks"));
                    }
                }   
                deferred1.resolve();
            }
        });
    });
});

function displayPick(bet, $picks) {
    var str, bet_id;
    str = "";
    bet_id = bet.game_id + '-' + bet.bet_type;

    str += '<tr id="' + bet_id + '">';
    str += '<td class="0 2">' + bet.visitor_name + '</td>';
    if (bet.visitor_score) {
        str += '<td class="0 2">' + bet.visitor_score + '</td>';
    }
    else {
        str += '<td class="0 2"></td>';
    }
    str += '<td class="1 3">@' + bet.home_name + '</td>';
    if (bet.home_score) {
        str += '<td class="1 3">' + bet.home_score + '</td>';
    }
    else {
        str += '<td class="1 3"></td>';
    }
    if (bet.bet_type === '0' || bet.bet_type === '1') {
        str += '<td>Spread</td><td>' + bet.margin + '</td>';
    }
    else if (bet.bet_type === '2' || bet.bet_type === '3') {
        str += '<td>Moneyline</td><td>' + bet.american_odds + '</td>';
    }
    else if (bet.bet_type === '4' || bet.bet_type === '5') {
        str += '<td class="' + bet.bet_type + '">';
        str += (bet.bet_type === '4') ? 'Over' : 'Under';
        str += '</td><td>' + bet.margin + '</td>';
    }
    
    if (bet.status === "open") {
        str += '<td><a class="delete" style="color:red" href="#">delete</a>';
    }
    
    str += '</tr>';

    str += '<tr><td colspan="2">' + bet.dt + '</td>';
    if (is_contest) { 
        str += '<td>Wager:</td><td class="amount">' + bet.amount + '</td>';
        if ($picks.is('#picks')) {
            amount_spent += parseFloat(bet.amount);
            $('#bankroll').text(String(1000.0 - amount_spent));
        }
    }
    str += '</tr>';
    
    if (bet.result) {
        var result_string = "";
        if (parseInt(bet.result) > 0) {
            result_string = "Win";
        }
        else if (parseInt(bet.result) === 0) {
            result_string = "Push";
        }
        else {
            result_string = "Lose";
        }
        
        str += '<tr><td>Result: ' + result_string + '</td>';
        str += '<td>' + parseFloat(bet.winnings).toFixed(2) + '</td></tr>';
    }


    str += '<tr><td><td/></tr>';

    $picks.prepend(str);
    //make user's pick bold
    $('#' + bet_id + ' .' + bet.bet_type).css('font-weight', 'Bold');
}