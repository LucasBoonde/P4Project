import serial

# Configure the serial port
ser = serial.Serial('COM4', 9600)  # Replace 'COM3' with the appropriate port name for your Arduino


# Function to send torque value to Arduino
def send_torque_value(torque):
    # Convert the torque value to bytes
    torque_bytes = str(torque).encode('utf-8')

    # Send the torque value to Arduino
    ser.write(torque_bytes)


# Example usage: send a torque value of 50
send_torque_value(50)

# Close the serial port
ser.close()
