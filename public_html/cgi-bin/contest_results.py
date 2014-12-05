#!/usr/bin/python

import cgi
import sqlite3
import json
import game
from datetime import date, time, datetime, timedelta

import cgitb
cgitb.enable()

data = {}	#container for json data

conn = sqlite3.connect('../users.db')
c = conn.cursor()

form = cgi.FieldStorage()

#email = 'awaller@u.rochester.edu'
# email = ""
# if 'email' in form:
# 	email = form['email'].value

c.execute('select email from users;')
users = c.fetchall()
ranks = []	#will ultimately store results
last_week = game.get_week(date.today() - timedelta(days=7))

for user in users:
	c.execute('select winnings, date, time from alluserscontestbets where email=? and winnings not null;', (user[0],))
	bets = c.fetchall()

	bet_count = len(bets)
	total_winnings = 0
	average_winnings = 0

	if bet_count > 0:
		bet_count = 0
		for bet in bets:
			b = game.Bet()
			b.set_datetime(bet[1] + ' ' + bet[2])
			if b.week == last_week:
				total_winnings += float(bet[0]);
				bet_count += 1
		average_winnings = total_winnings / bet_count
		ranks.append((average_winnings, total_winnings, bet_count, user[0]))

	# if email: #want info for a specific user's profile
	# 	if user[0] == email:	#this is the user's data
	# 		data['total_winnings'] = '{0:.2f}'.format(total_winnings)
	# 		data['average_winnings'] = '{0:.2f}'.format(average_winnings)

ranks.sort(reverse=True);	#sort by average winnings

# if email:	#want info for a specific user's profile
# 	for i in range(len(ranks)):
# 		if ranks[i][3] == email:
# 			data['rank'] = i+1
# 			data['user_count'] = len(ranks)	#only consider users who have completed bets in user count
# 			break

#else:	#this is for displaying global leaderboard
data['leaders'] = []
for i in range(len(ranks)):
	data['leaders'].append( {'rank': i, 'email': ranks[i][3], 'average_winnings': '{0:.2f}'.format(ranks[i][0]),
		'total_winnings': '{0:.2f}'.format(ranks[i][1]), 'bet_count': ranks[i][2]} )

#print JSON
print "Content-type: application/json"
print
print json.dumps(data)