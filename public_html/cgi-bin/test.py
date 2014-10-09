#!/usr/bin/env python

def login(email_address):
    import Cookie
    import uuid
    session_id = str(uuid.uuid4())
#    c.execute('update users set session_id=? where email=?', (session_id, email_address))
#    conn.commit()
    cook = Cookie.SimpleCookie()
    cook['session_id'] = session_id
    
    print 'Content-type: text/html'
    print cook
    print

    print '<html>'
    print '<head>'
    print '<title>Pigskinners</title>'
#    print '<meta http-equiv="refresh" content="1; url=profile.py" />'
    print '</head>'
    print '<body>'
    print '<p><a href=profile.py>Profile</a></p>'
    print '</body>'
    print '</html>'
    
login('test@test.com')