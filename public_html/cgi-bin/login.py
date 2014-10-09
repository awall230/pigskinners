#!/usr/bin/env python

import cgi

print 'Content-type: text/html'
print

print '<html>'
print '<head><title>Pigskinners Login</title></head>'
print '<body>'

form = cgi.FieldStorage()
if 'error' in form:
    if form['error'].value == "bad_login":
        print '<h2>Invalid e-mail/password combination</h2>'

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