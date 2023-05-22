import matlab.engine
import numpy as np
import time
import serial
import math


arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)

eng = matlab.engine.start_matlab()


def write_until_answer(x):

    while True:
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline().decode().strip()
        parts = data.split("#")
        if len(parts) > 1 and parts[len(parts) - 1] == "M": #Kig efter om det sidste element i den modtagene besked er en Stopbesked
            break

    return parts


def SendCurrentReceivePosition(current):
    while True:
        message = ("I#"+str(current[0]) + ',' + str(current[1]))
        print("Besked fra PC:" + str(message))
        print("-----------------------------------------")
        returnMessage = write_until_answer(message)

        #Svaret bliver læst når start bit I er spottet:
        if returnMessage[0] == "I":
            print("Return message" + str(returnMessage))
            print("-----------------------------------------")

            positionNow = returnMessage[1].split(",")
            positionNow[0] = (float(positionNow[0]) * math.pi) / 180
            positionNow[1] = (float(positionNow[1]) * math.pi) / 180

            velocityNow = returnMessage[2].split(",")
            velocityNow[0] = float(velocityNow[0])
            velocityNow[1] = float(velocityNow[1])

            break

    return positionNow, velocityNow


def main():
    ZeroCurrent = np.array([0, 0])
    posOld, velOld = SendCurrentReceivePosition(ZeroCurrent)

    print("Position start:" + str(posOld))
    print("-----------------------------------------")
    print("Velocity start:" + str(velOld))
    print("-----------------------------------------")


    # Add other functions that should be initialized when the script starts
    # Add input in console, to tell the script to start GOING!
    while True:
        txtInput = input("Skriv Go for at starte programmet: ")
        if txtInput == "Go":


            while True:
                    Current1 = np.array([150, 0])
                    Current2 = np.array([-150, 0])

                    positionNow, velocityNow = SendCurrentReceivePosition(Current1)

                    print("Position now:" + str(positionNow))
                    print("-----------------------------------------")
                    print("Velocity now:" + str(velocityNow))
                    print("-----------------------------------------")
                    time.sleep(0.1)

                    positionNow, velocityNow = SendCurrentReceivePosition(Current2)
                    
                    print("Position now:" + str(positionNow))
                    print("-----------------------------------------")
                    print("Velocity now:" + str(velocityNow))
                    print("-----------------------------------------")
                    time.sleep(0.1)






if __name__ == "__main__":
    main()