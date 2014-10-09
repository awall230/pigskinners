#!/usr/bin/env python

import cgi
import sqlite3
import Cookie

import cgitb
cgitb.enable()

conn = sqlite3.connect('./users.db')
c = conn.cursor()

def main():

    form = cgi.FieldStorage()
    email = form['email'].value
    password = form['password'].value
    c.execute("select * from users where email = ?;", (email,))
    account = c.fetchall()
    
    if form['last_page'].value == 'registration':
        if len(account) > 0:
            print 'Content-type: text/html'
            print
    
            print '<html>'
            print '<head><title>Error</title></head>'
            print '<body>'
            print '<p>E-mail address already registered.'
            print '<br/>'
            print 'Please <a href=../register.html>register with a different e-mail address.</a>'
            print '<br/>'
            print 'Or <a href=login.py>log in.</a>'
            print '</p>'
            print '</body>'
            print '</html>'
        else:
            #write to database
            #send cookie with e-mail and sessionid
            #redirect to profile.py
            first_name = form['first_name'].value
            last_name = form['last_name'].value
            fav_team = form['fav_team'].value
            c.execute("insert into users (email, password, first_name, last_name, fav_team)"
                  "values (?,?,?,?,?);", (email, password, first_name, last_name, fav_team))
            conn.commit()
            login(email)
            
    
    
    elif form['last_page'].value == 'login':
        c.execute("select * from users where email = ? AND password = ?;", (email, password))
        account = c.fetchall()
        if len(account) == 0:
            #redirect back to login.py with error=bad_login
            print 'Content-type: text/html'
            print
    
            print '<html>'
            print '<head>'
            print '<title>Pigskinners</title>'
            print '<meta http-equiv="refresh" content="1; url=login.py?error=bad_login" />'
            print '</head>'
            print '</html>'
            
        else:
            #send cookie with e-mail and sessionid
            #redirect to profile.py
            login(email)
    
def login(email_address):
    import uuid
    session_id = str(uuid.uuid4())
    c.execute('update users set session_id=? where email=?', (session_id, email_address))
    conn.commit()
    cook = Cookie.SimpleCookie()
    cook['session_id'] = session_id
    
    print 'Content-type: text/html'
    print cook
    print

    print '<html>'
    print '<head>'
    print '<title>Pigskinners</title>'
    print '<meta http-equiv="refresh" content="1; url=profile.py" />'
    print '</head>'
#    print '<body>'
#    print '<p><a href=profile.py>Profile</a></p>'
#    print '</body>'
    print '</html>'
    
main()