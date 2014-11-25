#!/usr/bin/env python

import cgi
import sqlite3
import os
import Cookie
from xml.dom import minidom
import urllib2
import game
from datetime import datetime, date, time
import json

import cgitb
#cgitb.enable()

cookie_string = os.environ.get('HTTP_COOKIE')
#cookie_string = None

conn = sqlite3.connect('../users.db')
c = conn.cursor()

form = cgi.FieldStorage()

f = urllib2.urlopen('http://www.referincome.com/odds/rss2/football_nfl.xml')
xmldoc = minidom.parse(f)
itemlist = xmldoc.getElementsByTagName('title')
home = ''
visitor = ''
home_spread = 0
visitor_spread = 0
home_moneyline = 0
visitor_moneyline = 0
over = 0
under = 0
d = ""
t = ""

data = {}	#container for json data
data['odds'] = []

odds = []

for i in range(1, len(itemlist)-1):
	g = game.Game() #new Game object for each game
	game_data = itemlist[i].childNodes[0].nodeValue
	if 'Q' in game_data: #eliminate bets on individual quarters
		continue
	game_data = game_data.split('|')
	for j in range(len(game_data)):
		game_data[j] = game_data[j].split()

	#info for visiting team
	j = 0
	visitor = ''
	while True:
		try:
			float(game_data[0][j])
		except:
			visitor += game_data[0][j] + ' '
			j += 1
		else:
			visitor = visitor[:-1]
			g.set_visitor(visitor)
			break
	if j < len(game_data[0]):
		visitor_spread = float(game_data[0][j])
		g.set_visitor_spread(visitor_spread)
#            j += 2  #skip the 'O' for over
		j += 1
	if j < len(game_data[0]):
		if game_data[0][j] == 'O':
			j += 1
			over = float(game_data[0][j][1:-1])  #lose the parentheses
			g.set_over(over)
			j += 1
	if j < len(game_data[0]):
		visitor_moneyline = float(game_data[0][j])
		g.set_visitor_moneyline(visitor_moneyline)

	#info for home team
	j = 0
	home = ''
	while True:
		try:
			float(game_data[1][j])
		except:
			home += game_data[1][j] + ' '
			j += 1
		else:
			home = home[:-1] #remove last space
			g.set_home(home)
			break
	
	#don't need range checks for home data--just find the date/time portion
	home_spread = float(game_data[1][j])
	g.set_home_spread(home_spread)
#            j += 2  #skip the 'U' for under
	j += 1
	if game_data[1][j] == 'U':  #game has an under
		j += 1
		under = float(game_data[1][j][1:-1])  #lose the parentheses
		g.set_under(under)
		j += 1
	
	#check if game has a moneyline
	try:
		float(game_data[1][j])
	except: #it doesn't, move on to date
		pass
	else:   #it does, add it to g
		home_moneyline = float(game_data[1][j])
		g.set_home_moneyline(home_moneyline)
		j += 1
	
	#date/time
	d = game_data[1][j][1:] + ' ' + game_data[1][j+1] + ' ' + game_data[1][j+2]
	t = game_data[1][j+3] + ' ' + game_data[1][j+4][:-1]
	#make datetime object from feed's date and time strings
	dt = datetime.strptime(str(d + ' ' + t), '%b %d, %Y %I:%M %p')
	g.set_datetime(dt)

	odds.append(g)

#check to make sure database is up to date
current_week = game.get_week(date.today())
for g in odds:
	c.execute('select game_id from games where home=? and visitor=? and date=?;',
			  (g.home, g.visitor, g.d.__str__()))
	game_id = c.fetchall()    #inside a tuple inside a list
	if len(game_id) == 0:   #not in the database yet; add it
		c.execute('insert into games (game_id, home, visitor, date, time, week)'
				  'values(null, ?, ?, ?, ?, ?);', (g.home, g.visitor, g.d.__str__(), time.strftime(g.t, '%H:%M'), g.week))
		conn.commit()

	c.execute('select game_id from games where visitor=? and home=? and date=?;',
		(g.visitor, g.home, g.d.__str__()))
	game_id = c.fetchall()[0][0]
	g.set_game_id(game_id)
		
	game_info = [(attr, value.__str__()) for attr, value in g.__dict__.items() if not callable(value)]
	game_info = dict(game_info)
	if form['contest'].value == 'true':
		if g.week != current_week:
			continue	#can't wager on more than one week at once in contest
	data['odds'].append(game_info)
	
print "Content-type: application/json"
print
print json.dumps(data)