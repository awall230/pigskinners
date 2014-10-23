#!/usr/bin/env python

import cgi
import sqlite3
import os
import Cookie
from xml.dom import minidom
import urllib2

import cgitb
cgitb.enable()

#cookie_string = os.environ.get('HTTP_COOKIE')
cookie_string = None

conn = sqlite3.connect('../users.db')
c = conn.cursor()
games_conn = sqlite3.connect('../games.db')
g = games_conn.cursor()

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
    g.execute('select game_id from games where team_a=? and team_b=? and date=?;',
              (game[0], game[3], game[8]))
    game_id = g.fetchall()
    if len(game_id) == 0:   #not in the database yet; add it
        g.execute('insert into games (game_id, team_a, team_b, date, time)'
                  'values(null, ?, ?, ?, ?);', (game[0], game[3], game[8], game[9]))
        games_conn.commit()
        g.execute('select game_id from games where team_a=? and team_b=? and date=?;',
              (game[0], game[3], game[8]))
        game_id = g.fetchall()[0][0]
        g.execute('insert into bets (bet_id, game_id, a_spread, b_spread, a_line, b_line, over_under, live)'
                  'values(null, ?, ?, ?, ?, ?, ?, ?);', 
                  (game_id, game[1], game[4], game[2], game[5], game[6], "True"))
        games_conn.commit()

g.execute('select * from bets;')
games = g.fetchall()

print 'Content-type: text/html'
print

print '<html>'
print '<head><title>Pigskinners -- Odds</title></head>'
print '<body>'
print '<p><a href=../index.html>Home</a></p>'
print '<h1>Current Odds</h1>'
print '<p>'
for game in games:
    for i in game:
        print i
    print '<br/><br/>'
print '</p>'
print '</body>'
print '</html>'