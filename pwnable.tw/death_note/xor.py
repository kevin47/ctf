#!/usr/bin/env python2

a = [(0, 0)]*256
for i in range(127, 31, -1):
	for j in range(127, 31, -1):
		a[i^j] = (i, j)

for i in range(256):
	print i, a[i]
