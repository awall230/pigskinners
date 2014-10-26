#!/usr/bin/env python

import sqlite3
import os
import Cookie

import cgitb
cgitb.enable()

cookie_string = os.environ.get('HTTP_COOKIE')

conn = sqlite3.connect('../users.db')
c = conn.cursor()

logged_in = False
first_name = ""

if cookie_string:   #user already has session id
    cook = Cookie.SimpleCookie(cookie_string)
    if 'session_id' in cook:
        saved_session_id = cook['session_id'].value
        
        #check if session id is valid
        c.execute('select * from users where session_id=?', (saved_session_id,))
        account = c.fetchall()
        if len(account) > 0:
            logged_in = True
            first_name = account[0][2]

#make JSON string indicating whether logged in or not
login_string = '{"logged_in": "' + str(logged_in) + '"'
if logged_in:
    login_string += ', "first_name": "' + first_name + '"}'
else:
    login_string += '}'

#print JSON
print "Content-type: application/json"
print
print login_string