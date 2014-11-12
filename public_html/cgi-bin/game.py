from datetime import datetime, date, time

#teams = {'ARI': 'Arizona Cardinals',
#	'ATL': 'Atlanta Falcons',
#	'BAL': 'Baltimore Ravens',
#	'BUF': 'Buffalo Bills',
#	'CAR': 'Carolina Panthers',
#	'CHI': 'Chicago Bears',
#	'CIN': 'Cincinnati Bengals',
#	'CLE': 'Cleveland Browns',
#	'DAL': 'Dallas Cowboys',
#	'DEN': 'Denver Broncos',
#	'DET': 'Detroit Lions',
#	'GB': 'Green Bay Packers',
#	'HOU': 'Houston Texans',
#	'IND': 'Indianapolis Colts',
#	'JAC': 'Jacksonville Jaguars',
#	'KC': 'Kansas City Chiefs',
#	'MIA': 'Miami Dolphins',
#	'MIN': 'Minnesota Vikings',
#	'NE': 'New England Patriots',
#	'NO': 'New Orleans Saints',
#	'NYG': 'New York Giants',
#	'NYJ': 'New York Jets',
#	'OAK': 'Oakland Raiders',
#	'PHI': 'Philadelphia Eagles',
#	'PIT': 'Pittsburgh Steelers',
#	'SD': 'San Diego Chargers',
#	'SEA': 'Seattle Seahawks',
#	'SF': 'San Francisco 49ers',
#	'STL': 'Saint Louis Rams',
#	'TB': 'Tampa Bay Buccaneers',
#	'TEN': 'Tennessee Titans',
#	'WAS': 'Washington Redskins'}

teams = {'ARI': 'Arizona',
	'ATL': 'Atlanta',
	'BAL': 'Baltimore',
	'BUF': 'Buffalo',
	'CAR': 'Carolina',
	'CHI': 'Chicago',
	'CIN': 'Cincinnati',
	'CLE': 'Cleveland',
	'DAL': 'Dallas',
	'DEN': 'Denver',
	'DET': 'Detroit',
	'GB': 'Green Bay',
	'HOU': 'Houston',
	'IND': 'Indianapolis',
	'JAC': 'Jacksonville',
	'KC': 'Kansas City',
	'MIA': 'Miami',
	'MIN': 'Minnesota',
	'NE': 'New England',
	'NO': 'New Orleans',
	'NYG': 'NY Giants',
	'NYJ': 'NY Jets',
	'OAK': 'Oakland',
	'PHI': 'Philadelphia',
	'PIT': 'Pittsburgh',
	'SD': 'San Diego',
	'SEA': 'Seattle',
	'SF': 'San Francisco',
	'STL': 'St. Louis',
	'TB': 'Tampa Bay',
	'TEN': 'Tennessee',
	'WAS': 'Washington'}
	
#create reverse dictionary for looking up abbreviations from full team name
teams_reverse = dict((b,a) for (a, b) in teams.items())

class Game(object):
	
	def __init__(self):
		pass
		
	def set_game_id(self, gid):
		self.game_id = int(gid)
		
	def set_home(self, h):
		if len(h) > 3:
			h = teams_reverse[fix_team_name(h)]
		self.home = h
		self.home_name = teams[self.home]
	
	def set_visitor(self, v):
		if len(v) > 3:
			v = teams_reverse[fix_team_name(v)]
		self.visitor = v
		self.visitor_name = teams[self.visitor]
		
	def set_home_score(self, hs):
		self.home_score = int(hs)
	
	def set_visitor_score(self, vs):
		self.visitor_score = int(vs)
		
	def set_home_spread(self, hs):
		self.home_spread = float(hs)
	
	def set_visitor_spread(self, vs):
		self.visitor_spread = float(vs)
	
	def set_home_moneyline(self, hml):
		self.home_moneyline = float(hml)
	
	def set_visitor_moneyline(self, vml):
		self.visitor_moneyline = float(vml)
		
	def set_over(self, o):
		self.over = float(o)
		self.under = float(o)
	
	def set_under(self, u):
		self.set_over(u)
	
	def set_datetime(self, dt):
		if not isinstance(dt, datetime):
			dt = datetime.strptime(str(dt), '%Y-%m-%d %H:%M')
		self.dt = dt
		self.d = dt.date()
		self.t = dt.time()
		
	def set_status(self):
		if self.dt > datetime.today():	#hasn't started yet
			self.status = "open"
		else:
			self.status = "closed"
	
	def set_complete(self, c):
		self.complete = (int(c) == 1)	#sqlite uses 0 and 1 for boolean values
		
	def set_home_score(self, hs):
		self.home_score = int(hs)
	
	def set_visitor_score(self, vs):
		self.visitor_score = int(vs)
		
class Bet(Game):
	
	def __init__(self):
	    self.margin = 0.0
	    self.odds = 1.0
	    self.american_odds = 100.0
	
	def set_game_id(self, gid):
		self.game_id = int(gid)
	
	def set_margin(self, m):
		self.margin = float(m)
	
	def set_odds(self, i):
		self.odds = float(i)
	
	def set_american_odds(self, a):
		self.american_odds = float(a)

	def set_bet_type(self, b):
		self.bet_type = int(b)
		
	def set_result(self, r):
		self.result = int(r)
		self.set_winnings()
	
	def set_winnings(self):
		if self.result > 0:
			self.winnings = 100.0 * self.odds
		elif self.result == 0:
			self.winnings = 0
		else:
			self.winnings = -100.0
		
def fix_team_name(name):
	if name == "New York-A":
		name = "NY Jets"
	elif name == "New York-N":
		name = "NY Giants"
	elif name == "Phila.":
		name = "Philadelphia"
	elif name == "San Fran.":
		name = "San Francisco"
	return name
