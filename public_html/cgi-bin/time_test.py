#!/usr/bin/env python

import cgi
import datetime

import cgitb
cgitb.enable()

form = cgi.FieldStorage()

print("""Content-type: text/html

<html>
<head><title>Pigskinners time test></title></head>
<body>
<h1>The time is {1}</h1>
</body>
</html>
""", str(datetime.datetime.now()))