"""
SUMMARY

Vehicle class to execute Q-learning on
"""

class Vehicle(object):

    # nx, ny: Number of x, y cells divisions (total number of cells = nx*ny)
    # xloc, yloc: Discrete location in x, y coordinates
    # orientation index: 0 -> "N", 1 -> "E", 2 -> "S", 3 -> "W"
    # speed (int), minimum is 0
    # rewards_matrix: Rewards matrix, must be constructed in the same way as the Q matrix
    def __init__(self, nx, ny, xloc, yloc, orientation_index, speed, speed_max, rewards_matrix):
        self.nx = nx
        self.ny = ny

        self.xloc = xloc
        self.yloc = yloc

        self.orientation_index = orientation_index
        self.speed = speed
        self.speed_max = speed_max

        self.rewards_matrix = rewards_matrix


    # Executes an action
    # 0->"Forwards", 1->"Turn left", 2->"Turn Right", 3->"Accelerate", 4->"Decelerate"
    # modify_self: If true, modifies 

    # Return [None/copy there Vehicle object, None/end location [[xloc, yloc], orientation index, speed]
    def execute_action(self, action_index, modify_self=True, get_copy_there=True, get_end_location=True):

        end_orientation = self.orientation_index
        end_speed = self.speed

        if action_index == 0:
            reached_positions = move_forwards_with_current_speed(self.xloc, self.yloc, self.orientation_index, self.speed)
            orientation_at_step = (end_speed + 1)*[self.orientation_index]

        elif (action_index == 1) or (action_index == 2):
            reached_positions = move_forwards_with_current_speed(self.xloc, self.yloc, self.orientation_index, self.speed)
            orientation_at_step = (end_speed + 1)*[self.orientation_index]
            end_orientation = turn_direction(end_orientation, action_index)

            reached_positions += move_forwards_with_current_speed(reached_positions[-1][0], reached_positions[-1][1], end_orientation, self.speed)
            orientation_at_step += (end_speed + 1)*[end_orientation]

        elif action_index == 3:
            reached_positions = move_forwards_with_current_speed(self.xloc, self.yloc, self.orientation_index, self.speed)
            orientation_at_step = (end_speed + 1)*[self.orientation_index]
            end_speed = self.increase_speed(end_speed)

        elif action_index == 4:
            reached_positions = move_forwards_with_current_speed(self.xloc, self.yloc, self.orientation_index, self.speed)
            orientation_at_step = (end_speed + 1)*[self.orientation_index]
            end_speed = self.reduce_speed(end_speed)


        # If an intermediate location is not valid (as per the rewards matrix) then the vehicle stops there
        for nvnv in range(0, len(reached_positions)):
            x_end, y_end = reached_positions[nvnv]
            end_orientation = orientation_at_step[nvnv]

            # If a location is outside the map, it simply reverts back to the previous position, stops
            # Assumed that the starting location is within the map
            if not self.location_is_within_boundaries(x_end, y_end):
                x_end, y_end = reached_positions[nvnv - 1]
                end_orientation = orientation_at_step[nvnv - 1]
                end_speed = 0
                break

            # If the location is an obstacle or not part of the circuit, ends there
            elif self.rewards_matrix[x_end][y_end] == -100:
                break



        # Modifies object itself if needed
        if self.rewards_matrix:
            self.xloc = x_end
            self.yloc = y_end
            self.orientation_index = end_orientation
            self.speed = end_speed


        vehicle_copy_at_end = None
        state_at_end = None

        # Creates a vehicle copy at the end if needed
        if get_copy_there:
            vehicle_copy_at_end = Vehicle(self.nx, self.ny, x_end, y_end, end_orientation, end_speed, self.speed_max, self.rewards_matrix)

        if get_end_location:
            state_at_end = [[x_end, y_end], end_orientation, end_speed]


        # Returns
        return [vehicle_copy_at_end, state_at_end]



    # Checks if a location is within the boundaries
    def location_is_within_boundaries(self, xcord, ycord):
        return location_is_within_z(xcord, 0, self.nx) and location_is_within_z(ycord, 0, self.ny)


    # Reduces the speed, returns the updated speed
    def reduce_speed(self, start_speed):
        return max(0, start_speed - 1)


    # Increases the speed, returns the updated speed
    def increase_speed(self, start_speed):
        return min(self.speed_max, start_speed + 1)




# Checks if a locations is between 2 values. i.e. z_min <= z < z_max
def location_is_within_z(z, z_min, z_max):
    return (z_min <= z) and (z < z_max)


# Turns the direction, returns the new direction
def turn_direction(start_direction, instruction):
    if instruction == 1:
        adder = -1
    else:
        adder = +1

    after_orientation = start_direction + adder

    if after_orientation < 0:
        return 3
    elif after_orientation > 3:
        return 0
    else:
        return after_orientation


# Moves with a certain speed in the given orientation, returns the updated coordinates
# Returns positions along the way [[x1, y1], ...] including the last one
def move_forwards_with_current_speed(start_x, start_y, start_direction, current_speed):

    # 0 -> "N", 1 -> "E", 2 -> "S", 3 -> "W"

    if start_direction == 0:
        up = 1
        right = 0
    elif start_direction == 1:
        up = 0
        right = 1
    elif start_direction == 2:
        up = -1
        right = 0
    elif start_direction == 3:
        up = 0
        right = -1

    positions_along_the_way = []

    # +1 so that the current speed is handled
    for a_speed_step in range(0, current_speed+1):
        positions_along_the_way.append([start_x + a_speed_step*right, start_y + a_speed_step*up])

    return positions_along_the_way
