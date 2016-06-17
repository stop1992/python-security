assume cs:codesg, ds:data


data segment

;db 'daitao', 'wangxi', 'xinali'
;db '1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986'   
dd 22h,33h,66h

data ends

codesg segment

start: 
	mov ax, data
	mov ds, ax

	mov ax, 4c00h
	int 21h

codesg ends
end start
