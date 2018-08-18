#! /usr/bin/env python3

# Direct Cloud Sync
# Author: Omid Estaji (estaji.work@gmail.com)
# TCP Wrapper Editor On IoT Device Component 

import os
mirrorIP = '192.168.1.3'

def main():
    os.system('echo ALL: ALL >> /etc/hosts.deny')
    os.system('echo sshd: {} >> /etc/hosts.allow'.format(mirrorIP))
    
if __name__ == '__main__':
    main() 
