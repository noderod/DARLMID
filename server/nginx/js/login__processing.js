/*
BASICS

Processes the login.
*/

// Attempts to login
async function attempt__login() {

  // Get data
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  let API_result = await POST_JSON_return_JSON("/login_action", {"username": username, "password": password});

  // Clears any possible error messages
  clear_div_contents("login errors");

  let output = API_result["Output"];

  if (output == "Failure") {
    // Show error message
    document.getElementById("login errors").append(create_error_message("ERROR", API_result["Cause"], "error: login error"));
    return;
  }

  // Redirect to /
  window.location.href = "/";
}