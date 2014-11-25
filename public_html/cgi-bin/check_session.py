#!/usr/bin/env python

import sqlite3
import os
import Cookie
import json
import cgi

import cgitb
cgitb.enable()

cookie_string = os.environ.get('HTTP_COOKIE')

conn = sqlite3.connect('../users.db')
c = conn.cursor()

form = cgi.FieldStorage()

logged_in = False
data = {}	#will hold JSON data

if cookie_string:   #user already has session id
    cook = Cookie.SimpleCookie(cookie_string)
    if 'session_id' in cook:
        saved_session_id = cook['session_id'].value
        
        #check if session id is valid
        c.execute('select * from users where session_id=?', (saved_session_id,))
        account = c.fetchall()
        if len(account) > 0:
            logged_in = True
            data['email'] = account[0][0]
            data['first_name'] = account[0][2]
            data['last_name'] = account[0][3]
            data['fav_team'] = account[0][4]

if 'email' in form:
    user_email = form['email'].value
    c.execute('select * from users where email=?;', (user_email,))
    account = c.fetchall()
    data['user_email'] = user_email
    data['user_first_name'] = account[0][2]
    data['user_last_name'] = account[0][3]
    data['user_fav_team'] = account[0][4]

data['logged_in'] = logged_in

#print JSON
print "Content-type: application/json"
print
print json.dumps(data)