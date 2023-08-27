// incredibly hacky function
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
  for (let x=0; x < rsids.length; x++) {
    option = document.createElement("option");
    option.value = x;
    option.innerHTML = rsids[x];
    select.insertAdjacentElement("afterbegin", option);
  }
}




