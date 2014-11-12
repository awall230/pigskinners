#!/usr/bin/python

import cgi
import Cookie
import sqlite3
import os
import json
import game

import cgitb
cgitb.enable()

def main():

    data = {}	#container for json data
    data['bets'] = []
    
    cookie_string = os.environ.get('HTTP_COOKIE')
    
    conn = sqlite3.connect('../users.db')
    c = conn.cursor()
    
    form = cgi.FieldStorage()
    
    email = ""
    if cookie_string:   #user already has session id
        cook = Cookie.SimpleCookie(cookie_string)
        
        if 'session_id' in cook:
            saved_session_id = cook['session_id'].value
            
            #check if session id is valid
            c.execute('select * from users where session_id=?', (saved_session_id,))
            account = c.fetchall()
            if len(account) > 0:
                email = account[0][0]
    
    b = game.Bet()
    bet_id = form['bet_id'].value
    temp = bet_id.split('-')
    if 'num' in form:
        num = form['num'].value
    b.set_game_id(temp[0])   #same as game_id in games table
    b.set_bet_type(temp[1])  #int representing bet type
    
    #adding pick to db
    if form['action'].value == 'add':
        #check it they've already made this bet
        c.execute('select * from bets where email=? and game_id=? and bet_type=?;', (email, str(b.game_id), str(b.bet_type)))
        bets = c.fetchall()
        if len(bets) > 0:
            pass
        else:	#new bet, write it to database
            temp = get_odds(num, b.bet_type)
            b.set_margin(temp[0])
            b.set_american_odds(temp[1])
            b.set_odds(temp[2])
            b.set_complete(0)
            c.execute('insert into bets (game_id, bet_type, email, margin, american_odds, odds) values (?,?,?,?,?,?);',
                      (str(b.game_id), str(b.bet_type), email, str(b.margin), str(b.american_odds), str(b.odds)))
            conn.commit()

            c.execute('select * from allusersbets where email=? and game_id=? and bet_type=?;',
                      (email, str(b.game_id), str(b.bet_type)))
            bet = c.fetchall()[0]
            b.set_visitor(bet[2])
            b.set_home(bet[4])
            b.set_datetime(bet[6] + ' ' + bet[7])
            b.set_status()

            #if new, make json string using object attributes (not callable eliminates methods)
            bet_info = [(attr, value.__str__()) for attr, value in b.__dict__.items() if not callable(value)]
            bet_info = dict(bet_info)
            data['bets'].append(bet_info)


        
    #deleting pick from db
    elif form['action'].value == 'delete':
        c.execute('delete from bets where email=? and game_id=? and bet_type=?;',
                  (email, str(b.game_id), str(b.bet_type)))
        conn.commit()
        
    #print JSON (empty if deleting pick)
    print "Content-type: application/json"
    print
    print json.dumps(data)
        

def get_odds(num, bet):
    margin = 0.0
    odds = 1.0
    american_odds = 100.0
    num = float(num)
    bet = int(bet)
    #spread or over/under: margin is the value passed through cgi, pays even odds
    if bet == 0 or bet == 1 or bet == 4 or bet ==5:
        margin = num
    #moneyline: odds are passed through cgi, convert to "x to y" odds
    elif bet == 2 or bet == 3:
        american_odds = num
        if num > 0:
            odds = num/100.0
        elif num < 0:
            odds = -100.0/num
    return (margin, american_odds, odds)


main()