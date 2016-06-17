assume cs:codesg

codesg segment
	mov ax, 4c00h
	int 21h

start:  mov ax, 0
	s:	nop
		nop

	s0: jmp short s

	s1: mov ax, 0
		int 21h
		mov ax, 0

	s2: jmp short s1
		nop

codesg ends
end start
