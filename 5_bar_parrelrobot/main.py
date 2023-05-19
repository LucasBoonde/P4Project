import matlab.engine
import numpy as np
import time
import serial

arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
eng = matlab.engine.start_matlab()
ts = np.loadtxt('ts.txt', delimiter=",")
refq1 = np.loadtxt('refq1.txt', delimiter=",")
refq2 = np.loadtxt('refq2.txt', delimiter=",")
refdq1 = np.loadtxt('refdq1.txt', delimiter=",")
refdq2 = np.loadtxt('refdq2.txt', delimiter=",")
refddq1 = np.loadtxt('refddq1.txt', delimiter=",")
refddq2 = np.loadtxt('refddq2.txt', delimiter=",")

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

#For Calculating Velocity
tOld = np.zeros(1, 2)
#posOld = np.array(positionNow[0], positionNow[1]) #Skal ændres til at den bare bliver til posOld første gange den initializes

tSample = 0.3 #Sample time for control system
i = 0 #Variable resonsible for the itterations in given point
j = 0 #Variable responsible for the current trajectory
tItteration = 0 #number of itterations the current trajectory - Måske skal den være 1?
#numPtsInTraj = (ts+1-ts)/tSample #Number of points in current trajectory. Should be updated when reaching new point.


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
def controlSystem(thRef, dthRef, ddthRef, thNow, dthNow, samplingtime):
    #Teoretiske værdier for control system, skal muligvis ændres
    kp = 39.48
    kd = 12.57
    ki = 10

    ddqControl = ddthRef + kp*(thRef-thNow) + kd*(dthRef-dthNow) + ki*(thRef-thNow)*samplingtime
    return ddqControl


def CalculateAngVelocity(posOld, tOld):
    #Make a 2x2 Matrix That holds the old position of the motor and the new
    #Calculate velocity by: (ThetaNu - Theta Sidste  Sample)/ (Tiden Nu - Tiden Sidste Sample)
    posNew = np.array(positionNow[0], positionNow[1])
    tNew = np.array(time.time(), time.time())

    angVel = np.zeros(1, 2)

    pDif = (posNew - posOld)
    tDif = (tNew - tOld)
    angVel = pDif/tDif

    #After Calculations has been made
    posOld = posNew
    tOld = tNew

    return angVel




def main():
    #Initialize necessary functions
    global i
    posOld = AskForPostion()
    tOld = time.time()
    # Add other functions that should be initialized when the script starts
    # Add input in console, to tell the script to start GOING!

    while True:
        num = input("Enter a number: ")
        if num == "Go":
            current = getCurrent(thNow, dthNow, ddqC)
            # String = (str(current[0]) + ',' + str(current[1]))
            String = ("I" + str(206) + ',' + str(215.74))
            # String =("I" + "#" + str(current[0]) + ',' + str(current[1]))
            # value = write_read(String)

            tTimetoSample = time.time()
            tGlobal = time.time()

            # Make ts = ts[0] og points[0]

            while True:

                tGlobal = time.time() #Sets tStartLoop = actual time

                if tTimetoSample <= tGlobal:
                    tTimetoSample = tTimetoSample + tSample

                    if tItteration == 0: #If itteration is 0, calculate number of points in next trajectory
                        numPtsInTraj = (ts[i+1]-ts[i])/tSample

                    if tItteration == numPtsInTraj: #If tItteration is == points in current trajectory, go to the next one
                        ts[i] = ts[i+1]
                        points[j] = points[j+1]
                        tItteration == 0

                    SendCurrent(current)
                    positionNow = AskForPostion()

                    print(positionNow)
                    print(positionNow[0])
                    print(positionNow[1])

                    SendCurrent(-current)
                    positionNow = AskForPostion()
                    # angVelNow = CalculateAngVelocity(positionNow(0), positionNow(1))

                    sFinLoop = time.time() - tStartLoop # Checks the time at the end.
                    tItteration += 1 #adds one to the itteration
                    




if __name__ == "__main__":
    main()
