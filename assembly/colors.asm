assume cs:code, ds:data, ss:stack

data segment
	db 'welcome to masm!' 
	db 02h, 24h, 71h   ; define color

data ends

stack segment

	dw 8 dup (0)

stack ends


code segment
start:
		mov ax, data
		mov ds, ax
		mov ax, stack
		mov ss, ax
		mov sp, 10h


		xor bx,bx
		mov ax, 0b872h

		mov cx, 3

s3:
		push cx
		push ax
		push bx
		mov es, ax
		mov si, 0
		mov di, 0

		mov cx, 10h


s1:	
		mov al, ds:[si]
		mov es:[di], al
		inc si
		add di,2
		loop s1

		mov di, 1
		pop bx
		mov al, ds:10[bx]
		inc bx

		mov cx,10h

s2:
		mov es:[di], al
		add di,2
		loop s2

		pop ax
		add ax,0ah

		pop cx
		loop s3

		mov ax, 4c00h
		int 21h

code ends
end start
