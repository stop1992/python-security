assume cs:code,ds:data,ss:stack


data segment
	db 0 dup(10)
data ends


stack segment
	dw 0 dup(8)
stack ends

code segment
start:
	mov ax,12666
	mov bx,data
	mov ds,bx
	mov si,0 
	mov bx,stack
	mov ss,bx
	mov sp,16
	;push 0
	call dtoc


	mov ax,0b800h
	mov es,ax
	mov dh,8
	mov dl,3
	;mov cl,2
	call show_str
	
	mov ax,4c00h
	int 21h

dtoc:
	mov di,0
	mov bx,10
	push 0 
	;mov dx,0
s0:
    
	mov dx,0
	div bx
	add dx,30h
	mov cx,ax    
	push dx
	inc di

	;jcxz s1
	jcxz reverse
	;push dx	
	;inc di
	jmp short s0


reverse: 

	pop cx
	mov ds:[si],cl  
	inc si
	jcxz s1
	jmp short reverse

s1: 
    ret
    ;jmp s0
	;mov byte ptr ds:[di],0
	;ret

	
	
show_str:
	dec dh
	mul dh
	mov bx,ax


	dec dl
	mul dl
	add bx,ax

	mov si,0
s2:

	mov ch,ds:[si]
	mov cl,0
	jcxz s3
	mov cl,71h
	mov es:[bx],ch
	mov es:[bx+1],cl
	inc si
	;inc bx
	add bx,2
	jmp short s2

s3:
	ret


code ends
end start

