var TAG_ID_DATA_DOCX_CONTENT_PROPERTIES = "data_docx_content_properties"
var TAG_ID_DOCX_CONTENT_PROPERTIES = "docx_content_properties"

var TAG_ID_DATA_UNIQUE_RSIDS = "data_docx_unique_rsids"


// Variable that holds index of stylesheet that describes RSID
var RSID_STYLE_SHEETSHEET_INDEX;

var RSID_CSS_BACKGROUNDCOLOURS;
var RSID_HIDDENS;

var DOCX_CONTENT_PROPERTIES_ARRAY

var rsids;

function init_visualise() {
  get_UNIQUE_RSID_array()

  find_rsid_style_index();
  populate_select();
  add_document_text_listeners();
  record_rsid_css_backgroundcolor();
  get_DOCX_CONTENT_PROPERTIES_ARRAY();
  display_DOCX_CONTENT_PROPERTIES_ARRAY();

  RSID_HIDDENS = Array(document.styleSheets[RSID_STYLE_SHEETSHEET_INDEX].cssRules.length).fill(false);
}


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


/**
 * Finds value of RSID_STYLE_SHEETSHEET_INDEX
 * Required to be called onload
 */
// 
function find_rsid_style_index() {
  for (let x=0; x < document.styleSheets.length; x++) {
    if (document.styleSheets[x].title === "rsid_css") {
      RSID_STYLE_SHEETSHEET_INDEX = x;
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
  let cssRules = document.styleSheets[RSID_STYLE_SHEETSHEET_INDEX].cssRules[rsid_index];
  cssRules.style.backgroundColor = color;
  RSID_CSS_BACKGROUNDCOLOURS[rsid_index] = color;
};

function set_rsid_css_bcolour(rsid_index, rsid_color) {

}

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
        let cssRules = document.styleSheets[RSID_STYLE_SHEETSHEET_INDEX].cssRules[selected_rsid_index];
        let select_colour = document.getElementById("rsid_color");
        select_colour.value = rgb_to_hex(cssRules.style.backgroundColor);
      });

      document_text_rsid[y].addEventListener('dblclick', function() {
        let selected_rsid_index = this.getAttribute("data-rsid_index");
        rsid_toggle_hidden(selected_rsid_index);
        console.log("dblclick");
      });
    }
  }
};

/**
 * Following functions initialises RSID_CSS_BACKGROUNDCOLOUR;
 * it records the intial values within for the RSID stylesheet.
 * 
 * Currently redundant
 */
function record_rsid_css_backgroundcolor () {
  let rsid_cssRules = document.styleSheets[RSID_STYLE_SHEETSHEET_INDEX].cssRules

  RSID_CSS_BACKGROUNDCOLOURS = Array(rsid_cssRules.length);
  for (let index = 0; index < rsid_cssRules.length; index++) {
    RSID_CSS_BACKGROUNDCOLOURS[index] = rsid_cssRules[index].style.backgroundColor;
  }
}

function rsid_toggle_hidden (rsid_index) {

  rsid_tag = rsids[rsid_index]
  rsid_tag = "_".concat(rsid_tag);
  runs = document.getElementsByClassName(rsid_tag);

  // Toggle to hidden
  if (RSID_HIDDENS[rsid_index] == false) {
    RSID_HIDDENS[rsid_index] = true;
    for (let x = 0; x < runs.length; x++) {
      runs[x].classList.add("hidden");
    }
  }
  // Toggle to visible
  else {
    RSID_HIDDENS[rsid_index] = false;
    for (let x = 0; x < runs.length; x++) {
      runs[x].classList.remove("hidden");
    }
  }
}

function selected_rsid_toggle_hidden() {
  let rsid_index = document.getElementById("select_rsid").value;
  rsid_toggle_hidden(rsid_index);
}

function rsid_hide_all() {
  for (let x = 0; x < RSID_HIDDENS.length; x++) {
    if (RSID_HIDDENS[x] == false) {
      rsid_toggle_hidden(x)
    }
  }
}

function rsid_unhide_all() {
  for (let x = 0; x < RSID_HIDDENS.length; x++) {
    if (RSID_HIDDENS[x] == true) {
      rsid_toggle_hidden(x)
    }
  }
}

