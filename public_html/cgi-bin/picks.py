#!/usr/bin/env python

import cgi
import sqlite3
import os
import Cookie
from xml.dom import minidom
import urllib2

import cgitb
#cgitb.enable()

cookie_string = os.environ.get('HTTP_COOKIE')
#cookie_string = None

conn = sqlite3.connect('../users.db')
c = conn.cursor()

logged_in = False
first_name = ""

if cookie_string:   #user already has session id
    cook = Cookie.SimpleCookie(cookie_string)
    saved_session_id = cook['session_id'].value
    
#    check if session id is valid
    c.execute('select * from users where session_id=?', (saved_session_id,))
    account = c.fetchall()
    if len(account) > 0:
        logged_in = True
        first_name = account[0][2]

if not logged_in:
    print 'Content-type: text/html'
    print

    print '<html>'
    print '<head>'
    print '<title>Please log in</title>'
    print '</head>'
    print '<body>'
    print '<h3>Please <a href=login.py>log in </a> to make picks.</h3>'
    print '</body>'
    print '</html>'

else:   #logged in
    f = urllib2.urlopen('http://www.referincome.com/odds/rss2/football_nfl.xml')
    xmldoc = minidom.parse(f)
    itemlist = xmldoc.getElementsByTagName('title')
    team_a = ''
    team_b = ''
    spread_a = 0
    spread_b = 0
    money_line_a = 0
    money_line_b = 0
    over = 0
    under = 0
    date_string = ""
    time_string = ""
    
    odds = []
    
    for i in range(1, len(itemlist)-1):
        game = itemlist[i].childNodes[0].nodeValue
        if 'Q' in game: #eliminate bets on individual quarters
            continue
        game = game.split('|')
        for j in range(len(game)):
            game[j] = game[j].split()
    
        #info for team a
        j = 0
        team_a = ''
        while True:
            try:
                float(game[0][j])
            except:
                team_a += game[0][j] + ' '
                j += 1
            else:
                team_a = team_a[:-1]
                break
        spread_a = float(game[0][j])
        j += 2  #skip the 'O' for over
        over = float(game[0][j][1:-1])  #lose the parentheses
        j += 1
        money_line_a = float(game[0][j])
    
        #info for team b
        j = 0
        team_b = ''
        while True:
            try:
                float(game[1][j])
            except:
                team_b += game[1][j] + ' '
                j += 1
            else:
                team_b = team_b[:-1] #remove last space
                break
        spread_b = float(game[1][j])
        j += 2  #skip the 'U' for under
        under = float(game[1][j][1:-1])  #lose the parentheses
        j += 1
        money_line_b = float(game[1][j])
        j += 1
        
        #date/time
        date_string = game[1][j][1:] + ' ' + game[1][j+1] + ' ' + game[1][j+2]
        time_string = game[1][j+3] + ' ' + game[1][j+4][:-1]
    
        odds.append([team_a, spread_a, money_line_a, team_b, spread_b, money_line_b,
                     over, under, date_string, time_string])
    
    #check to make sure database is up to date
    for game in odds:
        c.execute('select game_id from games where team_a=? and team_b=? and date=?;',
                  (game[0], game[3], game[8]))
        game_id = c.fetchall()    #inside a tuple inside a list
        if len(game_id) == 0:   #not in the database yet; add it
            c.execute('insert into games (game_id, team_a, team_b, date, time)'
                      'values(null, ?, ?, ?, ?);', (game[0], game[3], game[8], game[9]))
            conn.commit()
    #        c.execute('select game_id from games where team_a=? and team_b=? and date=?;',
    #              (game[0], game[3], game[8]))
    #        game_id = c.fetchall()[0][0]
    #        c.execute('insert into bets (bet_id, game_id, a_spread, b_spread, a_line, b_line, over_under, live)'
    #                  'values(null, ?, ?, ?, ?, ?, ?, ?);', 
    #                  (game_id, game[1], game[4], game[2], game[5], game[6], "True"))
    #        conn.commit()
    
    #c.execute('select * from bets;')
    #games = c.fetchall()
    
    print 'Content-type: text/html'
    print
    
    print '<html>'
    print '<head><title>Pigskinners -- Odds</title></head>'
    print '<body>'
    print '<p><a href=../index.html>Home</a>'
    print " | <a href=profile.py>" + first_name + "'s profile</a>"
    print ' | <a href=logout.py>Log out</a></p>'
    print '<h1>Current Odds</h1>'
    print '<p>'
    
    print '<form name="input" action="process_picks.py" method="post">'
    
    for game in odds:
        c.execute('select game_id from games where team_a=? and team_b=? and date=?;',
                  (game[0], game[3], game[8]))
        game_id = c.fetchall()[0][0]
        print '<b>' + game[0] + ' @ ' + game[3] + '</b>'
        print '<br/>'
        
        #spread (spread a is bet type 0, spread b is bet type 1)
        print 'Spread: <input type="checkbox" name="' + str(game_id) + '-0" value="' + str(game[1]) + '">'
        print game[0] + ' ' + str(game[1])
        print ' <input type="checkbox" name="' + str(game_id) + '-1" value="' + str(game[4]) + '">'
        print game[3] + ' ' + str(game[4])
        print '<br/>'
        
        #moneyline (ml a is bet type 2, ml b is bet type 3)
        print 'Moneyline: <input type="checkbox" name="' + str(game_id) + '-2" value="' + str(game[2]) + '">'
        print game[0] + ' ' + str(game[2])
        print ' <input type="checkbox" name="' + str(game_id) + '-3" value="' + str(game[5]) + '">'
        print game[3] + ' ' + str(game[5])
        print '<br/>'
        
        #over is bet type 4, under is bet type 5
        print 'Over/Under: <input type="checkbox" name="' + str(game_id) + '-4" value="' + str(game[6]) + '">'
        print 'Over ' + str(game[6])
        print ' <input type="checkbox" name="' + str(game_id) + '-5" value="' + str(game[6]) + '">'
        print 'Under ' + str(game[6])
        print '<br/>'

        print game[8] + ' ' + game[9]
        print '<br/><br/>'
    
    print '<input type="submit"> <input type="reset">'
    
    print '</form>'
    print '</p>'
    print '</body>'
    print '</html>'