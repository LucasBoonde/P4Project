import matlab.engine
import numpy as np
import time
import serial
import cv2 as cv
import math


arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
tOld = np.zeros((1,2))

def write_read(x):

    while True:
        arduino.write(bytes(x, 'utf-8'))
        print(x)
        time.sleep(0.05)
        data = arduino.readline().decode().strip()
        parts = data.split("#")
        print(parts)
        if len(parts) > 1 and parts[len(parts) - 1] == "M": #Kig efter om det sidste element i den modtagene besked er en Stopbesked
            break

    return parts


def CalculateAcc(velOld, tOld, vel):
    #Make a 2x2 Matrix That holds the old position of the motor and the new
    #Calculate velocity by: (ThetaNu - Theta Sidste  Sample)/ (Tiden Nu - Tiden Sidste Sample)

    velNow = vel[1].split(",")

    tNew = time.time()
    pDif = np.zeros(shape= [2,1])
    pDif[0] = velNow[0]-velOld[0]
    pDif[1] = velNow[1]-velOld[1]

    tDif = (tNew - tOld)
    Acc = pDif/tDif

    #After Calculations has been made
    velOld = velNow
    tOld = tNew

    return Acc, velOld, tOld

tOld = time.time()
velOld = np.zeros((2,1))

def AskForPosition():
    while True:

        message = ("P#")
        positionNow = np.zeros((2,1))
        returnMessage = write_read(message)
        if returnMessage[0] == "P":
            position = returnMessage[1].split(",")
            positionNow[0][0] = (float(position[0])*math.pi)/180
            positionNow[1][0] = (float(position[1])*math.pi)/180
            print(positionNow)

            break
        #print("Positionerne er nu: "+ str(position[0]) + " og " + str(position[1]))

    return positionNow


def main():
    pos= AskForPosition()
    print(pos)



#while True:
    #pos = AskForPosition()
    #returnmsg = write_read(("I#"+str(20)+","+str(0)))
    #print(returnmsg[1])
    #Acc , velOld, tOld = CalculateAcc(velOld, tOld, returnmsg[1])
    #print("Acc:"+ str(Acc))
    #time.sleep(2)
    #returnmsg1 = write_read("I#"+str(-20)+","+str(0))
    #print(returnmsg1[1])
    #time.sleep(10)

if __name__ == "__main__":
    main()