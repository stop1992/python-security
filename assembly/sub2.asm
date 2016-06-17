assume cs:code


stack segment
	dw 2 dup(0)
stack ends


code segment

start:
	mov ax,4240h ;define L
	mov dx,000fh ;define H
	mov cx,0ah   ;define N
	call divwd

	mov ax,4c00h
	int 21h


divwd:
	;push dx
	push ax

	mov ax,dx
	mov dx,0
	div cx ;H/N

	mov bx,ax
	pop ax

	div cx

	mov cx,dx
	mov dx,bx


code ends
end start

