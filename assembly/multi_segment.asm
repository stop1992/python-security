assume cs:code, ds:data, ss:stack

data segment
	dw 9009h,1234h,2323h,3434h,1231h,9999h,3431h,2222h
data ends

stack segment
	dw 0,0,0,0,0,0,0,0
stack ends

code segment
start:  mov ax, stack
		mov	ss, ax
		mov sp, 16
		mov ax, data
		mov ds, ax
		mov bx, 0
		mov cx, 8

s:		push [bx]
		add bx,2
		loop s

		mov bx,0
		mov cx,8
s1:		pop [bx]
		loop s1

		mov ax,4c00h
		int 21h

start end
