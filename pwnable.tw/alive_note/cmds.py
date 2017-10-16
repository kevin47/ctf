#!/usr/bin/env python2

from pwn import *
import string

s = string.ascii_letters+string.digits

for i in s:
	print i, disasm(i+'ACBDEF').split('\n')[0]

