/*
SUMMARY

Necessary functions for driving
*/

// Intention placeholder
var chosen_intention = null;

//Processes the entire driving setup
async function process_driving_conditions() {

  let c = document.getElementById("circuit_selected");
  let chosen_circuit = c.options[c.selectedIndex].value;

  let i = document.getElementById("intention");
  // Positive intention
  chosen_intention = i.options[i.selectedIndex].value;

  let API_result = await POST_JSON_return_JSON("/retrieve_circuit_vehicle", {"circuit": chosen_circuit});

  // Clears any possible error messages
  clear_div_contents("cv errors");

  let output = API_result["Output"];

  if (output == "Failure") {
    // Show error message
    document.getElementById("cv errors").append(create_error_message("ERROR", API_result["Cause"], "Error selecting driving environment"));
    return;
  }

  // Deletes the middle div's contents
  clear_div_contents("center");

  // Updates the size of the center div
  let total_window_height = window.innerHeight;

  // Gets the navbar and footer's heights
  let navbar_height = document.getElementById("top navbar").offsetHeight;
  let footer_height = document.getElementById("actual footer").offsetHeight;

  let center_div_height = total_window_height - navbar_height - footer_height;

  document.getElementById("center").style.height = center_div_height.toString() + "px";

  // Delete the underfooter
  document.getElementById("bottom_underfooter").remove();

  let center_contents_JSON = {"<>":"table", "class":"driving_table", "html":[
    {"<>":"tr", "html":[
      {"<>":"td", "class":"driving_controls", "id":"driving controls", "html":[
        {"<>":"div", "html":[
          {"<>":"h3", "text":"VEHICLE CONTROLS", "class":"center-x"},

          {"<>":"div", "class":"center-x", "html":[
            {"<>":"div", "html":[
              {"<>":"b", "text":"W"},
              {"<>":"span", "text":" Move forwards"},
              {"<>":"br"},

              {"<>":"b", "text":"A"},
              {"<>":"span", "text":" Turn left"},
              {"<>":"br"},

              {"<>":"b", "text":"S"},
              {"<>":"span", "text":" Move backwards"},
              {"<>":"br"},

              {"<>":"b", "text":"R"},
              {"<>":"span", "text":" Accelerate"},
              {"<>":"br"},

              {"<>":"b", "text":"F"},
              {"<>":"span", "text":" Decelerate"},
            ]}
          ]},

          {"<>":"br"},

          {"<>":"h3", "text":"VEHICLE DATA", "class":"center-x"},
          {"<>":"br"},

          {"<>":"div", "class":"center-x", "html":[
            {"<>":"div", "html":[

              {"<>":"b", "text":"Orientation "},
              {"<>":"span", "text":"N", "id":"vehicle orientation"},
              {"<>":"br"},

              {"<>":"b", "text":"Speed "},
              {"<>":"span", "text":"0", "id":"vehicle speed"},
            ]}
          ]},

          {"<>":"br"}
        ]}
      ]},
      {"<>":"td", "class":"driving_area", "id":"driving area"}
    ]
    }
  ]
  }

  let center_contents = json2html.transform({}, center_contents_JSON);
  replace_element_HTML_contents("center", center_contents);

  var driving_area_to_be_drawn = document.getElementById("driving area");

  da_ow = driving_area_to_be_drawn.offsetWidth;
  da_oh = driving_area_to_be_drawn.offsetHeight;

  var driving_area_to_be_drawn_params = { width: da_ow, height: da_oh};
  two = new Two(driving_area_to_be_drawn_params);
  two.appendTo(driving_area_to_be_drawn);

  // Gets the reward matrix
  R = API_result["rewards matrix"];


  // Gets the necessary requirements for accounting for measurements
  Δx = API_result["Δx"];
  Δy = API_result["Δy"];
  nx = API_result["nx"];
  ny = API_result["ny"];

  // Vehicle data
  let speed_max = API_result["possible speeds"];

  circuit_xy_minmax = [[0, nx], [0, ny]];

  // Goal location
  let goal_location = API_result["goal discrete location"];

  // Draws the goal location
  draw_cell(goal_location, "Green", 3, "ForestGreen", "goal cell");

  // Valid cells
  valid_positions = API_result["valid positions"];

  // Draws the valid positions
  for (let mt = 0; mt < valid_positions.length; mt++) {
    draw_cell(valid_positions[mt], "LightGrey", 3, "Grey", "valid position " + mt.toString());
  }

  // Renders the background
  two.update();


  // Selects a random start location
  let random_start_index = Math.floor(Math.random() * (valid_positions.length - 0)) + 0;
  // In the extreme case when the random number obtained is 1
  random_start_index = Math.min(random_start_index, valid_positions.length - 1)
  let start_location = valid_positions[random_start_index];

  let start_orientation = Math.floor(Math.random() * (4 - 0)) + 0;
  // In the extreme case when the random number obtained is 1
  start_orientation = Math.min(start_orientation, 3);
  // Starting speed is always 0
  let start_speed = 0;


  // Generates a vehicle with at the start location
  user_vehicle = new Vehicle(nx, ny, start_location[0], start_location[1], start_orientation, start_speed, speed_max, R);

  // Draws the vehicle for the first time

  // Obtains vehicle values
  let v_x = user_vehicle.xloc;
  let v_y = user_vehicle.yloc;
  let v_o = user_vehicle.orientation_index;
  let v_v = user_vehicle.speed;

  // Draws a triangle there
  // Placeholder
  let current_local_vehicle_coordinates = generate_vehicle_polygon(v_x, v_y, v_o);

  let vehicle_anchors = [];

  for (let ny = 0; ny < current_local_vehicle_coordinates.length; ny++) {
    let item_xy = generate_TWO_xy(current_local_vehicle_coordinates[ny][0], circuit_xy_minmax[0], current_local_vehicle_coordinates[ny][1], circuit_xy_minmax[1], da_ow, da_oh, y_invert=true);
    vehicle_anchors.push(new Two.Anchor(item_xy[0], item_xy[1]));
  }

  drawn_vehicle = new Two.Path(vehicle_anchors, true, false);

  drawn_vehicle.stroke = "MidnightBlue";
  drawn_vehicle.linewidth = 3;
  drawn_vehicle.fill = "MediumBlue";
  drawn_vehicle.id = "vehicle";
  two.add(drawn_vehicle);

  // Renders the vehicle
  two.update();

  // The user can start demonstrating now
  demonstration_in_progress = true;

  // Adds an event listener so that keypresses result in vehicle actions
  window.addEventListener("keypress", vehicle_act);
}



