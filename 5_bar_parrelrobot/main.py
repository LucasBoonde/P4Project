import matlab.engine
import numpy as np
import time
import serial
import cv2 as cv


arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
eng = matlab.engine.start_matlab()
ts = np.loadtxt('ts.txt', delimiter=",")
refq1 = np.loadtxt('refq1.txt', delimiter=",")
refq2 = np.loadtxt('refq2.txt', delimiter=",")
refdq1 = np.loadtxt('refdq1.txt', delimiter=",")
refdq2 = np.loadtxt('refdq2.txt', delimiter=",")
refddq1 = np.loadtxt('refddq1.txt', delimiter=",")
refddq2 = np.loadtxt('refddq2.txt', delimiter=",")
# For Calculating Velocity
tOld = np.zeros((1,2))
Ti = 0.1

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


#posOld = np.array(positionNow[0], positionNow[1]) #Skal ændres til at den bare bliver til posOld første gange den initializes

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

def getCurrent(thNow,dthNow,ddqC):

    tau = eng.dynamic(thNow[0], thNow[1], dthNow[0], dthNow[1], ddqC[0], ddqC[1])
    tau = np.array(np.around(tau, decimals=2), dtype=float)
    print("tau: " +str(tau))
    kt = 1.62
    current = np.divide(tau, kt)
    current = np.around(current, decimals=2)
    print("type: " + str(type(current[1])))
    current1 = (float(current[0]))
    current2 = (float(current[1]))

    current = np.zeros((2,1))
    current[0] = current1
    current[1] = current2
    return current


def SendCurrent(current):
    while True:
        message = ("I#"+str(current[0]) + ',' + str(current[1]))
        returnMessage = write_read(message)
        if returnMessage[0] == "I":
            break


def AskForPostion():
    while True:

        message = ("P#")
        positionNow = np.zeros((2,1))
        returnMessage = write_read(message)
        if returnMessage[0] == "P":
            position = returnMessage[1].split(",")
            positionNow[0] = float(position[0])
            positionNow[1] = float(position[1])
            positionNow[0] = 3.79
            positionNow[1] = 3.07

            break
        #print("Positionerne er nu: "+ str(position[0]) + " og " + str(position[1]))

    return positionNow
def controlSystem(thNow, dthNow, samplingtime, samplingsIterations, path):
    #Teoretiske værdier for control system, skal muligvis ændres
    kp = 39.48
    kd = 12.57
    ki = 10
    ddqControl = np.zeros((2,1))
    thRef = np.zeros((2,1))
    thRef[0] = refq1[path][samplingsIterations]
    thRef[1] = refq2[path][samplingsIterations]
    dthRef = np.zeros((2, 1))
    dthRef[0] = refdq1[path][samplingsIterations]
    dthRef[1] = refdq2[path][samplingsIterations]
    ddthRef = np.zeros((2, 1))
    ddthRef[0] = refddq1[path][samplingsIterations]
    ddthRef[1] = refddq2[path][samplingsIterations]


    ddqControl[0] = ddthRef[0] + kp *(thRef[0]-thNow[0]) + kd*(dthRef[0]-dthNow[0]) + ki*(thRef[0]-thNow[0])*samplingtime
    ddqControl[1] = ddthRef[0] + kp *(thRef[0]-thNow[0]) + kd*(dthRef[0]-dthNow[0]) + ki*(thRef[0]-thNow[0])*samplingtime

    return ddqControl


def CalculateAngVelocity(posOld, tOld, positionNow):
    #Make a 2x2 Matrix That holds the old position of the motor and the new
    #Calculate velocity by: (ThetaNu - Theta Sidste  Sample)/ (Tiden Nu - Tiden Sidste Sample)
    posNew = positionNow
    tNew = time.time()
    pDif = np.zeros(shape= [2,1])
    pDif[0] = posNew[0]-posOld[0]
    pDif[1] = posNew[1]-posOld[1]

    tDif = (tNew - tOld)
    angVel = pDif/tDif

    #After Calculations has been made
    posOld = posNew
    tOld = tNew

    return angVel, posOld, tOld




def main():
    #Initialize necessary functions
    posOld = AskForPostion()
    tOld = time.time()


    # Add other functions that should be initialized when the script starts
    # Add input in console, to tell the script to start GOING!
    while True:
        num = input("Enter a number: ")
        if num == "Go":
            while True:

                positionNow = AskForPostion()

                angVelNow, posOld, tOld = CalculateAngVelocity(posOld, tOld, positionNow)
                print(angVelNow)

                accNow= controlSystem(positionNow,angVelNow, samplingtime=Ti, samplingsIterations=1, path=1)
                print("acc"+str(accNow))
                current = getCurrent(positionNow, angVelNow, accNow)
                SendCurrent(current)






                k = cv.waitKey(1)
                if k == ord('q'):
                    break

if __name__ == "__main__":
    main()
