#!/usr/bin/env python

import cgi
import datetime

import cgitb
cgitb.enable()

form = cgi.FieldStorage()

print 'Content-type: text/html'
print

print '<html>'
print '<head><title>Pigskinners time test></title></head>'
print '<body>'
print '<h1>The time is ' + str(datetime.datetime.now()) + '</h1>'
print '<h2>You typed: ' + form['my_string'].value + '</h2>'
print '</body>'
print '</html>'