// Updates the location of a point, linearizing its position based on the overall TWO.js coordinates
// Utilizes the normal coordinate way, where y moves from from bottom to top unless, by default
// xc, yc: Current x, y coordinates
// xc_minmax, yc_minmax: Min/Max of the corresponding variable, in the format: [min, max]
// t_width, t_height: two js area width, height (in pixels)
// y_invert: Whether or not to invert the y in order to make y start at the bottom, true by default
function generate_TWO_xy(xc, xc_minmax, yc, yc_minmax, t_width, t_height, y_invert=true) {

  let x = interpolate(xc, xc_minmax[0], xc_minmax[1], 0, t_width);
  let y = interpolate(yc, yc_minmax[0], yc_minmax[1], 0, t_height);

  if (y_invert) {
    y = t_height - y;
  }

  return [x, y]
}



// Interpolates a point
function interpolate(x, x_min, x_max, y_min, y_max) {

  if (x >= x_max) {
    return y_max;
  }

  if (x <= x_min) {
    return y_min;
  }

  let Δ = y_max - y_min;
  return y_min + Δ*(x - x_min)/(x_max - x_min);
}



// Draws a single shape given its external points (assumed no rotation)
// Designed for fixed locations
// polygon_border = [[x1, x2], ...]
function draw_single_item(polygon_border, stroke_color, border_linewidth, fill_color, given_id) {

  let item_anchors = [];

  for (let nv = 0; nv < polygon_border.length; nv++) {
    let item_xy = generate_TWO_xy(polygon_border[nv][0], circuit_xy_minmax[0], polygon_border[nv][1], circuit_xy_minmax[1], da_ow, da_oh, y_invert=true);
    item_anchors.push(new Two.Anchor(item_xy[0], item_xy[1]));
  }

  let single_item = new Two.Path(item_anchors, true, false);
  single_item.stroke = stroke_color;
  single_item.linewidth = border_linewidth;
  single_item.fill = fill_color;
  single_item.id = given_id;
  two.add(single_item);
}



// Draws a cell given its bottom left x, y (BL = [x, y]) values
function draw_cell(BL, stroke_color, border_linewidth, fill_color, given_id) {

  let x_bl = BL[0];
  let y_bl = BL[1];

  // Only add 1 because the Δx, Δy are handled automatically
  let cell_border = [
                    [x_bl, y_bl],
                    [x_bl + 1, y_bl],
                    [x_bl + 1, y_bl + 1],
                    [x_bl, y_bl + 1]
                    ]

  draw_single_item(cell_border, stroke_color, border_linewidth, fill_color, given_id);
}

