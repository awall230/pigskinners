create table games(
    game_id integer primary key,
    visitor varchar(10),
    visitor_score integer,
    home varchar(10),
    home_score integer,
    date varchar(10),
    time varchar(10),
    status varchar(10),
    complete integer
    );