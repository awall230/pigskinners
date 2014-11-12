#!/usr/bin/env python

import sqlite3
import os
import Cookie
import json

import cgitb
cgitb.enable()

cookie_string = os.environ.get('HTTP_COOKIE')

conn = sqlite3.connect('../users.db')
c = conn.cursor()

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


data['logged_in'] = logged_in

#print JSON
print "Content-type: application/json"
print
print json.dumps(data)