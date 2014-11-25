create view alluserscontestbets as select
email, g.game_id,
g.visitor, g.visitor_score,
g.home, g.home_score,
g.date, g.time, 
cb.status, g.complete,
cb.bet_type, cb.margin, cb.american_odds,
cb.odds, cb.result, cb.winnings, cb.amount 
from games g, contestbets cb where g.game_id = cb.game_id;