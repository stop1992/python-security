assume cs:code,ds:data,ss:stack

data segment
	db 'thisis'
	db 02h, 24h, 71h

data ends

stack segment
	dw 8 dup(0)
stack ends

code segment

start:
	mov ax,data
	mov ds,ax
	mov ax, stack
	mov ss,ax
	mov sp, 10h
	mov ax,0b872h

	mov di,5
	mov cx,3

s3:
	mov es,ax
	push cx
	push ax

	mov si,0
	inc di
	mov bx,0

	mov cx,6


s0:

	mov al,ds:[si]
	mov ah,ds:[di]
	mov es:[bx], ax

	inc si
	add bx,2
	loop s0

	
	pop ax
	add ax, 0ah

	pop cx
	loop s3

	
	mov ax,4c00h
	int 21h

code ends
end start
