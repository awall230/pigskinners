#!/usr/bin/env python

import cgi
import sqlite3
import os
import Cookie

import cgitb
cgitb.enable()

cookie_string = os.environ.get('HTTP_COOKIE')

conn = sqlite3.connect('../users.db')
c = conn.cursor()

if cookie_string:
    cook = Cookie.SimpleCookie(cookie_string)
    saved_session_id = cook['session_id'].value
    
    c.execute('select * from users where session_id=?', (saved_session_id,))
    account = c.fetchall()
    if len(account) > 0:
        email = account[0][0]
        first_name = account[0][2]
        last_name = account[0][3]
        fav_team = account[0][4]
        
        print 'Content-type: text/html'
        print
        
        print '<html>'
        print '<head><title>My Profile</title></head>'
        print '<body>'
        print '<h1>' + first_name + ' ' + last_name + '</h1>'
        print '<p>'
        print email
        print '</br>'
        print 'Fan of the ' + fav_team
        print '</p>'
        print '</body>'
        print '</html>'
else:
        print 'Content-type: text/html'
        print

        print '<html>'
        print '<head><title>Session Expired</title></head>'
        print '<body>'
        print '<p>Your session has expired.'
        print '<br/>'
        print 'Please <a href=./htdocs/login.html>log in</a> again.'
        print '</body>'
        print '</html>'
