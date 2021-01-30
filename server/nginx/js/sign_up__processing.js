/*
BASICS

Processes the sign-up form to create a new user.
*/



// Checks that the username and password have [3, 30) length
function helper_username_password_length() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  return ensure_str_size(username, 3, 30) && ensure_str_size(password, 3, 30);
}



// Updates the username and password table img as needed
function check_username_password() {
  change_img_src_based_on_boolean(helper_username_password_length(), "img username, password length", "/images/good.svg", "/images/bad.svg");
}



// Checks that the password and the repeated password are the same
function helper_repeated_password() {
  let original_password = document.getElementById("password").value;
  let repeated_password = document.getElementById("repeated password").value;
  return original_password == repeated_password;
}



// Updates the repeated password img
function check_repeated_password() {
  change_img_src_based_on_boolean(helper_repeated_password(), "img repeated password", "/images/good.svg", "/images/bad.svg");
}



// Checks that the terms and conditions box is checked
function helper_agreed_to_TOS() {
  return document.getElementById("agreed_to_TOS").checked;
}



// Updates the agreed to TOS img
function check_agreed_to_TOS() {
  change_img_src_based_on_boolean(helper_agreed_to_TOS(), "img agreed to TOS", "/images/good.svg", "/images/bad.svg");
}


// Attempts to sign up
async function attempt__sign_up() {

  // Ensures that all requirements are met
  if (! (helper_username_password_length() && helper_repeated_password() && helper_agreed_to_TOS())) {
    return;
  }


  // Get data
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let agreed_to_TOS = "agreed";

  let API_result = await POST_JSON_return_JSON("/sign_up_action", {"username": username, "password": password, "agreed to TOS": "yes"});
  console.log(API_result);


  // Clears any possible error messages
  clear_div_contents("go to login");

  let output = API_result["Output"];

  if (output == "Failure") {
    // Show error message
    document.getElementById("go to login").append(create_error_message("ERROR", API_result["Cause"], "error: username exists"));
    return;
  }

  // Show a success message
  document.getElementById("go to login").append(create_success_message("SUCCESS", "User has been created, login to enter.", "error: username exists"));

  // The attempt has been successful, disallow button
  mark_button_as_disallowed("sign-up button");
}