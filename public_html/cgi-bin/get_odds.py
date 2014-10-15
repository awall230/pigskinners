#!/usr/bin/env python

from xml.dom import minidom
import urllib2

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
            break
    spread_b = float(game[1][j])
    j += 2  #skip the 'U' for under
    under = float(game[1][j][1:-1])  #lose the parentheses
    j += 1
    money_line_b = float(game[1][j])

    odds.append([team_a, spread_a, money_line_a, team_b, spread_b, money_line_b, over, under])

#for i in odds:
#    print i

print 'Content-type: text/html'
print

print '<html>'
print '<head><title>Pigskinners -- Odds</title></head>'
print '<body>'
print '<p><a href=../index.html>Home</a></p>'
print '<h1>Current Odds</h1>'
print '<p>'
for game in odds:
    print '<b>' + game[0] + ' @ ' + game[3] + '</b>'
    print '<br/>'
    print 'Spread: ' + game[0] + ' ' + str(game[1]) + ' | ' + game[3] + ' ' + str(game[4])
    print '<br/>'
    print 'Moneyline: ' + game[0] + ' ' + str(game[2]) + ' | ' + game[3] + ' ' + str(game[5])
    print '<br/>'
    print 'Over/Under: ' + str(game[6])
    print '<br/><br/>'
print '</p>'
print '</body>'
print '</html>'
