from pwn import *
p = process('./a.out')
p.sendline('1234\0')
p.sendline('1234\0')
p.sendline('1234\0')
p.interactive()
