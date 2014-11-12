#!/usr/bin/env python

import cgi
import sqlite3
import os
import Cookie
import game
from datetime import datetime, date, time
import get_results  #updates database with latest scores
import json

import cgitb
cgitb.enable()

cookie_string = os.environ.get('HTTP_COOKIE')

conn = sqlite3.connect('../users.db')
c = conn.cursor()

cook = Cookie.SimpleCookie(cookie_string)
saved_session_id = cook['session_id'].value
        
data = {}    #container for json data
data['bets'] = []
        
#check if session id is valid
c.execute('select * from users where session_id=?', (saved_session_id,))
account = c.fetchall()
if len(account) > 0:
#if True:
    email = account[0][0]
    first_name = account[0][2]
    last_name = account[0][3]
    fav_team = account[0][4]
#    email = 'awaller@u.rochester.edu'
#    first_name = 'Adam'
#    last_name = 'Waller'
#    fav_team = 'New York Giants'
    
    c.execute('select * from allusersbets where email=?;', (email,))
    bets = c.fetchall()
    
    for bet in bets:
        b = game.Bet()
        #bet_type is at bet[10]
        b.set_bet_type(int(bet[10]))
        b.set_game_id(int(bet[1]))
        b.set_visitor(bet[2])
        b.set_home(bet[4])
        b.set_datetime(str(bet[6]) + ' ' + str(bet[7]))
        b.set_margin(float(bet[11]))
        b.set_american_odds(float(bet[12]))
        b.set_odds(float(bet[13]))
        if bet[9] != None:
            b.set_complete(bet[9])
        else:
            b.set_complete(0)
        b.set_status()
        
        if b.complete:
            #assess bet if not already done
            b.set_visitor_score(bet[3])
            b.set_home_score(bet[5])
            if bet[14] != None:     #already assessed
                b.set_result(bet[14])   #also calculates winnings
            else:   #hasn't been assessed yet
                result = get_results.check_bet(b)
                b.set_result(result)
            
            #write results to db
            c.execute('update bets set result=?, winnings=?, status=? where email=? and game_id=? and bet_type=?;', (b.result, b.winnings, b.status, email, b.game_id, b.bet_type))
            conn.commit()
            
        else: #just update the bet status (open or closed)
            c.execute('update bets set status=? where email=? and game_id=? and bet_type=?;',
                      (b.status, email, b.game_id, b.bet_type))
            conn.commit()
            
        #make json string using object attributes (not callable eliminates methods)
        bet_info = [(attr, value.__str__()) for attr, value in b.__dict__.items() if not callable(value)]
        bet_info = dict(bet_info)
        data['bets'].append(bet_info)


    #sort by date and print JSON
    temp = sorted(data['bets'], key=lambda k: k['dt'])
    data['bets'] = temp
    print "Content-type: application/json"
    print
    print json.dumps(data)