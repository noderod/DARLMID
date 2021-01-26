/*
BASICS

Updates the background in the middle div so that everything is balanced.
Only useful for the sign-up and login pages.
*/

function resize_appropriately() {
  // Obtains the total window height
  var total_window_height = window.innerHeight;

  // Gets the navbar and footer's heights
  var navbar_height = document.getElementById("navbar element").offsetHeight;
  var footer_height = document.getElementById("standard footer").offsetHeight;

  // 0 size if already occupying the entire page
  var middle_height = Math.max(total_window_height - navbar_height - footer_height, 0);

  // Sets the height of the middle div
  document.getElementById("middle div").style.height = middle_height.toString() + "px";
}

// Executes immediately upon loading
window.onload = resize_appropriately();