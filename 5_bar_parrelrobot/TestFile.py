import numpy as np
import time

tSample = 0.1 #Sample time for control system
i = 0 #Variable resonsible for the itterations in given point
j = 0 #Variable responsible for the current trajectory
tItteration = 0 #number of itterations the current trajectory - Måske skal den være 1?

ts = [0,1,2,3]
points = [10, 20, 30, 40]
len(points)


while True:
    num = input("Enter a number: ")
    if num == "Go":
        #current = getCurrent(thNow, dthNow, ddqC)
        # String = (str(current[0]) + ',' + str(current[1]))
        String = ("I" + str(206) + ',' + str(215.74))
        # String =("I" + "#" + str(current[0]) + ',' + str(current[1]))
        # value = write_read(String)

        tTimetoSample = time.time()
        tGlobal = time.time()

        # Make ts = ts[0] og points[0]

        while True:

            tGlobal = time.time()  # Sets tStartLoop = actual time

            if tTimetoSample <= tGlobal:
                tStarLoop = time.time()
                tTimetoSample = tTimetoSample + tSample

                if tItteration == 0:  # If itteration is 0, calculate number of points in next trajectory
                    numPtsInTraj = (ts[i + 1] - ts[i]) / tSample


                if tItteration >= numPtsInTraj:  # If tItteration is == points in current trajectory, go to the next one
                    #ts[i] = ts[i + 1]
                    #points[j] = points[j + 1]
                    tItteration = 0
                    i += 1
                    j += 1

                #SendCurrent(current)
                #positionNow = AskForPostion()

                #print(positionNow)
                #print(positionNow[0])
                #print(positionNow[1])

                #SendCurrent(-current)
                #positionNow = AskForPostion()
                # angVelNow = CalculateAngVelocity(positionNow(0), positionNow(1))

                sFinLoop = time.time() - tStarLoop  # Checks the time at the end.
                print("Loop took: ", + round(sFinLoop, 6),  str(" Seconds"))
                print("-----------------------------------------")
                print("---------------")
                print("---------------")
                print("At Itteration: ", + tItteration)
                print("-----------------------------------------")
                print("Working on crack: ", + j+1, str("and currently at: "), + i+1, str("of: "), + numPtsInTraj, str("points"))
                print("-----------------------------------------")

                tItteration += 1  # adds one to the itteration


            if i >= len(ts) and j >= len(points):
                i = 0
                j = 0
                break




if __name__ == "__main__":
    main()