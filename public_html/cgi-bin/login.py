#!/usr/bin/env python

import cgi
import sqlite3
import os
import Cookie

import cgitb
cgitb.enable()

def main():
    
    cookie_string = os.environ.get('HTTP_COOKIE')
    
    conn = sqlite3.connect('../users.db')
    c = conn.cursor()
    
    print 'Content-type: text/html'
    
    if cookie_string:   #user already logged in, redirect to profile
        conn = sqlite3.connect('../users.db')
        c = conn.cursor()
        cook = Cookie.SimpleCookie(cookie_string)
        if 'session_id' in cook:
            saved_session_id = cook['session_id'].value
        
            #check if session id is valid
            c.execute('select * from users where session_id=?', (saved_session_id,))
            account = c.fetchall()
            if len(account) > 0:    #cookie valid, redirect
                print
                print '<html><head>'
                print '<meta http-equiv="refresh" content="1; url=profile.py" />'
                print '</head></html>'
                
                return
            else: #session id no longer valid, delete it
                cook['session_id']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT' #expiration in past, deletes cookie
                print cook  #then continue printing login as below
    
    print   #extra line for header
    
    print '<html>'
    print '<head><title>Pigskinners Login</title></head>'
    print '<body>'
    print '<p><a href=../index.html>Home</a> | <a href=register.py>Register</a></p>'
    
    form = cgi.FieldStorage()
    if 'error' in form:
        if form['error'].value == "bad_login":
            print '<h2>Invalid e-mail/password combination</h2>'
        elif form['error'].value == "incomplete_login":
            print '<h2>Please enter a username and password</h2>'
    
    print '<form method="post" action="error_check.py">'
    print 'E-mail: <input name="email" type=text size="30"/>'
    print '<br/>'
    print 'Password: <input name="password" type="password" size="20"/>'
    print '<br/>'
    print '<input name="last_page" type="hidden" value="login"/>'
    print '<input type="submit"> <input type="reset">'
    print '</form>'
    print '</body>'
    print '</html>'
    
main()