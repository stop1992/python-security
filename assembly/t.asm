assume  cs:code,ss:stack


stack segment
	db 0 dup(10)

code segment

start:
	mov ax,3
	push ax
	pop ax

	mov ax,4c00h
	int 21h

code ends
end
