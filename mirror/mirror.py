#! /usr/bin/env python3

# Direct Cloud Sync
# Omid Estaji (estaji.work@gmail.com)
# Mirror (Cloud VM) Component 

import socket
import random
import paramiko
import time

interface = '192.168.1.3'
port = 2000
MAX_BYTES = 65535

def heartbeat(upnum):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        #Simulate a packet drop in virtual environment
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        upnum2 = data.decode('ascii')
        print('The IoT at {} says its update number is {!r}'.format(address, upnum2))
        message = upnum
        sock.sendto(message.encode('ascii'), address)
        return upnum,  upnum2

def checkupdate(upnum,  upnum2):
    if int(upnum) == int(upnum2):
        print('No update needed, because update numbers are equal')
        return None
    elif int(upnum) > int(upnum2):
        print('Who should Sync with other one?')
        return 'iot'
    elif int(upnum) < int(upnum2):
        print('Who should Sync with other one?')
        return 'mirror'


def ssh(upnum):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('192.168.1.6', username='omid', password='password_phrase')
        commands = ''
        path = 'cmd.txt'
        file = open(path, 'r')
        commands_list = file.readlines()
        for i in commands_list:
            commands = commands + i[:-1] + ' ; '
        file.close()
        commands += 'echo {} > ~/upnum.txt ; '.format(upnum[:-1])
        commands += 'echo 1 > ~/wait.txt ; '
        print (commands)
        stdin,stdout,stderr = ssh.exec_command(commands)
        for line in stdout.readlines():
            print (line.strip())
        file = open(path, 'w')
        file.write('')
        file.close()
    except paramiko.SSHException:
        print ("Connection Failed")
    except:
        print ("SSH Connection General Error")
    ssh.close()
    
def upnum_read():
    path = 'upnum.txt'
    upnum_file = open(path,'r')
    upnum = upnum_file.read()
    upnum_file.close()
    return upnum


def wait_read():
    path = 'wait.txt'
    wait_file = open(path,'r')
    wait = wait_file.read()
    wait_file.close()
    #Return 0 for wait longer and 1 for finish
    return wait
    
    

def main():
    who = None
    while who == None:
        upnum = upnum_read()
        upnum,  upnum2 = heartbeat(upnum)
        who = checkupdate(upnum,  upnum2)
        print(who)
    if who == 'iot':
        ssh(upnum)
    else:
        #Wait until SSH complete
        wait = wait_read()
        while int(wait) == 0:
            time.sleep(5)
            wait = wait_read()
        wait_file = open("wait.txt", "w")
        wait_file.write("0")
        wait_file.close()
    print('***************************** Synchronization Finished **********************************')
    
if __name__ == '__main__':
    while True:
        main()
