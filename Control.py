import Ipano # type: ignore
import time

import paramiko # type: ignore
import time
import subprocess
import sys

master = "172.20.4.160"
slave1 = "172.20.4.161"
slave2 = "172.20.4.162"



def captures(cam, it) : 

    username = "sand"
    password = "lumin007"

    # Prise des photos

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(master, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo capture{cam}.py -t 10000 -g 16")
    #time.sleep(10)
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave1, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo capture{cam}.py -t 10000 -g 16")
    #time.sleep(10)
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave2, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo capture{cam}.py -t 10000 -g 16")
    time.sleep(10)
    client1.close()



    # On renomme les photos
    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(master, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_{cam}.jpg Capture_{master}{cam}{it}.jpg")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave1, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_{cam}.jpg Capture_{slave1}{cam}{it}.jpg")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave2, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_{cam}.jpg Capture_{slave2}{cam}{it}.jpg")
    client1.close()

    # On copie les photos sur l'ordinateur
    subprocess.call(f"scp sand@{master}:~/Capture_{master}{cam}{it}.jpg C:\\Users\\mathi\\Rose\\Mesure-angle\\Data\\{master}\\{cam}" , shell=True)
    subprocess.call(f"scp sand@{slave1}:~/Capture_{slave1}{cam}{it}.jpg C:\\Users\\mathi\\Rose\\Mesure-angle\\Data\\{slave1}\\{cam}" , shell=True)
    subprocess.call(f"scp sand@{slave2}:~/Capture_{slave2}{cam}{it}.jpg C:\\Users\\mathi\\Rose\\Mesure-angle\\Data\\{slave2}\\{cam}" , shell=True)

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(master, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo rm capture_*")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave1, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo rm capture_*")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave2, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo rm capture_*")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(master, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo rm Capture*")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave1, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo rm Capture*")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(slave2, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo rm Capture*")
    client1.close()


ipano = Ipano.IPANO('COM5')
ipano.set_zero_position()


def measures(altIterations, altPrecision,  azIterations, pauseTime) :
    ipano.goto((0-altIterations)*2, 0*(360/azIterations))
    time.sleep(7)
    for i in range(altIterations) :
        for j in range(azIterations) :
            ipano.goto((i-altIterations/2)*altPrecision, j*(360/azIterations))
            time.sleep(pauseTime)
            captures("A", i*azIterations+j)
            time.sleep(10)
            captures("B", i*azIterations+j)
            time.sleep(10)
            captures("C", i*azIterations+j)
            time.sleep(10)
            captures("D", i*azIterations+j)
            time.sleep(10)


measures(1, 2, 3, 5)