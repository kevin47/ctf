#!/usr/bin/env python2

from pwn import *
import string

a = string.letters + string.digits

context.arch='amd64'
for i in a:
	print i, disasm(i+'ACBDEF').split('\n')[0]
