#!/usr/bin/env python2

from pwn import *

def yes(x):
	if 'push' in x: return 1
	if 'pop' in x: return 1
	if 'add' in x: return 1
	if 'sub' in x: return 1
	if 'inc' in x: return 1
	if 'dec' in x: return 1
	return 1

for i in range(32, 127):
	x = disasm('%c' % chr(i))
	if yes(x):
		print i, '---'
		print x
for i in range(32, 127):
	for j in range(32, 127):
		x = disasm('%c%c' % (chr(i), chr(j)))
		if yes(x):
			print i, j, '---'
			print x
'''
for i in range(32, 127):
	for j in range(32, 127):
		for k in range(32, 127):
			print disasm('%c%c%c' % (chr(i), chr(j), chr(k)))
'''
'''
for i in range(32, 127):
	for j in range(32, 127):
		for k in range(32, 127):
			for l in range(32, 127):
				print disasm('%c%c%c%c' % (chr(i), chr(j), chr(k), chr(l)))
'''
