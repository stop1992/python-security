assume cs:code,ds:data

data segment 
	db 'Welcome to assumenimjljlj', 0
data ends

code segment

start:
	mov ax,data
	mov ds,ax
	mov ax,0b800h
	mov es,ax
	mov dh,8
	mov dl,3
	call show_str

	
	mov ax,4c00h
	int 21h

show_str:
	dec dh
	mul dh
	mov bx,ax


	dec dl
	mul dl
	add bx,ax

	mov si,0
s1:

	mov ch,ds:[si]
	mov cl,0
	jcxz s2
	mov cl,71h
	mov es:[bx],ch
	mov es:[bx+1],cl
	inc si
	;inc bx
	add bx,2
	jmp short s1

s2:
	ret


code ends
end start
