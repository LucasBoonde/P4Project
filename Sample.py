import time
import random

# Set the desired sampling frequency (in Hz)
sampling_frequency = 10  # 10 samples per second

while True:
    # Start time of the sample
    start_time = time.time()

    # Simulate data sampling from a sensor (random number generation)
    sensor_data = random.random()

    # Replace the above line with your actual code to sample the data from the sensor

    # Print or process the sampled sensor data
    print(sensor_data)

    # Calculate the elapsed time for the sampling
    elapsed_time = time.time() - start_time

    # Calculate the delay required to achieve the desired sampling frequency
    delay = 1 / sampling_frequency - elapsed_time

    # Check if the delay is positive (i.e., sampling is faster than the desired frequency)
    if delay > 0:
        time.sleep(delay)
