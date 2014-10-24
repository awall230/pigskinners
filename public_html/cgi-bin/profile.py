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

if cookie_string:   #user already has session id
    cook = Cookie.SimpleCookie(cookie_string)
    
    if 'session_id' in cook:
        saved_session_id = cook['session_id'].value
        
        
        #check if session id is valid
        c.execute('select * from users where session_id=?', (saved_session_id,))
        account = c.fetchall()
        if len(account) > 0:
            email = account[0][0]
            first_name = account[0][2]
            last_name = account[0][3]
            fav_team = account[0][4]
            
            #display profile information
            print 'Content-type: text/html'
            print
            
            print '<html>'
            print '<head><title>My Profile</title></head>'
            print '<body>'
            print '<p><a href=../index.html>Home</a> | <a href=logout.py>Log Out</a>'
            print ' | <a href=picks.py>Make picks</a></p>'
            print '<h1>' + first_name + ' ' + last_name + '</h1>'
            print '<h3>YOU ARE NOW LOGGED IN</h3>'
            #print '<h1>first_name + ' ' + last_name + ' , you are now logged in</h1>'
            
            print '<p>'
            print email
            print '<br/>'
            print 'Fan of the ' + fav_team
            print '<br/><br/>'
            print '</p>'
            print '<h2>Your picks:</h2>'
            print '<p>'
            c.execute('select * from allusersbets where email=?;', (email,))
            bets = c.fetchall()
            for bet in bets:
                #bet_type is at bet[7]
                bet_type = int(bet[7])
                #bold user's pick
                if bet_type == 0 or bet_type == 2:
                    print '<b>' + bet[2] + '</b> @ ' + bet[3]
                elif bet_type == 1 or bet_type == 3:
                    print bet[2] + ' @ <b>' + bet[3] + '</b>'
                elif bet_type == 4 or bet_type == 5:
                    print bet[2] + ' @ ' + bet[3]
                if bet_type == 0 or bet_type == 1:
                    print ' | Spread | ' + str(bet[8])
                elif bet_type == 2 or bet_type == 3:
                    print ' | Moneyline | ' + str(bet[9])
                elif bet_type == 4:
                    print ' | ' + '<b>Over</b>/Under | ' + str(bet[8])
                elif bet_type == 5:
                    print ' | ' + 'Over/<b>Under</b> | ' + str(bet[8])
                
                print '<br/>'
                print bet[4] + ', ' + bet[5]
                print '<br/><br/>'
            print '</p>'
            print '</body>'
            print '</html>'
        else:   
            #session id not valid
            print 'Content-type: text/html'
            print
    
            print '<html>'
            print '<head><title>Session Expired</title></head>'
            print '<body>'
            print '<p>Your session has expired.'
            print '<br/>'
            print 'Please <a href=login.py>log in</a> again.'
            print '</body>'
            print '</html>'
    else:
        #no session_id
        print 'Content-type: text/html'
        print

        print '<html>'
        print '<head><title>Session Expired</title></head>'
        print '<body>'
        print '<p>Your session has expired.'
        print '<br/>'
        print 'Please <a href=login.py>log in</a> again.'
        print '</body>'
        print '</html>'
else:   #no cookie, redirect to login
    print 'Content-type: text/html'
    print

    print '<html>'
    print '<head>'
    print '<title>Pigskinners</title>'
    print '<meta http-equiv="refresh" content="1; url=login.py" />'
    print '</head>'
    print '</html>'
