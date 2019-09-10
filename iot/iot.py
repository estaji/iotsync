#! /usr/bin/env python3

# Direct Cloud Sync
# Author: Omid Estaji (estaji.work@gmail.com)
# IoT Device Component 

import os
import time
import socket
import paramiko

mirrorIP = '192.168.1.3'
mirrorPORT = 2000
MAX_BYTES = 65535

def off_network():
    os.system('sudo ifconfig ens33 down')
    
def on_network():
    os.system('sudo ifconfig ens33 up')
    time.sleep(3)

def heartbeat(upnum):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((mirrorIP, mirrorPORT))
    print('IoT socket name is {}'.format(sock.getsockname()))
    delay = 0.1 # seconds
    text = upnum
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        upnum2 = ''
        try:
            data = sock.recv(MAX_BYTES)
            if data != '':
                upnum2 = data.decode('ascii')
                print('The server says its update number is {!r}'.format(upnum2))
        except:
            #Exponential backoff, wait even longer for the next request
            delay *= 2
            if delay > 2.0:
                print('I think the server(mirror) is down')
                return upnum,  None
        else:
            break
    return upnum,  upnum2
    

def checkupdate(upnum,  upnum2):
    if upnum2 == None:
        print("We can't update {No connection}")
        return None
    elif int(upnum) == int(upnum2):
        print('No update needed')
        return None
    elif int(upnum) > int(upnum2):
        print('Who should Sync with other one?')
        return 'mirror'
    elif int(upnum) < int(upnum2):
        print('Who should Sync with other one?')
        return 'iot'


def ssh(upnum):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('192.168.1.3', username='omid', password='password_phrase')
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
        print ("SSH Connection Error")
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
        off_network()
        timer=0
        while timer<60:   #60
            time.sleep(1)
            timer+=1
            print(timer)
        on_network()
        time.sleep(10)
        upnum = upnum_read()
        upnum,  upnum2 = heartbeat(upnum)
        who = checkupdate(upnum,  upnum2)
        print(who)
    if who == 'mirror':
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
    print('**************************** Synchronization Finished ****************************')

if __name__ == '__main__':
    while True:
        main()

