assume cs:code, ds:data, ss:stack

data segment
	db 'welcome to masm!'
	dw 42h, 71h, 0cah
data ends

stack segment

	dw 8 dup(0)

stack ends

code segment
start:
	mov ax,data
	mov ds,ax
	mov ax,stack
	mov ss,ax
	mov sp,10h

	mov di,10h
	mov ax,0b800h
	mov es,ax

	mov bx,0b800h

	mov cx,3
s0:
	push cx
	push bx

	mov si,0

	mov cx,10h
	mov bx,0
s1:
	mov ah,ds:[si]
	mov al,ds:[di]
	mov es:[bx],ax

	add bx,2
	inc si
	loop s1


	pop bx
	add bx,9fh
	inc di
	pop cx
	loop s0


	mov ax,4c00h
	int 21h
code ends
end start
