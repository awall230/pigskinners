#!/usr/bin/env python

import cgi

import cgitb
cgitb.enable()

form = cgi.FieldStorage()

print 'Content-type: text/html'
print

print '<html>'
print '<head><title>Pigskinners time test></title></head>'
print '<body>'
print "<h2>So you're a " + form['fav_team'].value + " fan?</h2>"
print '</body>'
print '</html>'