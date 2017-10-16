#!/usr/bin/env python2
from pwn import *
import string

p = remote('csie.ctf.tw', 10131)
s, b = [], []
NUM, LEN = 40, 128
space = [[0]*(LEN/2) for i in range(NUM)]

p.recvuntil('Press any key to read the book\n', drop=True)
for i in range(NUM):
	p.sendline('')
	s.append(p.recvuntil('Press any key to read the book\n', drop=True).split()[0])
	byte_arr = []
	for j in range(LEN/2):
		byte_arr.append(int(s[i][j*2 : j*2+2], 16))
	b.append(byte_arr)


for i in range(NUM):
	for j in range(LEN/2):
		for k in range(NUM):
			if i == k: continue
			if chr(b[i][j] ^ b[k][j]) in string.letters:
				space[i][j] += 1

threshold = 20
ans = ''
print 'LEN/2', LEN/2
for j in range(LEN/2):
	end = 0
	for i in range(1, NUM):
		if end: break
		if space[i][j] >= threshold:
			ans += chr(b[i][j] ^ b[0][j] ^ ord(' '))
			end = 1
        if end == 0: print 'jizz'
print ans, len(ans)

key = [b[0][i] ^ ord(ans[i]) for i in range(LEN/2)]

#for i in range(1, NUM):
#	print ''.join(chr(b[i][x] ^ key[x]) for x in range(LEN/2))

#while(1):
for i in range(1000):
	p.sendline('')

s = p.recvuntil('You read the entire book!\n', drop=True).split('Press any key to read the book\n')
#print s

next_break = 0
for i in s:
	byte_arr = []
        LEN = len(i)-1
	for j in range(LEN/2):
		byte_arr.append(int(i[j*2 : j*2+2], 16))
	i = ''.join(chr(byte_arr[x] ^ key[x]) for x in range(LEN/2))
	if 'FLAG' in i or next_break:
		print i
		if next_break: break
		next_break = 1
	

