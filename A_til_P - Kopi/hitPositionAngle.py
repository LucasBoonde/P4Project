import math


def get_theta_difference(theta1, theta2):
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    return math.degrees(abs(theta2_rad - theta1_rad))

def check_accomp_pos(current_theta, desired_theta, threshold):
    for i in range(len(current_theta)):
        theta_difference = get_theta_difference(current_theta[i], desired_theta[i])
        if theta_difference > threshold:
            return False, None
    return True, desired_theta

current_theta = [86, 46]
desired_theta = [[90, 45], [60, 30]]
threshold = 5

accomp, accomp_theta = check_accomp_pos(current_theta, desired_theta[0], threshold)
if accomp:
    print(f"Desired angle accomplished: {accomp_theta}")
else:
    print("Desired angle not accomplished")

