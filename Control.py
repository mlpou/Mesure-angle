import Ipano # type: ignore
import time
import math

import paramiko # type: ignore
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
    subprocess.call(f"scp sand@{master}:~/Capture_{master}{cam}{it}.jpg sand@rasberrypi:~/Mesure-Angle/data/{master}{cam}" , shell=True)
    subprocess.call(f"scp sand@{slave1}:~/Capture_{slave1}{cam}{it}.jpg sand@rasberrypi:~/Mesure-Angle/data/{slave1}\\{cam}" , shell=True)
    subprocess.call(f"scp sand@{slave2}:~/Capture_{slave2}{cam}{it}.jpg sand@rasberrypi:~/Mesure-Angle/data/{slave2}\\{cam}" , shell=True)

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
print("zero")


def measures(altIterations, altPrecision,  azIterations, azAugmentation, pauseTime) :
    ipano.goto((0-altIterations)*2, 0*(360/azIterations))
    time.sleep(7)
    for i in range(altIterations) :
        iterations = azIterations #+ int(math.sin(math.radians(i-altIterations/2*altPrecision))*azAugmentation)
        for j in range(iterations) :
            ipano.goto((i-altIterations/2)*altPrecision, j*(360/iterations))
            time.sleep(pauseTime)
            captures("A", i*azIterations+j)
            time.sleep(10)
            captures("B", i*azIterations+j)
            time.sleep(10)
            captures("C", i*azIterations+j)
            time.sleep(10)
            captures("D", i*azIterations+j)
            time.sleep(10)

#time.sleep(300)
measures(3, 3, 3, 0, 5)