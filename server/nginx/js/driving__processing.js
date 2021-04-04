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

  console.log(API_result);

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
}