import serial

# Establish serial communication
ser = serial.Serial('COM4', 9600)  # Replace 'COM3' with your Arduino's serial port

while True:
    if ser.in_waiting > 0:
        # Read the incoming theta value
        theta_str = ser.readline().decode().rstrip()
        theta = float(theta_str)

        # Process the received theta value
        print("Received theta:", theta)

ser.close()  # Close the serial connection when finished
