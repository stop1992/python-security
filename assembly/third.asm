assume cs:code, ds:data, es:table

data segment

	; year data
	db '1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986'
	db '1987','1988','1989','1990','1991','1992','1993','1994','1995'
     
    	; income data
	;dd 16,22,32,1356,2390,8000,16000,24486,50065,93444,140417,187777
	;dd 232323,690000,189999,781111,900000,8989989
	;dd 232343,454545,234243,3453345
    	;dd 21 dup(64h)
    	dd 64,64,64,64,64
        dd 64,64,64,64,64
    	dd 64,64,64,64,64
    	dd 64,64,64,64,64,64  
    	; staff data
	;dw 2,2,4,13,28,38,130,220,476,778,1001,1441,2269,2793,40384
	;dw 5635,8225,11542,14430,15257,17800
    	dw 21 dup(2)
    
data ends

	
	
table segment
	db 21 dup ('year summ ne ?? ')
table ends

code segment
start:
		; initialization
		mov ax, data
		mov ds, ax
		mov ax, table
		mov es, ax
		mov bx,0
		mov si,0
		mov di,0
		mov cx,21

	s:
		mov ax, ds:[bx]
		mov es:[di], ax
		mov dx, ds:[bx+2]
		mov es:[di+2], dx

		;add di,5
		mov ax, ds:[bx+54h]
		mov es:[di+5h],ax
		mov dx, ds:[bx+56h]
		mov es:[di+7h], dx

		;add si,5
		mov ax, ds:[si+0a8h]
		mov es:[di+0ah], ax
		
		mov ax, ds:[bx+54h]
		mov dx, ds:[bx+56h]
		div word ptr ds:[si+0a8h]
		
		;add si,3
		mov es:[di+0dh], ax

		;add si,2
		;add bx, 1


		add bx, 4
		add si, 2
		add di, 10h 
		
		loop s

	mov ax, 4c00h
	int 21h
code ends
end start
