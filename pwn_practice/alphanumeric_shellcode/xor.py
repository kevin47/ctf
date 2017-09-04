#!/usr/bin/env python2

from pwn import *
import string

a = string.letters + string.digits
dic = {}

for i in a:
	for j in a:
		dic[ord(i)^ord(j)] = (i, j)

for d in dic:
	print d, dic[d]
