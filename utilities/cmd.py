#! /usr/bin/env python3

# Direct Cloud Sync
# Author: Omid Estaji (estaji.work@gmail.com)
# Run Command Component

from sys import argv
import subprocess

def main():
    str_args = [ str(x) for x in argv[1:] ] #create sequence
    cmd = ''
    for i in argv[1:]: #create str
        cmd += i + ' '
    path = 'cmd.txt'
    file=open(path, "a")
    file.write(cmd + '\n')
    file.close()
    #update the upnum
    path_upnum = '/home/omid/upnum.txt'
    file=open(path_upnum, "r")
    upnum = int(file.read())
    upnum = str(upnum + 1)
    file.close()
    file=open(path_upnum, 'w')
    file.write(upnum + '\n')
    file.close()
    #execute the command
    subprocess.call(str_args)
    
if __name__ == '__main__':
    main() 
