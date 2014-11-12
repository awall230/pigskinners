from xml.dom import minidom
from datetime import datetime, date, time
import urllib2
import sqlite3
import game

f = urllib2.urlopen('http://www.nfl.com/liveupdate/scorestrip/ss.xml')
xmldoc = minidom.parse(f)
itemlist = xmldoc.getElementsByTagName('g') #get list of all games for the week

conn = sqlite3.connect('../users.db')
c = conn.cursor()

for item in itemlist:
	item = item.attributes
	g = game.Game()
	d = str(item['eid'].value[:-2])
	d = date(int(d[0:4]), int(d[4:6]), int(d[6:8]))
	t = (item['t'].value).split(':')
	t = time(int(t[0]) + 12, int(t[1]))
	dt = datetime.combine(d, t)
	g.set_datetime(dt)
	
	home = game.teams[str(item['h'].value)]
	g.set_home(home)
	visitor = game.teams[str(item['v'].value)]
	g.set_visitor(visitor)
	hscore = item['hs'].value
	g.set_home_score(hscore)
	vscore = item['vs'].value
	g.set_visitor_score(vscore)
	complete = ('F' in str(item['q'].value))
	g.set_complete(complete)
	g.set_status()
	
	c.execute('select * from games where visitor=? and home=? and date=?;',
	         (g.visitor, g.home, g.d.__str__()))
	results = c.fetchall()
	if len(results) == 0:	#not in db yet, add it
		c.execute('insert into games (game_id, visitor, home, visitor_score,'
		          'home_score, date, time, status, complete)'
		          'values (null, ?,?,?,?,?,?,?,?);',
		          (g.visitor, g.home, g.visitor_score, g.home_score, g.d.__str__(),
		          time.strftime(g.t, '%H:%M'), g.status, g.complete))
		conn.commit()
	else:
		g.set_game_id(results[0][0])
		c.execute('update games set visitor_score=?, home_score=?, time=?, status=?, complete=?'
		          'where game_id=?;', (g.visitor_score, g.home_score, 
		          time.strftime(g.t, '%H:%M'), g.status, g.complete, g.game_id))
		conn.commit()
	
		
	
def check_bet(b):
	if b.bet_type == 0 or b.bet_type == 1:	
		if b.bet_type == 0:		#spread, visiting team
			diff = b.home_score - b.visitor_score
		else:					#spread, home team
			diff = b.visitor_score - b.home_score
		if diff < b.margin:
			return 1		#win
		elif diff == b.margin:
			return 0		#push
		else:
			return -1		#lose
	elif b.bet_type == 2:		#moneyline, visiting team
		if b.visitor_score > b.home_score:
			return 1
		elif b.visitor_score == b.home_score:
			return 0
		else:
			return -1
	elif b.bet_type == 3:		#moneyline, home team
		if b.home_score > b.visitor_score:
			return 1
		elif b.home_score == b.visitor_score:
			return 0
		else:
			return -1
	elif b.bet_type == 4:		#over
		if (b.home_score + b.visitor_score) > b.margin:
			return 1
		elif (b.home_score + b.visitor_score) == b.margin:
			return 0
		else:
			return -1
	elif b.bet_type == 5:		#under
		if (b.home_score + b.visitor_score) < b.margin:
			return 1
		elif (b.home_score + b.visitor_score) == b.margin:
			return 0
		else:
			return -1
