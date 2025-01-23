import Ipano # type: ignore
import time

import paramiko # type: ignore
import time
import subprocess
import sys

master = "172.20.4.160"
slave1 = "172.20.4.161"
slave2 = "172.20.4.162"



def captures(pi, it) : 

    username = "sand"
    password = "lumin007"

    # Prise des photos

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command("sudo captureA.py -t 10000 -g 16")
    time.sleep(10)
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command("sudo captureB.py -t 10000 -g 16")
    time.sleep(10)
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command("sudo captureC.py -t 10000 -g 16")
    time.sleep(10)
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command("sudo captureD.py -t 10000 -g 16")
    time.sleep(10)
    client1.close()

    # On renomme les photos
    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_A.jpg Capture_{pi}A{it}.jpg")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_B.jpg Capture_{pi}B{it}.jpg")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_C.jpg Capture_{pi}C{it}.jpg")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo mv capture_D.jpg Capture_{pi}D{it}.jpg")
    client1.close()

    # On copie les photos sur l'ordinateur
    subprocess.call(f"scp sand@{pi}:~/Capture_*A* C:\\Users\\mathi\\Rose\\Mesure-angle\\Data\\{pi}\\A" , shell=True)
    subprocess.call(f"scp sand@{pi}:~/Capture_*B* C:\\Users\\mathi\\Rose\\Mesure-angle\\Data\\{pi}\\B" , shell=True)
    subprocess.call(f"scp sand@{pi}:~/Capture_*C* C:\\Users\\mathi\\Rose\\Mesure-angle\\Data\\{pi}\\C" , shell=True)
    subprocess.call(f"scp sand@{pi}:~/Capture_*D* C:\\Users\\mathi\\Rose\\Mesure-angle\\Data\\{pi}\\D" , shell=True)

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
    stdin, stdout, stderr = client1.exec_command(f"sudo rm capture_*")
    client1.close()

    client1 = paramiko.client.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(pi, username=username, password=password)
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
            captures(master, i*azIterations+j)
            captures(slave1, i*azIterations+j)
            captures(slave2, i*azIterations+j)


measures(1, 2, 3, 5)