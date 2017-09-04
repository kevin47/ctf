import sys
import urllib
d1 = open('x1r', 'rb').read()
d2 = open('x2r', 'rb').read()
f = { 'username' : d1, 'password' : d2}
print urllib.urlencode(f)
