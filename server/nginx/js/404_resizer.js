/*
SUMMARY

Updates the picture size so that it always fills the remaining of the page
Only useful for /404.html.
*/


// Creates the navbar
async function generate_navbar() {

  // Obtains the user information
  let user_session_info = await GET_JSON("/user_info");
  let navbar_json = {};

  if (jQuery.isEmptyObject(user_session_info)) {
    console.log("Unlogged");
    // Logged out user
    navbar_json = {"html":[
                        {"<>":"a", "class":"logo_element center-y", "href":"/", "html":[
                          {"<>":"img", "alt":"logo", 'src':"/images/DARLMID_icon.png", "class":"logo_element center-y", "height":"100%"}
                        ]},
                        {"<>":"div", "class":"navbar_empty_element"},
                        {"<>":"a", "class":"element center-xy", "href":"/", "text":"Home"},
                        {"<>":"a", "class":"element center-xy", "href":"/about_us", "text":"About Us"},
                        {"<>":"a", "class":"element center-xy", "href":"/documentation", "text":"Documentation"},
                        {"<>":"a", "class":"element center-xy login", "href":"/login", "text":"Login"},
                        {"<>":"a", "class":"element center-xy signup", "href":"/sign_up", "text":"Sign-Up"}
                      ]};
  } else {
    navbar_json = {"html":[
                        {"<>":"a", "class":"logo_element center-y", "href":"/", "html":[
                          {"<>":"img", "alt":"logo", 'src':"/images/DARLMID_icon.png", "class":"logo_element center-y", "height":"100%"}
                        ]},
                        {"<>":"div", "class":"navbar_empty_element"},
                        {"<>":"a", "class":"element center-xy", "href":"/", "text":"Home"},
                        {"<>":"a", "class":"element center-xy", "href":"/about_us", "text":"About Us"},
                        {"<>":"a", "class":"element center-xy", "href":"/documentation", "text":"Documentation"},
                        {"<>":"a", "class":"element center-xy login", "href":"/profile", "text":user_session_info["username"], "id":"profile a"},
                        {"<>":"a", "class":"element center-xy logout", "href":"/logout", "text":"Logout"}
                      ]};

  }

  // Add each content within navbar JSON after being transformed into HTML
  let navbar_contents = "";
  let actual_html = navbar_json["html"];
  for (let html_item_JSON_index in actual_html) {
    navbar_contents += json2html.transform({}, actual_html[html_item_JSON_index]);
  }

  replace_element_HTML_contents("navbar item", navbar_contents);
}


// Resizes the picture
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


// Summarized both functions into one
async function startup_generation() {
  await generate_navbar();
  resize_appropriately();
}