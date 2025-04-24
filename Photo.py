import Ipano # type: ignore
import time
import math

import paramiko # type: ignore
import time
import subprocess
import sys

ipano = Ipano.IPANO('port')
ipano.set_zero_position()
print("zero")
ipano.goto(0,0)
time.sleep(10)

master = "172.20.4.160"
slave1 = "172.20.4.161"
slave2 = "172.20.4.162"

username = "username"
password = "password"

    # Prise des photos

client1 = paramiko.client.SSHClient()
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client1.connect(slave2, username=username, password=password)
stdin, stdout, stderr = client1.exec_command(f"sudo captureA.py -t 10000 -g 16")
time.sleep(10)
client1.close()

# On renomme les photos
client1 = paramiko.client.SSHClient()
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client1.connect(slave2, username=username, password=password)
stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_A.jpg Capture_{master}A.jpg")
client1.close()

time.sleep(5)

subprocess.call(f"scp sand@{slave2}:~/Capture_{master}A.jpg path" , shell=True)

client1 = paramiko.client.SSHClient()
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client1.connect(slave2, username=username, password=password)
stdin, stdout, stderr = client1.exec_command(f"sudo rm capture_*")
client1.close()