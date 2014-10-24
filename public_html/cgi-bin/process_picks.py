#!/usr/bin/python

import cgi
import Cookie
import sqlite3
import os

import cgitb
cgitb.enable()

def main():
    
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
    
    for bet in form.keys():
        temp = bet.split('-')
        info = form[bet].value
        game_id = temp[0]   #same as game_id in games table
        bet_type = temp[1]  #int representing bet type
        #check it they've already made this bet
        c.execute('select * from bets where email=? and game_id=? and bet_type=?', (email, game_id, bet_type))
        bets = c.fetchall()
        if len(bets) > 0:
            continue
        #new bet, write it to database
        else:
            temp = get_odds(info, bet_type)
            c.execute('insert into bets (game_id, bet_type, email, margin, american_odds, odds) values (?,?,?,?,?,?);',
                      (game_id, bet_type, email, temp[0], temp[1], temp[2]))
            conn.commit()
        
    
    print 'Content-type: text/html'
    print
    print '<html>'
    print '<head>'
    print '<title>Pigskinners</title>'
    print '<meta http-equiv="refresh" content="1; url=profile.py" />'
    print '</head>'
    print '</html>'
 #   print '<body>'
#    print len(form)
#    for x in form.keys():
#        print x.split('-')[0] + ' | ' + x.split('-')[1] + ' | ' + str(form[x].value)
#        print '<br/>'



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
            odds = 100.0/num
    return (margin, american_odds, odds)


main()


#print len(form)
#for x in form.keys():
#    print x.split('-')[0] + ' | ' + x.split('-')[1] + ' | ' + str(form[x].value)
#    print '<br/>'
#print '<html><head><title>Process Picks></title></head>'
#print '<body><p>Data here</p></body></html>'
