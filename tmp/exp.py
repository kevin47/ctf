#!/usr/bin/env python2

from pwn import *

#r = process('./1')
r = remote('csie.ctf.tw', 10123)
r.sendline('1')

r.interactive()
