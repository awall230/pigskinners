#!/usr/bin/env python

import Cookie
import cgi
import os

cookie_string = os.environ.get('HTTP_COOKIE')

if cookie_string:   #user is logged in
    cook = Cookie.SimpleCookie()
    cook['session_id'] = ''
    cook['session_id']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT' #expiration in past, deletes cookie

    
print 'Content-type: text/html'
print cook
print
print '<html>'
print '<head><title>Logged Out</title></head>'
print '<body>'
print '<p><a href=../index.html>Home</a></p>'
print '<h3>YOU ARE NOW LOGGED OUT</h3>'
print '</body>'
print '</html>'