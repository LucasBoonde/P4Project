import socket

# IP address and port number of the MATLAB script
ipAddress = '172.26.50.145'  # Replace with the IP address of the MATLAB script
port = 65204             # Replace with the port number used in the MATLAB script

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
sock.bind((ipAddress, port))

# Listen for incoming connections
sock.listen(1)

# Accept the connection
conn, addr = sock.accept()
print('Connected by', addr)

# Receive data from MATLAB in a loop
while True:
    dataReceived = conn.recv(1024).decode()  # Adjust buffer size as needed
    if not dataReceived:
        break
    print('Received:', dataReceived)

# Close the connection
conn.close()
