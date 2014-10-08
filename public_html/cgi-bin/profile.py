#!/usr/bin/env python

import cgi
import sqlite3

import cgitb
cgitb.enable()

form = cgi.FieldStorage()

first_name = form['first_name'].value
last_name = form['last_name'].value
email = form['email'].value
password = form['password'].value
fav_team = form['fav_team'].value

#first_name = 'Adam'
#last_name = 'Waller'
#email = 'test'
#password = 'testpw'
#fav_team = 'Giants'

conn = sqlite3.connect('../users.db')
c = conn.cursor()

try:
    c.execute("insert into users (email, password, first_name, last_name, fav_team)"
              "values (?,?,?,?,?);", (email, password, first_name, last_name, fav_team))
    conn.commit()
except sqlite3.IntegrityError:
    pass

c.execute("select * from users where email = ?;", (email,))
info = c.fetchall()[0]


print 'Content-type: text/html'
print

print '<html>'
print '<head><title>My Profile</title></head>'
print '<body>'
print '<h1>' + str(info[2]) + ' ' + str(info[3]) + '</h1>'
print '<p>'
print str(info[0])
print '</br>'
print 'Fan of the ' + str(info[4])
print '</p>'
print '</body>'
print '</html>'