// Placeholders for drawing area variables
var da_ow = null;
var da_oh = null;


// Generates the polygon for a vehicle based on its current coordinates
function generate_vehicle_polygon(v_x, v_y, v_o) {

  if (v_o == 0) {
    // North
    return [
      [v_x + 0.2, v_y + 0.2],
      [v_x + 0.8, v_y + 0.2],
      [v_x + 0.5, v_y + 0.8]
    ];
  } else if (v_o == 1) {
    // East
    return [
      [v_x + 0.2, v_y + 0.2],
      [v_x + 0.8, v_y + 0.5],
      [v_x + 0.2, v_y + 0.8]
    ];
  } else if (v_o == 2) {
    // South
    return [
      [v_x + 0.8, v_y + 0.8],
      [v_x + 0.2, v_y + 0.8],
      [v_x + 0.5, v_y + 0.2]
    ];
  } else if (v_o == 3) {
    // West
    return [
      [v_x + 0.8, v_y + 0.8],
      [v_x + 0.2, v_y + 0.5],
      [v_x + 0.8, v_y + 0.2]
    ];
  }
}

// Placeholder rewards matrix
var R = null;

// Placeholder valid positions list
var valid_positions = null;

// Keeps track of states and actions seen so far
// [[x, y, o, v, a], ...]
var sa_seen_so_far = [];

// Placeholder for the vehicle object (class) itself
var user_vehicle = null;

// Placeholder for the drawn vehicle
var drawn_vehicle = null;

// Demonstration continues until the vehicle crashes or reaches the goal
var demonstration_in_progress = false;

// Action codes
// w: 87, 119
// a: 65, 97
// d: 68, 100
// r: 82, 114
// f: 70, 102
var action_codes = {
  87: 0,
  119:0,

  65: 1,
  97: 1,

  68: 2,
  100: 2,

  82: 3,
  114: 3,

  70: 4,
  102: 4
}


// Vehicle actions by key
function vehicle_act(event) {

  // Do nothing if the demonstration has ended
  if (! demonstration_in_progress) {
    return;
  }

  // Removes the current vehicle drawing
  two.remove(drawn_vehicle);

  // Gets the keycode
  let key_code = event.which;

  // Placeholder
  let action_index = action_codes[key_code];

  // If undefined, do nothing
  if (action_index == null) {
    return;
  }

  // Gets the current vehicle conditions
  let p_x = user_vehicle.xloc;
  let p_y = user_vehicle.yloc;
  let p_o = user_vehicle.orientation_index;
  let p_v = user_vehicle.speed;

  // Executes action
  let movement_results = user_vehicle.execute_action(action_index, modify_self=true, get_copy_there=false, get_end_location=true);

  let v_xy = movement_results[1][0];
  let v_x = v_xy[0];
  let v_y = v_xy[1];
  let v_o = movement_results[1][1];
  let v_v = movement_results[1][2];

  // Adds [s, a] as [x, y, o, v, a]
  sa_seen_so_far.push([p_x, p_y, p_o, p_v, action_index]);


  // Draws vehicle in its new position
  let current_local_vehicle_coordinates = generate_vehicle_polygon(v_x, v_y, v_o);

  let vehicle_anchors = [];

  for (let ny = 0; ny < current_local_vehicle_coordinates.length; ny++) {
    let item_xy = generate_TWO_xy(current_local_vehicle_coordinates[ny][0], circuit_xy_minmax[0], current_local_vehicle_coordinates[ny][1], circuit_xy_minmax[1], da_ow, da_oh, y_invert=true);
    vehicle_anchors.push(new Two.Anchor(item_xy[0], item_xy[1]));
  }

  drawn_vehicle = new Two.Path(vehicle_anchors, true, false);

  drawn_vehicle.stroke = "MidnightBlue";
  drawn_vehicle.linewidth = 3;
  drawn_vehicle.fill = "MediumBlue";
  drawn_vehicle.id = "vehicle";
  two.add(drawn_vehicle);

  // Renders the vehicle
  two.update();


  // If the vehicle has crashed or reached the reward, end here
  if (R[v_x][v_y] != (-1)) {

    // End demonstration
    demonstration_in_progress = false;

    // Send data to server
    // TODO
    POST_JSON_return_JSON("/receive_demonstration_data", {"actions taken":sa_seen_so_far, "intent":chosen_intention});

    // Notify the user
    alert("Demonstration has ended and data has been sent to the server");
  }
}