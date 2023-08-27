// incredibly hacky function
// document.styleSheets[1].cssRules[0].style.backgroundColor = 'rgb(0,0,0)'
function _bcolour_rsid(rsid_index, r, g, b) {
  let html_stylesheet_index = 1 // defined second in the HTML, hence index 1.
  let cssRules = document.styleSheets[html_stylesheet_index].cssRules[rsid_index];

  let expected_rsid = rsids[rsid_index];
  let actual_rsid = cssRules.selectorText;
  
  cssRules.style.backgroundColor = "rgb(".concat(r, ",", g, ",", b);

  console.log(expected_rsid.concat("with", actual_rsid))
};

function bcolour_rsid() {
  let color = document.getElementById("rsid_color").value;
  let rsid_index = document.getElementById("select_rsid").value;
  let html_stylesheet_index = 1 // defined second in the HTML, hence index 1.
  let cssRules = document.styleSheets[html_stylesheet_index].cssRules[rsid_index];

  let expected_rsid = rsids[1];
  let actual_rsid = cssRules.selectorText;
  
  cssRules.style.backgroundColor = color;

  console.log(expected_rsid.concat("with", actual_rsid, color))
};

function populate_select() {
  select = document.getElementById("select_rsid");
  console.log(select);
  for (let x=1; x < rsids.length; x++) {
    option = document.createElement("option");
    option.value = x;
    option.innerHTML = rsids[x];
    select.insertAdjacentElement("afterbegin", option);
  }
}

$(document).ready(function() {
  
  function get_rsid() {
    $.ajax({
      type: 'GET',
      url : urlGetRsid,
      dataType: 'json',
      success: function (data) {
        print("chocolate")
      }
    })
  }

});



