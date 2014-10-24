create table bets(
    game_id integer not null,
    bet_type integer not null,
    email varchar(100) not null,
    margin float,
    american_odds float,
    odds float,
    status varchar(10),
    primary key (game_id, bet_type, email)
    );