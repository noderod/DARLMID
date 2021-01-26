/*
BASICS

Updates the picture size so that it always fills the remaining of the page
Only useful for /404.html.
*/

function resize_appropriately() {
  // Obtains the total window height
  let total_window_height = window.innerHeight;

  // Gets the navbar and footer's heights
  let navbar_height = document.getElementById("navbar element").offsetHeight;
  let message_404_height = document.getElementById("404_message").offsetHeight;
  let footer_height = document.getElementById("standard footer").offsetHeight;

  // 0 size if already occupying the entire page
  let picture_height = Math.max(total_window_height - navbar_height - message_404_height - footer_height, 0);

  // Sets the height of the picture
  document.getElementById("404_img").style.height = picture_height.toString() + "px";
}

// Executes immediately upon loading
window.onload = resize_appropriately();