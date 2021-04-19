/*
SUMMARY

Vehicle controlled by the user
*/


class Vehicle {

  // nx, ny: Number of x, y cells divisions (total number of cells = nx*ny)
  // xloc, yloc: Discrete location in x, y coordinates
  // orientation index: 0 -> "N", 1 -> "E", 2 -> "S", 3 -> "W"
  // speed (int), minimum is 0
  // rewards_matrix: Rewards matrix, must be constructed in the same way as the Q matrix

  constructor(nx, ny, xloc, yloc, orientation_index, speed, speed_max, rewards_matrix) {
    this.nx = nx
    this.ny = ny

    this.xloc = xloc
    this.yloc = yloc

    this.orientation_index = orientation_index
    this.speed = speed
    this.speed_max = speed_max

    this.rewards_matrix = rewards_matrix
  }

  // Executes an action
  // 0->"Forwards", 1->"Turn left", 2->"Turn Right", 3->"Accelerate", 4->"Decelerate"
  // modify_self: If true, modifies 

  // Return [None/copy there Vehicle object, None/end location [[xloc, yloc], orientation index, speed]
  execute_action(action_index, modify_self=True, get_copy_there=True, get_end_location=True) {

    let end_orientation = this.orientation_index;
    let end_speed = this.speed;

    // Placeholder values
    let reached_positions = [];
    let orientation_at_step = 0;

    if (action_index === 0) {
      reached_positions = move_forwards_with_current_speed(this.xloc, this.yloc, this.orientation_index, this.speed);
      orientation_at_step = (end_speed + 1)*[this.orientation_index];
    } else if ((action_index === 1) || (action_index === 2)) {
      reached_positions = move_forwards_with_current_speed(this.xloc, this.yloc, this.orientation_index, this.speed);
      orientation_at_step = (end_speed + 1)*[this.orientation_index];
      end_orientation = turn_direction(end_orientation, action_index);

      reached_positions.concat(move_forwards_with_current_speed(reached_positions[-1][0], reached_positions[-1][1], end_orientation, this.speed));
      orientation_at_step += (end_speed + 1)*[end_orientation];
    } else if (action_index === 3) {
      reached_positions = move_forwards_with_current_speed(this.xloc, this.yloc, this.orientation_index, this.speed);
      orientation_at_step = (end_speed + 1)*[this.orientation_index];
      end_speed = this.increase_speed(end_speed);
    } else if (action_index === 4) {
      reached_positions = move_forwards_with_current_speed(this.xloc, this.yloc, this.orientation_index, this.speed);
      orientation_at_step = (end_speed + 1)*[this.orientation_index];
      end_speed = this.reduce_speed(end_speed);
    }

    // If an intermediate location is not valid (as per the rewards matrix) then the vehicle stops there
    for (let nv = 0; nv < reached_positions.length; nv++) {
      x_end = reached_positions[nv][0];
      y_end = reached_positions[nv][1];
      end_orientation = orientation_at_step[nv];

      // If a location is outside the map, it simply reverts back to the previous position, stops
      // Assumed that the starting location is within the map
      if (! this.location_is_within_boundaries(x_end, y_end)) {
        x_end = reached_positions[nv - 1][0];
        y_end = reached_positions[nv - 1][1];
        end_orientation = orientation_at_step[nv - 1];
        end_speed = 0;
        break;
      }
      // If the location is an obstacle or not part of the circuit, ends there
      else if (this.rewards_matrix[x_end][y_end] === -100) {
        break;
      }
    }

    // Modifies vehicle itself if needed
    if (this.modify_self) {
      this.xloc = x_end;
      this.yloc = y_end;
      this.orientation_index = end_orientation;
      this.speed = end_speed;
    }

    let vehicle_copy_at_end = null;
    let state_at_end = null;

    // Creates a vehicle copy at the end if needed
    if (get_copy_there) {
      vehicle_copy_at_end = new Vehicle(this.nx, this.ny, x_end, y_end, end_orientation, end_speed, this.speed_max, this.rewards_matrix);
    }

    // Obtains end conditions if needed
    if (get_end_location) {
      state_at_end = [[x_end, y_end], end_orientation, end_speed];
    }

    return [vehicle_copy_at_end, state_at_end];
  }


  // Checks if a location is within the boundaries
  location_is_within_boundaries(xcord, ycord) {
    return location_is_within_z(xcord, 0, this.nx) && location_is_within_z(ycord, 0, this.ny);
  }


  // Reduces the speed, returns the updated speed
  reduce_speed(start_speed) {
    return Math.max(0, start_speed - 1);
  }


  // Increases the speed, returns the updated speed
  increase_speed(start_speed) {
    return min(this.speed_max, start_speed + 1);
  }
}



// Checks if a locations is between 2 values. i.e. z_min <= z < z_max
function  location_is_within_z(z, z_min, z_max) {
  return (z_min <= z) && (z < z_max);
}


// Turns the direction, returns the new direction
function turn_direction(start_direction, instruction) {
  let adder = 0;
  if (instruction === 1) {
    adder = -1;
  } else {
    adder = 1;
  }

  let after_orientation = start_direction + adder;

  if (after_orientation < 0) {
    return 3;
  } else if (after_orientation > 3) {
    return 0;
  } else {
    return after_orientation;
  }
}


// Moves with a certain speed in the given orientation, returns the updated coordinates
// Returns positions along the way [[x1, y1], ...] including the last one
function move_forwards_with_current_speed(start_x, start_y, start_direction, current_speed) {

  // 0 -> "N", 1 -> "E", 2 -> "S", 3 -> "W"
  let up =0;
  let right = 0;

  if (start_direction === 0) {
    up = 1;
    right = 0;
  } else if (start_direction === 1) {
    up = 0;
    right = 1;
  } else if (start_direction === 2) {
    up = -1;
    right = 0;
  } else if (start_direction === 3) {
    up = 0;
    right = -1;
  }

  let positions_along_the_way = [];

  // # +1 so that the current speed is handled
  for (let a_speed_step = 0; a_speed_step < (current_speed+1); a_speed_step++) {
    positions_along_the_way.push([start_x + a_speed_step*right, start_y + a_speed_step*up]);
  }

  return positions_along_the_way;
}