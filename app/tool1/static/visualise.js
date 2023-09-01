// Convert "rgb(x, y, z)" to  respective hexvalue "#rrggbb" */
function rgb_to_hex(string) {

  function formatter(string) {
    string = Number(string.replace(/\D/g, "")).toString(16);
    if (string.length < 2) {
      string = "0".concat(string);
    }
    return string;
  }
  let rgb_array = string.split(",")
  
  
  if (rgb_array.length != 3) { // Assume already hex, return
    return string;
  }

  let red = formatter(rgb_array[0]);
  let green = formatter(rgb_array[1]);
  let blue = formatter(rgb_array[2]);

  return "#".concat(red, green, blue);
}



// Variable that holds index of stylesheet that describes RSID
let rsid_style_stylesheet_index;

/**
 * Finds value of rsid_style_stylesheet_index
 * Required to be called onload
 */
// 
function find_rsid_style_index() {
  for (let x=0; x < document.styleSheets.length; x++) {
    if (document.styleSheets[x].title === "rsid_css") {
      rsid_style_stylesheet_index = x;
      break;
    }
  }
};

/**
 * Changes the selected RSID to the select COLOUR
 * References inputs with id "rsid_color" and "select_rsid"
 */
function bcolour_rsid() {
  // Get selected colour and rsid
  let color = document.getElementById("rsid_color").value;
  let rsid_index = document.getElementById("select_rsid").value;

  // Change CSS
  let cssRules = document.styleSheets[rsid_style_stylesheet_index].cssRules[rsid_index];
  cssRules.style.backgroundColor = color;

  // Debug information
  let expected_rsid = rsids[rsid_index];
  let actual_rsid = cssRules.selectorText;
  console.log(expected_rsid.concat("with", actual_rsid, color));
};

/**
 * Function that populates the select tag "select_rsid" with all options.
 * Required to be called onload.
 */
function populate_select() {
  // Get element
  select = document.getElementById("select_rsid");

  // Populate select with options
  for (let x=0; x < rsids.length; x++) {
    option = document.createElement("option");
    option.value = x;
    option.innerHTML = rsids[x];
    select.insertAdjacentElement("afterbegin", option);
  }
};

function select_rsid() {

};
/** Adds event listeners that allows users to select click on text
 * to select it's corresponding RSID
 * Required to be called onload
 */
function add_document_text_listeners() {
  
  // Iterate for each unique RSID
  for (let x=0; x < rsids.length; x++) {
    let rsid = "_".concat(rsids[x]);
    document_text_rsid = document.getElementsByClassName(rsid);

    // Iterate for each object with unique RSID
    for (let y=0; y < document_text_rsid.length; y++) {
      document_text_rsid[y].addEventListener('click', function() {


        let selected_rsid_index = this.getAttribute("data-rsid_index");
        console.log(selected_rsid_index);

        // Change "select_rsid"
        let select_rsid = document.getElementById("select_rsid");
        select_rsid.value = selected_rsid_index;

        // Change "rsid_color"
        let cssRules = document.styleSheets[rsid_style_stylesheet_index].cssRules[selected_rsid_index];
        let select_colour = document.getElementById("rsid_color");
        select_colour.value = rgb_to_hex(cssRules.style.backgroundColor);
      })
    }
  }

};




