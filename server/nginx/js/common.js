/*
BASICS

Common functions.
*/


// Ensures that a string has a size between 2 integers
// a <= str < b
function ensure_str_size(given_str, a, b) {
  let l_str = given_str.length;
  return (a <= l_str) && (l_str < b);
}



// Updates a button's class into disallowed_button
// It also makes the button disabled
function mark_button_as_disallowed(button_id) {

  // Disables the actual button
  document.getElementById(button_id).disabled = "disabled";

  // Changes its class so that it looks accurate
  document.getElementById(button_id).className = "disallowed_button";
}



// Deletes all the contents within a div
// It does NOT delete the div itself
function clear_div_contents(element_ID) {
  document.getElementById(element_ID).innerHTML = "";
}



// Replaces the html content of an element by ID (div or otherwise by a new content)
// content_new (str)
function replace_element_HTML_contents(element_ID, content_new) {
  document.getElementById(element_ID).innerHTML = content_new;
}


// Creates an error message
// It always has the structure:
// TITLE (centered)
// Paragraph
function create_error_message(error_title, error_explained, given_id) {
  let div_containing_error = document.createElement("div");
  div_containing_error.className = "error_message";

  let error_title_p = document.createElement("p");
  let error_title_b = document.createElement("b");
  error_title_b.innerHTML = error_title;

  let error_message_div = document.createElement("div");
  let error_message_p = document.createElement("p");
  error_message_p.innerHTML = error_explained;
  error_message_p.className = "center-x";

  error_title_p.append(error_title_b);
  error_title_p.className = "center-x";
  div_containing_error.append(error_title_p);

  error_message_div.append(error_message_p);
  div_containing_error.append(error_message_div);

  div_containing_error.setAttribute("id", given_id);

  return div_containing_error;
}



// Creates a success message
// It always has the structure:
// TITLE (centered)
// Paragraph
function create_success_message(success_title, success_explained, given_id) {
  let div_containing_error = document.createElement("div");
  div_containing_error.className = "success_message";

  let error_title_p = document.createElement("p");
  let error_title_b = document.createElement("b");
  error_title_b.innerHTML = success_title;

  let error_message_div = document.createElement("div");
  let error_message_p = document.createElement("p");
  error_message_p.innerHTML = success_explained;
  error_message_p.className = "center-x";

  error_title_p.append(error_title_b);
  error_title_p.className = "center-x";
  div_containing_error.append(error_title_p);

  error_message_div.append(error_message_p);
  div_containing_error.append(error_message_div);

  div_containing_error.setAttribute("id", given_id);

  return div_containing_error;
}



// Creates a new line: <br>
function create_br() {
  return document.createElement("br");;
}



// Creates a new horizontal tag: <hr>
// Creates a new line: <br>
function create_hr() {
  return document.createElement("hr");;
}



// Increases the height of a certain div by a given number of pixels
// If the resulting height becomes negative afterwards, it simply reduces its height to zero
function increase_div_height_in_pixels(div_id_to_be_increased, px_to_add) {
  let current_height = document.getElementById(div_id_to_be_increased).offsetHeight;
  let updated_height = Math.max(0, Math.ceil(current_height + px_to_add));
  document.getElementById(div_id_to_be_increased).style.height = updated_height.toString() + "px";
}



// Changes the src of an img depending on a boolean value
// The src is only changed if different to its current value
function change_img_src_based_on_boolean(given_boolean, img_id, true_src, false_src) {

  let current_src = document.getElementById(img_id).src;
  let expected_src = "";

  if (given_boolean) {
    expected_src = true_src;
  } else {
    expected_src = false_src;
  }

  if (current_src != expected_src) {
    document.getElementById(img_id).src = expected_src;
  }
}



// POST JSON to a certain URL and returns the JSON output
// All JSON contents will be objects
// given_url (str)
async function POST_JSON_return_JSON(given_url, to_be_posted) {

  const POST_request = await fetch(given_url, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(to_be_posted)
  });

  const result = await POST_request.json();
  return result;
}



// Gets JSON from a GET requests to a certain URL
async function GET_JSON(given_url) {
  const GET_request = await fetch(given_url, {
      method: "GET",
  });

  const result = await GET_request.json();
  return result;
}


// Replaces the username
async function replace_profile_by_username() {
  let user_session_info = await GET_JSON("/user_info");
  replace_element_HTML_contents("profile a", user_session_info["username"]);
}