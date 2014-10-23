#!/usr/bin/env python

import cgi
import sqlite3
import Cookie
import time

import cgitb
cgitb.enable()

conn = sqlite3.connect('../users.db')
c = conn.cursor()

def main():

    form = cgi.FieldStorage()
    
    #should have email and pw regardless of whether user is coming from registration or login
    if form['last_page'].value == 'registration':
        if not ('email' in form and 'password' in form and 'first_name' in form and 'last_name' in form and 'fav_team' in form and 'password2' in form): #didn't fully complete registration form
                #redirect back to register.html with error=incomplete_registration
            print 'Content-type: text/html'
            print
    
            print '<html>'
            print '<head>'
            print '<title>Pigskinners</title>'
            print '<meta http-equiv="refresh" content="1; url=register.py?error=incomplete_registration" />'
            print '</head>'
            print '</html>'
            
            return
        
        elif form['password'].value != form['password2'].value: #passwords don't match, redirect to registration
            print 'Content-type: text/html'
            print
    
            print '<html>'
            print '<head>'
            print '<title>Pigskinners</title>'
            print '<meta http-equiv="refresh" content="1; url=register.py?error=different_passwords" />'
            print '</head>'
            print '</html>'
            
            return
    
    elif form['last_page'].value == 'login':
#        print 'Content-type: text/html'
#        print 
#        print not ('email' in form and 'password' in form)
        if not ('email' in form and 'password' in form): #didn't fully complete login
            #redirect back to login.py with error=incomplete_login
            print 'Content-type: text/html'
            print
    
            print '<html>'
            print '<head>'
            print '<title>Pigskinners</title>'
            print '<meta http-equiv="refresh" content="1; url=login.py?error=incomplete_login" />'
            print '</head>'
            print '</html>'
            
            return
        
    email = form['email'].value
    password = form['password'].value
    #see if email is in users database
    c.execute("select * from users where email = ?;", (email,))
    account = c.fetchall()
    
    if form['last_page'].value == 'registration':   #just submitted registration form
        if len(account) > 0:    #e-mail already in database
            print 'Content-type: text/html'
            print
    
            print '<html>'
            print '<head><title>Error</title></head>'
            print '<body>'
            print '<p>E-mail address already registered.'
            print '<br/>'
            print 'Please <a href=register.py>register with a different e-mail address.</a>'
            print '<br/>'
            print 'Or <a href=login.py>log in.</a>'
            print '</p>'
            print '</body>'
            print '</html>'
        else:   #valid new account
            #write to database
            first_name = form['first_name'].value
            last_name = form['last_name'].value
            fav_team = form['fav_team'].value
            c.execute("insert into users (email, password, first_name, last_name, fav_team)"
                  "values (?,?,?,?,?);", (email, password, first_name, last_name, fav_team))
            conn.commit()
            #send cookie with sessionid
            #redirect to profile.py
            login(email)
            
    
    
    elif form['last_page'].value == 'login':    #just tried to log in
        #see if email and password match database
        c.execute("select * from users where email = ? AND password = ?;", (email, password))
        account = c.fetchall()
        if len(account) == 0:   #no match in database
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
            #success, send cookie with sessionid
            #redirect to profile.py
            login(email)
    
def login(email_address):
    """Sends cookie to user with unique session id, and redirects to profile.py"""
    
    import uuid
    session_id = str(uuid.uuid4())
    c.execute('update users set session_id=? where email=?', (session_id, email_address))
    conn.commit()
    cook = Cookie.SimpleCookie()		#create the cookie
    cook['session_id'] = session_id		#assign a value
    cook['session_id']['expires'] = 20 * 60	#set expiration time to 20min
    						#returns to login page if once timed out
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