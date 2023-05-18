import math

def distance_calculator(p_1,p_2):
    x_1, y_1 = p_1
    x_2, y_2 = p_2
    return math.sqrt((x_2-x_1)**2 + (y_2-y_1)**2) 


def accomp_pos_check(currentPos, list_with_points, threshold):
    for i, endPos in enumerate (list_with_points):
        distance = distance_calculator(currentPos, endPos)
        if distance <= threshold:
            return True, endPos, i
    return False, None, None

currentPos = [(3, 4)]
list_with_points = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12)]
threshold = 1

accomp, accomp_position = accomp_pos_check(currentPos, list_with_points, threshold)
if accomp:
    print(f"End position accomplished: {accomp_position}")
    if index + 1 < len(list_with_points):
        next_position = list_with_points[index + 1]
        print(f"Going to next position: {next_position}")
else:
    print("End position not accomplished")




