Network Design Project - Phase 3
Prof. Vokkarane
Julie Dawley, Ricardo Candanedo, Mohammad Musawer

OS: Windows 10
Language: Python 3.8
IDE: Pycharm w/github

Instructions:
Run the server File, located in the serverside folder
Run the client file
If the server and client are running on the same machine, do not change the send address.
Otherwise, get the server name from the console of the server and write it in the send address.
If using the default image file (intothespiderverse.jpg) do not change the file name.
Otherwise, write the name of the file to transmit to the server.
Click the transmit button
Wait for the file to transmit
A copy of the sent file will now be located in the server side folder.

Different Scenarios:
In the No loss case, the client and server will behave as it did in the previous phase where it just sends the packets
one at a time. In this case the client and server will be sending each other ACKs and sequence numbers to confirm
the correct packets are being received and puting the packets in the correct order.
Ack and data packet bit errors are handled by comparing checksums and retransmitting the previous ack/packet.
In the packet loss case, the client side receiver will timeout after 50ms and retransmit the most recent packet.

Additonal information:
The program is single directional, only sending a file from client to server.
To alter ack bit and loss rates, change the values on lines 28 and 29 respectively in the server.py file.
To alter data packet bit and loss rates, change the values on lines 31 and 32 respectively in the client.py file.
Any file type can be used, only .jpg and .bmp files were tested.
The program uses port 8090
