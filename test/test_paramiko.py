
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.104', 22, 'xinali', 'daitaocaiguai')
stdin, stdout, stderr = ssh.exec_command('whoami')
print stdout.readlines()
print stderr.readlines()
ssh.close()

