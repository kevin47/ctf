#!/usr/bin/env python2
from Crypto.PublicKey import RSA
key = RSA.importKey(open('public.pem').read())
print key.n, key.e
