assume cs:codesg

codesg segment
		dw 0134h,3434h,3423h,8987h,9889h,1111h,3411h,3443h
		dw 0,0,0,0,0,0,0,0

start:  mov ax, cs
		mov ss, ax
		mov sp, 32
		mov cx, 8
		mov bx, 0

s:		push cs:[bx]
		add bx, 2
		loop s

		mov bx, 0
		mov cx, 8

pop_flag: pop cs:[bx]
		add bx,2
		loop pop_flag
	
		mov ax, 4c00h
		int 21h

codesg ends

end start
		


