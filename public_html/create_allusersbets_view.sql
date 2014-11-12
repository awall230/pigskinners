create view allusersbets as select
email, g.game_id,
g.visitor, g.visitor_score,
g.home, g.home_score,
g.date, g.time, 
b.status, g.complete,
b.bet_type, b.margin, b.american_odds, b.odds, b.result, b.winnings 
from games g, bets b where g.game_id = b.game_id;