function get_DOCX_CONTENT_PROPERTIES_ARRAY() {
  let div_tag = document.getElementById(TAG_ID_DATA_DOCX_CONTENT_PROPERTIES);
  if (div_tag != null) {
    DOCX_CONTENT_PROPERTIES_ARRAY = JSON.parse(div_tag.dataset.cont_prop);
  }
}

function display_DOCX_CONTENT_PROPERTIES_ARRAY() {
  let div_prop = document.getElementById(TAG_ID_DOCX_CONTENT_PROPERTIES);
  if (div_prop == null) {
    return;
  }

  // Iterate over each document property
  for (let index = 0; index < DOCX_CONTENT_PROPERTIES_ARRAY.length; index++) {
    let prop = DOCX_CONTENT_PROPERTIES_ARRAY[index];

    // Define name
    let title = document.createElement("h3");
    title.innerHTML = prop.name;

    // Give Iteratre over each property value
    let table = document.createElement("table")

    // 
    for (let key in prop.value_dict) {
      let tr = document.createElement("tr");

      let th = document.createElement("th");
      th.innerHTML = key;

      let td = document.createElement("td");
      td.innerHTML = prop.value_dict[key]

      tr.insertAdjacentElement("beforeend", th);
      tr.insertAdjacentElement("beforeend", td);
      table.insertAdjacentElement("beforeend", tr);
    }
    // Order title - table
    div_prop.insertAdjacentElement('beforeend', title);
    div_prop.insertAdjacentElement('beforeend', table);
    
    
  }
}

function get_UNIQUE_RSID_array() {
  let div_tag = document.getElementById(TAG_ID_DATA_UNIQUE_RSIDS);
  if (div_tag != null) {
    let string = div_tag.dataset.unique_rsids;
    string = string.replaceAll("'", '"')
    rsids = JSON.parse(string);
  }

}

function pdfChangeStyle(){
  document.getElementsByTagName("nav")[0].style.display = "none";
  document.getElementsByTagName("section")[0].classList.remove("grid-container");
  document.getElementsByTagName("section")[1].classList.remove("menu");
  document.getElementById("upload").style.display = "none";
  document.getElementById("colour").style.display = "none";
  document.getElementById("pdf").style.display = "none";
  window.print();
  document.getElementsByTagName("nav")[0].style.display = "block";
  document.getElementsByTagName("section")[0].classList.add("grid-container");
  document.getElementsByTagName("section")[1].classList.add("menu");
  document.getElementById("upload").style.display = "block";
  document.getElementById("colour").style.display = "block";
  document.getElementById("pdf").style.display = "block";
}

function toggleParagraphStructure () {
  let documentText = document.getElementsByClassName("document_text")[0];
  if (documentText.classList.contains("collapse_structure")) {
    documentText.classList.remove("collapse_structure");
  } else {
    documentText.classList.add("collapse_structure");
  }
}

let font_size = 1;
function increase_fontsize () {
  let documentText = document.getElementsByClassName("document_text")[0];
  font_size *=1.1;
  documentText.style.fontSize = font_size.toString().concat("rem");

  paragraphs = documentText.getElementsByClassName("paragraph");
  for (let x = 0; x < paragraphs.length; x++) {
    paragraphs[x].style.margin = font_size.toString().concat("rem 0");
  }
}

function  decrease_fontsize () {
  let documentText = document.getElementsByClassName("document_text")[0];
  font_size /= 1.1;
  documentText.style.fontSize = font_size.toString().concat("rem");

  paragraphs = documentText.getElementsByClassName("paragraph");
  for (let x = 0; x < paragraphs.length; x++) {
    paragraphs[x].style.margin = font_size.toString().concat("rem 0");
  }
}

function reset_fontsize () {
  let documentText = document.getElementsByClassName("document_text")[0];
  font_size = 1;
  documentText.style.fontSize = font_size.toString().concat("rem");

  paragraphs = documentText.getElementsByClassName("paragraph");
  for (let x = 0; x < paragraphs.length; x++) {
    paragraphs[x].style.margin = font_size.toString().concat("rem 0");
  }
}