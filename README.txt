# About
This is a solution for securing IoT devices using cloud-based synchronization.
Original idea comes from an article named "IoT Protection Through Device to Cloud Synchronization" by Christian Gehrmann and Mohammed Ahmed Abdelraheem. This article recommends a novel method where the IoT device execution state is modeled with a suitable high level application model and where the execution state of the application of the IoT device is "mirrored" in a cloud executed machine. This machine has very high availability and high attack resistance. The IoT device will only communicate with the mirror machine in the cloud using a dedicated synchronization protocol. All essential IoT state information and state manipulations are communicated through this synchronization protocol while all end application communication directed towards the IoT units is done towards the mirror machine in the cloud. This gives a very robust and secure system with high availability at the price of slower responses. However, for many non-real time IoT application with high security demands this performance penalty can be justified.
For more information read: https://ieeexplore.ieee.org/document/7830733

## Requirements
1.Two linux-based devices:
	A virtual-Machine(VM) in a public cloud called 'mirror'
	An ioT-Device(IoT) connected to Internet
2.Install Python3 and pip3 on both devices.
3.Install Paramiko module on both devices: "$ pip3 install paramiko"

## Deployment
1.Move iotsync/iot/ files to IoT device and user home directory.
2.Move iotsync/mirror/ files to mirror virtual machine and user home directory.
3.Move iotsync/utilities/ files to both devices.
4.Update IPs, ports, usernames, passwords, paths in codes.
5.Run ~/tcp_wrapper.py on IoT device.
6.Run ~/iot.py on IoT device.
7.Run ~/mirror.py on mirror.
