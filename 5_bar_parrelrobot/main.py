import matlab.engine
import numpy as np
import time
import serial

arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
eng = matlab.engine.start_matlab()

#Den nuværende position for motor 1 og 2
th1Now = 3.79
th2Now = 3.07
#Den nuværende hastighed for motor 1 og 2
dth1Now = -0.05
dth2Now = 0.02
#Accleration regnet fra controler
ddq1C = -2.50
ddq2C = 1.12
thNow = np.array([[th1Now], [th2Now]], dtype=float)
dthNow = np.array([[dth1Now], [dth2Now]], dtype=float)
ddqC = np.array([[ddq1C], [ddq2C]])
def write_read(x):

    while True:
        arduino.write(bytes(x, 'utf-8'))
        print(x)

        time.sleep(0.05)
        data = arduino.readline().decode().strip()



        parts = data.split("#")

        print(parts)

        if len(parts) > 1 and parts[len(parts) - 1] == "Modtaget": #Kig efter om det sidste element i den modtagene besked er en Stopbesked
            break

    return parts

def getCurrent(thNow,dthNow,ddqC):
    tau = eng.dynamic(thNow[0], thNow[1], dthNow[0], dthNow[1], ddqC[0], ddqC[1])
    tau = np.array(np.around(tau, decimals=2), dtype=float)
    kt = 1.62
    current = np.divide(tau, kt)
    current = np.around(current, decimals=2)
    current1 = (float(current[0]))
    current2 = (float(current[1]))
    current = np.array([current1,current2])
    return current


def SendCurrent(current):
    message = ("I"+"#"+str(current[0]) + ',' + str(current[1]))
    String = ("I#" + str(206) + ',' + str(215.74))
    write_read(message)

def AskForPostion():
    while True:
        message = ("P"+"#")
        returnMessage = write_read(message)
        position = returnMessage[1].split(",")
        print(position[0])
        if returnMessage[0] == "position":
            break


        #print("Positionerne er nu: "+ str(position[0]) + " og " + str(position[1]))
    return position



while True:
    num = input("Enter a number: ")
    if num == "Go":
        current = getCurrent(thNow, dthNow, ddqC)
        #String = (str(current[0]) + ',' + str(current[1]))
        String = ("I"+str(206) + ',' + str(215.74))
        #String =("I" + "#" + str(current[0]) + ',' + str(current[1]))
        #value = write_read(String)
        while True:
            SendCurrent(current)
            positionNow = AskForPostion()

            print(positionNow)
            print(positionNow[0])
            print(positionNow[1])

            SendCurrent(-current)
            positionNow = AskForPostion()



