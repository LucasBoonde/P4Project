import matlab.engine
import numpy as np
import time
import serial
import cv2 as cv
import math


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


#Den nuværende position for motor 1 og 2
thNow = np.zeros((2,1))
thNow[0][0] = 3.79
thNow[1][0] = 3.07


#Den nuværende hastighed for motor 1 og 2
dthNow  = np.zeros((2,1))
dthNow[0][0] = -0.05
dthNow[1][0] = 0.02
#Accleration regnet fra controler
ddthNow  = np.zeros((2,1))
ddthNow[0][0] = -2.50
ddthNow[1][0] = 1.12



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
    tau = eng.dynamic(thNow[0][0], thNow[1][0], dthNow[0][0], dthNow[1][0], ddqC[0][0], ddqC[1][0])
    print(tau)
    tau = np.around(tau, decimals=4).astype(float)
    kt = 1.62
    current = np.round(np.divide(tau, kt) * 1000, decimals=2)
    # Deadband for Motor 1
    if 0 < current[0]:
        current[0] += 100

    if current[0] < 0:
        current[0] -= 100

    # Deadband for Motor 2
    if 0 < current[1]:
        current[1] += 100

    if current[1] < 0:
        current[0] -= 100
    current1, current2 = float(current[0]), float(current[1])
    current = np.array([[current1], [current2]])
    print("current: " + str(current[0][0]) + " og " + str(current[1][0]))
    return current









def SendCurrent(current):
    while True:
        positionNow = np.zeros((2, 1))
        message = ("I#"+str(current[0][0]) + ',' + str(current[1][0]))
        #message = ("I#" + str(0) + ',' + str(0))
        returnMessage = write_read(message)
        if returnMessage[0] == "I":
            position = returnMessage[1].split(",")
            positionNow[0][0] = (float(position[0]) * math.pi) / 180
            positionNow[1][0] = (float(position[1]) * math.pi) / 180
            break

    return positionNow


def AskForPostion():
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
def controlSystem(thNow, dthNow, samplingtime, samplingsIterations, path):
    #Teoretiske værdier for control system, skal muligvis ændres

    kp = 39.48
    kd = 12.57
    ki = 10
    kp = 7.814
    kd = 6.861
    ki = 2.166

    ddqControl = np.zeros((2,1))
    thRef = np.zeros((2,1))
    thRef[0][0] = refq1[path][samplingsIterations]
    thRef[1][0] = refq2[path][samplingsIterations]
    string = ("I#"+str(thRef[0][0]) + ',' + str(thRef[1][0]))
    write_read(string)
    #dthRef = np.zeros((2, 1))
    #dthRef[0][0] = refdq1[path][samplingsIterations]
    #dthRef[1][0] = refdq2[path][samplingsIterations]
    #ddthRef = np.zeros((2, 1))
    #ddthRef[0][0] = refddq1[path][samplingsIterations]
    #ddthRef[1][0] = refddq2[path][samplingsIterations]


    #ddqControl[0] = ddthRef[0][0] + kp * (thRef[0][0] - thNow[0][0]) + kd*(dthRef[0][0] - dthNow[0][0]) + ki * (thRef[0][0] - thNow[0][0]) * samplingtime
    #ddqControl[1] = ddthRef[1][0] + kp * (thRef[1][0] - thNow[1][0]) + kd*(dthRef[1][0] - dthNow[1][0]) + ki * (thRef[1][0] - thNow[1][0]) * samplingtime

    #return ddqControl


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
    positionNow = posOld

    tOld = time.time()
    tSample = 0.2  # Sample time for control system
    i = 0  # Variable resonsible for the itterations in given point
    j = 0  # Variable responsible for the current trajectory
    tItteration = 0  # number of itterations the current trajectory - Måske skal den være 1?






    # Add other functions that should be initialized when the script starts
    # Add input in console, to tell the script to start GOING!
    while True:
        txtInput = input("Skriv Go for at starte programmet: ")
        if txtInput == "Go":

            tTimetoSample = time.time()


            # Make ts = ts[0] og points[0]

            while True:

                tGlobal = time.time()  # Sets tStartLoop = actual time

                if tTimetoSample <= tGlobal:
                    tStarLoop = time.time()
                    tTimetoSample = tTimetoSample + tSample

                    if tItteration == 0:  # If itteration is 0, calculate number of points in next trajectory
                        numPtsInTraj = round((ts[i + 1] - ts[i]) / tSample)

                    if tItteration >= numPtsInTraj:  # If tItteration is == points in current trajectory, go to the next one
                        # ts[i] = ts[i + 1]
                        # points[j] = points[j + 1]
                        tItteration = 0
                        i += 1
                        j += 1

                    controlSystem(0,0,0,samplingsIterations=tItteration,path=j)
                    #angVelNow, posOld, tOld = CalculateAngVelocity(posOld, tOld, positionNow)
                    #accNow = controlSystem(positionNow, angVelNow, samplingtime=tSample, samplingsIterations=tItteration, path=j)
                    #print("acc: "+ str(accNow))

                    #current = getCurrent(positionNow, angVelNow, accNow)
                    #positionNow = SendCurrent(current)
                    #print("postion:" + str(positionNow))


                    sFinLoop = time.time() - tStarLoop  # Checks the time at the end.
                    tItteration += 1  # adds one to the itteration
                    print("Loop took: ", + sFinLoop, str(" Seconds"))
                    print("-----------------------------------------")
                    print("---------------")
                    print("---------------")
                    print("At Itteration: ", + tItteration)
                    print("-----------------------------------------")
                    print("Working on crack: ", + j + 1, str("and currently at: "), + i + 1, str("of: "),
                          + numPtsInTraj, str("points"))
                    print("-----------------------------------------")
                if i >= len(ts) and j >= len(ts):
                    i = 0
                    j = 0
                    break

                k = cv.waitKey(1)
                if k == ord('q'):
                    break

if __name__ == "__main__":
    main()