/*
SUMMARY

Necessary functions for driving
*/

//Processes the entire 
async function process_driving_conditions() {

  let c = document.getElementById("circuit_selected");
  let chosen_circuit = c.options[c.selectedIndex].value;

  let v = document.getElementById("vehicle_selected");
  let chosen_vehicle = v.options[v.selectedIndex].value;

  let API_result = await POST_JSON_return_JSON("/retrieve_circuit_vehicle", {"circuit": chosen_circuit, "vehicle":chosen_vehicle});

  // Clears any possible error messages
  clear_div_contents("cv errors");

  let output = API_result["Output"];

  if (output == "Failure") {
    // Show error message
    document.getElementById("cv errors").append(create_error_message("ERROR", API_result["Cause"], "error selecting circuit and/or vehicle"));
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

              {"<>":"b", "text":"D"},
              {"<>":"span", "text":" Turn right"},
              {"<>":"br"},
            ]}
          ]}
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

  let da_ow = driving_area_to_be_drawn.offsetWidth;
  let da_oh = driving_area_to_be_drawn.offsetHeight;

  var driving_area_to_be_drawn_params = { width: da_ow, height: da_oh};
  var two = new Two(driving_area_to_be_drawn_params);
  two.appendTo(driving_area_to_be_drawn);

  // Draws the circuit
  let circuit_points = API_result["circuit"];
  let circuit_anchors = [];
  let circuit_xy_minmax = calculate_xy_minmax(circuit_points);

  for (let nvnv = 0; nvnv < circuit_points.length; nvnv++) {
    let c_xy = generate_TWO_xy(circuit_points[nvnv][0], circuit_xy_minmax[0], circuit_points[nvnv][1], circuit_xy_minmax[1], da_ow, da_oh, y_invert=true);
    circuit_anchors.push(new Two.Anchor(c_xy[0], c_xy[1]));
  }

  var circuit_TWO = new Two.Path(circuit_anchors, true, false);

  circuit_TWO.stroke = "Black";
  circuit_TWO.linewidth = 5;
  circuit_TWO.fill = "Gray";
  circuit_TWO.id = "circuit";
  two.add(circuit_TWO);


  // Draws the vehicle
  let vehicle_points = API_result["vehicle"];
  let vehicle_anchors = [];

  for (let wiwi = 0; wiwi < vehicle_points.length; wiwi++) {
    let v_xy = generate_TWO_xy(vehicle_points[wiwi][0], circuit_xy_minmax[0], vehicle_points[wiwi][1], circuit_xy_minmax[1], da_ow, da_oh, y_invert=true);
    vehicle_anchors.push(new Two.Anchor(v_xy[0], v_xy[1]));
  }

  var vehicle_TWO = new Two.Path(vehicle_anchors, true, false);

  vehicle_TWO.stroke = "SteelBlue";
  vehicle_TWO.linewidth = 3;
  vehicle_TWO.fill = "RoyalBlue";
  vehicle_TWO.id = "vehicle";

  // Adds the vehicle to agroup, so that it is easier to handle
  var v_group = two.makeGroup(vehicle_TWO);


  // Translates the vehicle to its starting position
  let starting_pos = API_result["starting position"];
  let starting_pos_updated = generate_TWO_xy(starting_pos[0][0], circuit_xy_minmax[0], starting_pos[0][1], circuit_xy_minmax[1], da_ow, da_oh, y_invert=false);

  // Moves the vehicle to its starting position, negative y because positive y is moving down
  v_group.translation.set(starting_pos_updated[0], -starting_pos_updated[1]);
  // Rotates it as appropiate
  v_group.rotation += starting_pos[1];


  two.add(v_group);

  // Rendering
  two.update();
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



// Obtains the x min, x max, y min, y max in an array representing a poly line
// Returns the result in the format: [[x min, x max], [y min, y max]]
function calculate_xy_minmax(given_polyline) {

  let xmin = (10)**9;
  let xmax = (-10)**9;
  let ymin = (10)**9;
  let ymax = (-10)**9;

  for (let azaz = 0; azaz < given_polyline.length; azaz++) {

    [xn, yn] = given_polyline[azaz];

    xmin = Math.min(xmin, xn);
    xmax = Math.max(xmax, xn);
    ymin = Math.min(ymin, yn);
    ymax = Math.max(ymax, yn);
  }

  return [[xmin, xmax], [ymin, ymax]];
}