$(document).ready(function() {
    $.ajax({
        url: "cgi-bin/odds.py",
        type: "GET",
        data: {
            contest: is_contest
        },
        dataType: "json",
        
        success: function(dat) {
            $('#odds_info').append('<table id="odds"></table>');
            var str, game;
            console.dir(dat);
            for (var i = 0; i < dat.odds.length; i++) { 
                str = "";
                game = dat.odds[i];
                
                str += '<tr class="' + game.game_id + '">';
                str += '<td>Spread:</td>';
                str += '<td>' + game.visitor_name + '</td>';
                str += '<td id="' + game.game_id + '-0">';
                str += '<a href="#">' + game.visitor_spread + '</a></td>';
                str += '<td>@' + game.home_name + '</td>';
                str += '<td id="' + game.game_id + '-1">'
                str += '<a href="#">' + game.home_spread + '</a></td>';
                str += '</tr>';
                
                str += '<tr class="' + game.game_id + '">';
                str += '<td>Moneyline:</td>';
                str += '<td>' + game.visitor_name + '</td>';
                str += '<td id="' + game.game_id + '-2">'
                str += '<a href="#">' + game.visitor_moneyline + '</a></td>';
                str += '<td>@' + game.home_name + '</td>';
                str += '<td id="' + game.game_id + '-3">'
                str += '<a href="#">' + game.home_moneyline + '</a></td>';
                str += '</tr>';
                
                str += '<tr class="' + game.game_id + '">';
                str += '<td>Over/Under:</td>';
                str += '<td>Over</td>';
                str += '<td id="' + game.game_id + '-4"><a href="#">' + game.over + '</a></td>';
                str += '<td>Under</td>';
                str += '<td id="' + game.game_id + '-5"><a href="#">' + game.under + '</a></td>';
                str += '</tr>';
                
                str += '<tr><td colspan="4">' + game.dt + '</td></tr>';
                str += '<tr><td><br/></td></tr>';
                
                $('#odds').append(str);
            }
            deferred2.resolve();
        }
    });
});