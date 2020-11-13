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
Click the exit button
Close the server process
A copy of the sent file will now be located in the server side folder.

Different Scenarios:
In the No loss case, the client and server will behave as it did in the previous phase where it just sends the packets
one at a time. In this case the client and server will be sending each other ACKs and sequence numbers to confirm
the correct packets are being received and puting the packets in the correct order.
Ack bit error cases were not properly implemented (see design document for further information). However, 3 bit error codes were implemented to transmit the single bit sequence numbers. This allows for up to 1 bit to be corrupted while still functioning properly.
In the data bit error case, the checksums will fail to match on the server side and the server will send a nack (previous sequence number ack) and the client will retransmit the file. This repeats until a proper checksum check occurs and a proper ack is received.

Additonal information:
The program is single directional, only sending a file from client to server.
In order to alter the error rate of sent packets, edit line 4 of the makepacket function "error rate = x" where x is the percent of packets that are corrupted.
Any file type can be used, only .jpg and .bmp files were tested.
The program uses port 8090
