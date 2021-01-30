/*
BASICS

Updates the background in the middle div so that everything is balanced.
Updates the central boxes' size
Only useful for the sign-up and login pages.
*/



// Updates the size of the middle div so that entire page is occupied
function resize_middle_div() {
  // Obtains the total window height
  let total_window_height = window.innerHeight;

  // Gets the navbar and footer's heights
  let navbar_height = document.getElementById("navbar element").offsetHeight;
  let footer_height = document.getElementById("standard footer").offsetHeight;

  // 0 size if already occupying the entire page
  let min_necessary_middle_height = Math.max(total_window_height - navbar_height - footer_height, 0);

  let current_middle_height = document.getElementById("middle div").offsetHeight;

  // Only act if the size of the middle div is smaller than the window's height
  if (current_middle_height < min_necessary_middle_height) {
    document.getElementById("middle div").style.height = min_necessary_middle_height.toString() + "px";
  }
}


// Resizes the central box so that it is always 10% wider than the form within
function resize_central_box() {

  let central_box_width = document.getElementById("central_box").offsetWidth;
  let central_form_width = document.getElementById("central_form").offsetWidth;

  if ((1.1*central_form_width) > central_form_width) {
    central_box_width = 1.1*central_form_width;
    document.getElementById("central_box").style.width = central_box_width.toString() + "px";
  }
}


function resize_appropriately() {
  resize_middle_div();
  resize_central_box();
}

// Executes immediately upon loading
window.onload = resize_appropriately();