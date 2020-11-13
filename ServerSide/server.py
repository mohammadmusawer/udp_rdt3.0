import socket  # module to establish connection
import random

# initializes the socket obj, hostname and port and binds it to the server
socketVar = socket.socket()
hostName = socket.gethostname()
port = 8090
socketVar.bind((hostName, port))
socketVar.listen(1)  # wait for 1 incoming connection
sequenceNumber = 0

print(hostName)
def calculateChecksum(packetData):
    checksumTotal = 0
    dataLength = len(packetData)

    for x in range(0, dataLength):
        currByte = packetData[-x]
        checksumTotal += currByte

    checksumInverse = checksumTotal % 65536
    checksum = 65535 - checksumInverse

    return int(checksum)

def sendAck(seqNumber, connection):
    #Creates, encodes, and sends an ack. Also implements corruption and packet loss
    packetLossRate = 10
    bitLossRate = 10

    ack = str(seqNumber) + str(seqNumber) + str(seqNumber)
    ack = ack + ack + ack + ack + ack + ack + ack + ack
    bitLossCalc = random.randint(0,99)
    if bitLossCalc < bitLossRate:
        corruption = random.randint(0, pow(8,8))
        ack = str(int(ack) ^ corruption)
    encodedAck = ack.encode()

    packetLossCalc = random.randint(0, 99)
    if packetLossCalc >= packetLossRate:
        connection.send(encodedAck)
    else:
        print("Ack failed to transmit")

# loops to accept the incoming connection and file being sent from the client
while True:
    print("Waiting for connection...")
    connection, address = socketVar.accept()

    print(address, "Has connected to the server")

    # receives the fileName and packets from the client and decodes it
    fileName = connection.recv(1024)
    print(fileName)
    fileName = fileName.decode()
    numOfPackets = connection.recv(1024)
    decodedNumOfPackets = numOfPackets.decode()
    numOfPackets = int(decodedNumOfPackets)

    # open the file in write-binary
    file = open(fileName, 'wb')
    expectedSeqNumber = 0

    # loops to keep receiving packets and prints the packets being received from the client
    for x in range(1, numOfPackets + 1):
        numOfPacketsRecv_String = f"Receiving packet #{x} from client..."
        print(numOfPacketsRecv_String)

       #receive the packet and extract information from it
        rcvdPacket = connection.recv(1033)
        rcvdSeqNumber = rcvdPacket[0]
        rcvdChecksum = int.from_bytes(rcvdPacket[1:3], "big")
        rcvdData = rcvdPacket[3:]

        #determine if the packet was received properly via checksum. If yes, send ack, else send nack.
        calcChecksum = calculateChecksum(rcvdData)

        while True:
            if(calcChecksum == rcvdChecksum) and (expectedSeqNumber == rcvdSeqNumber):
               #if the checksums matched, send an ack and write the data
                file.write(rcvdData)
                sendAck(rcvdSeqNumber, connection)
                break
            else:
                #if they dont, send a nack and receive a new packet. Repeat until everything is fine
                sendAck(expectedSeqNumber ^ 1, connection)


                #receive a new packet
                errorDeteced_string = f"Receiving retransmitted packet #{x} from client..."
                print(errorDeteced_string)

                rcvdPacket = connection.recv(1033)
                rcvdSeqNumber = rcvdPacket[0]
                rcvdChecksum = int.from_bytes(rcvdPacket[1:3], "big")
                rcvdData = rcvdPacket[3:]
                calcChecksum = calculateChecksum(rcvdData)
        expectedSeqNumber ^= 1
    connection.close()
    file.close()

    print("\nData has been transmitted successfully!")  # display that data has been transferred
    break
