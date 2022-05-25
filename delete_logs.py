# import pip
# pip.main(["install","--user","--user", "--trusted-host","pypi.org","--trusted-host","pypi.python.org"
#                          ,"--trusted-host","files.pythonhosted.org","getpass"])
# pip.main(["install","--user","--user", "--trusted-host","pypi.org","--trusted-host","pypi.python.org"
#                          ,"--trusted-host","files.pythonhosted.org","netmiko"])

from paramiko import SSHClient, AutoAddPolicy
client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())
host = "xxxx"
client.connect(host,  username="xxxx", password="xxxx", timeout=5) # we are connected we just cant send instructions
shell = client.invoke_shell()

client.exec_command("im")

#chan.sendall('im')
res = shell.recv(4096)
print("s:", res)



stdin, stdout, stderr = client.exec_command('im')

#chan.sendall('im')
res = she.recv(4096)
print("s:", res)

print("\n".join(stdout.readlines()))
print("commands executed...")
print(stdout.readlines())
print("readlines...")
print("done")
