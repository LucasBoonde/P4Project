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
        time.sleep(0.05)
        data = arduino.readline().decode().strip()
        parts = data.split("#")
        print(parts)
        if len(parts) > 1 and parts[len(parts)-1] == "Modtaget":  #Kig efter om det sidste element i den modtagene besked er en Stopbesked
            break

    values = parts[0].split(",")
    print("Values:"+ str(values))
    print("Values er: "+ str(values[0]) + " og " + str(values[1]))
    return values

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



def controller(M, H, qref, dqref, ddqref, q, dq):
    kp = 0
    kd = 0

    indputq = ddqref + kp*(qref-q)+kd*(dqref-dq)
    tau = M * indputq + H

    return tau



while True:
    num = input("Enter a number: ")
    if num == "Go":
        current = getCurrent(thNow, dthNow, ddqC)
        String = (str(current[0]) + ',' + str(current[1]))
        value = write_read(String)
        print(value)



