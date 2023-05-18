coordinates = [(120, 150), (130, 160), (140, 170), (150, 180), (160, 190),
               (110, 120), (170, 130), (180, 140), (190, 150), (200, 160)]

# Iterate through the coordinates list starting from the second point
for i in range(1, len(coordinates)):
    current_point = coordinates[i]
    previous_point = coordinates[i - 1]

    difference_x = current_point[0] - previous_point[0]
    difference_y = current_point[1] - previous_point[1]

    print(f"Difference from {previous_point} to {current_point}: Δx = {difference_x}, Δy = {difference_y}")