import socket                    # module to establish connection
import tkinter as tk             # module to create GUI
import time                      # module for time funcs such as .sleep()
import random

def calculateChecksum(packetData):
    checksumTotal = 0
    dataLength = len(packetData)

    for x in range(0, dataLength):
        currByte = packetData[-x]
        checksumTotal += currByte

    checksumInverse = checksumTotal % 65536
    checksum = 65535 - checksumInverse

    return int(checksum)

def corruptPacket(packetData):
    #corrupts data by generating a random number and xoring it with the data

    corruption = random.randint(0, pow(2, 1024))
    tempData = int.from_bytes(packetData, "big")
    tempCorrupted = tempData ^ corruption
    corruptedData = tempCorrupted.to_bytes(1024, "big")

    return corruptedData

def sendPacket(packetData, seqNumber, socketVar, x):
    #takes the data and seq number and converts it into a packet, including checksum, and encodes it
    errorRate = 10  #percentage of packets that get corrupted
    packetLossRate = 0 #percentage of packets lost in transit (simulated as not being sent)
    dataChecksum = calculateChecksum(packetData)

    #Potentially corrupt the packet
    errorCalc = random.randint(0, 99)
    if errorCalc < errorRate:
        packetData = corruptPacket(packetData)
    madePacket = seqNumber.to_bytes(1,"big") + dataChecksum.to_bytes(2,"big") + packetData
    packetLossCalc = random.randint(0, 99)
    if packetLossCalc >= packetLossRate:
        socketVar.send(madePacket)
    else:
        print("Packet " + str(x) + " failed to transmit.")

def receiveAck(socketVar, data, seqNumber, x):
    #receives an ack from the server. Includes sequence number checking and timeouts.
    ackReceivedBool = False

    while ackReceivedBool == False:
        try:
            socketVar.settimeout(0.05)
            receivedAck = socketVar.recv(3)
            ackReceivedBool = True
        except socket.timeout:
            print("Timeout detected. Retransmitting packet " + str(x))
            sendPacket(data,seqNumber, socketVar, x)

    #process the ack to determine the seq number received
    if (receivedAck == 110) or (receivedAck == 101) or (receivedAck == 11) or (receivedAck == 111):
        decodedAck = 1
    else:
        decodedAck = 0

    print("Expected and received sequence numbers. " + str(seqNumber) + " " + str(decodedAck))

    if decodedAck != seqNumber:
        retransmitError_string = f"Sequence number mismatch. Retransmitting packet {x} to the server..."
        print(retransmitError_string)
        sendPacket(data, seqNumber, socketVar, x)
        receiveAck(socketVar, data, seqNumber, x)


def transmitFile(hostAddress, fileName):
    # function to transmit the file. Contains the code copy/pasted from phase1
    # takes as input the host address to send the file to and the name for the file upon arrival

    start = time.time() #Start time of sending the file. Used to calculate time to transmit

    # initialization of the object and connects it to the port and host address
    socketVar = socket.socket()
    port = 8090
    socketVar.connect((hostAddress, port))

    # open file in read-binary
    fileToSend = open(fileName, 'rb')

    # finds the length of the file, calculates the number of packets and prints all info
    fileToSend.seek(0, 2)
    fileLength = fileToSend.tell()
    numOfPackets = int(fileLength / 1024) + 1
    fileToSend.seek(0, 0)
    print(fileLength)
    print(fileName)
    print(numOfPackets)

    # encodes the fileName and numOfPackets and sends it to the server
    encodedFileName = fileName.encode()
    socketVar.send(encodedFileName)
    time.sleep(1)  # delays by 1 second
    stringNumOfPackets = str(numOfPackets)
    encodedStringNumOfPackets = stringNumOfPackets.encode()
    socketVar.send(encodedStringNumOfPackets)

    seqNumber = 0  #initialize the sequence number


    # loop to keep sending packets and prints the packet number that is being sent
    for x in range(1, numOfPackets + 1):
        numOfPacketsSend_String = f"Sending packet #{x} to the server with sequence {seqNumber}"
        print(numOfPacketsSend_String)

        data = fileToSend.read(1024)  #read data from the file
        sendPacket(data, seqNumber, socketVar, x)

        #receive an ack from the server
        ackFromServer = socketVar.recv(3)
        receivedAck = int(ackFromServer.decode())

        #decode the ack
        if (receivedAck == 110) or (receivedAck == 101) or (receivedAck == 11) or (receivedAck == 111):
            decodedAck = 1
        else:
            decodedAck = 0

        #if the received ack does not match the sent sequence number, retransmit and repeat until they do.
        while decodedAck != seqNumber:
            retransmitError_string = f"Retransmitting packet #{x} to the server..."
            print(retransmitError_string)
            sendPacket(data, seqNumber, socketVar,x)

            ackFromServer = socketVar.recv(3)
            receivedAck = int(ackFromServer.decode())
            if (receivedAck == 110) or (receivedAck == 101) or (receivedAck == 11) or (receivedAck == 111):
                decodedAck = 1
            else:
                decodedAck = 0

        #flip the sequence number
        seqNumber = seqNumber ^ 1


    fileToSend.close()

    # displays that the data has been sent successfully
    print("\nData has been sent successfully!")

    # Times the amount of time it takes to send all packets to the server after the file closes
    end = time.time()
    print("Amount of time to receive all packets: ", end - start)

    return

def sendFile(event):
    # event to send the file once the user has clicked the "Send file" button
    hostAddress = ent_destination.get()
    fileName = ent_fileName.get()
    window.quit()
    transmitFile(hostAddress, fileName)
    return

# get the name of this machine to use as a default address
defaultServerName = socket.gethostname()
window = tk.Tk()
# introductory message
lbl_introduction = tk.Label(text = "Networking Design Project Phase 2. \n"
                             "EECE.4830 201. Professor Vokkarane. \n"
                             "By: Julie Dawley, Ricardo Candanedo, and Mohammad Musawer \n \n"
                             "Destination Computer: Defaults to this machine. \n"
                             "Change to the address in serverClient if running client and server on seperate machines")
lbl_introduction.pack()
# get the destination name from the user, default to defaultServerName
ent_destination = tk.Entry()
ent_destination.pack()
ent_destination.insert(0, defaultServerName)
# hostAddress = ent_destination.get()

# get the file name from the user. Default to receivedFile.jpg
lbl_getFileName = tk.Label(text="\n Enter the name the file should have at the destination")
ent_fileName = tk.Entry()
lbl_getFileName.pack()
ent_fileName.pack()

ent_fileName.insert(0, "intothespiderverse.jpg")

btn_confirmEntry = tk.Button(text="Transmit File", height=2, width=10)
btn_confirmEntry.pack()
btn_confirmEntry.bind('<Button-1>', sendFile)

window.mainloop()  # keeps window open until event is called or the user exits the GUI
