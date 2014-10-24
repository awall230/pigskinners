#!/usr/bin/env python

import Cookie
import cgi
import os

cookie_string = os.environ.get('HTTP_COOKIE')
cook = None

if cookie_string:   #user is logged in
    cook = Cookie.SimpleCookie()
    cook['session_id'] = ''
    cook['session_id']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT' #expiration in past, deletes cookie

    
print 'Content-type: text/html'
if cookie_string:
    print cook
print
print '<html>'
print '<head><title>Logged Out</title>'
print '<meta http-equiv="refresh" content="1; url=../index.html" />'
print '</head>'
print '</html>'