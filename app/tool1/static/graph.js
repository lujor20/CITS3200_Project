let TAG_ID_CHAR_PER_UNIQUE_RSID = "char_per_unique_rsid"
let CHAR_PER_UNIQUE_RSID // Array of array, each item correspond to docx
let GRAPH_CHAR_PER_UNIQUE_RSID = "graph1"
let TAG_ID_CHAR_PER_RUN = "char_per_run"
let CHAR_PER_RUN
let GRAPH_CHAR_PER_RUN = "graph2"


function init_graph() {
  get_char_per_unique_rsid()
  get_char_per_run()
  show_char_per_unique_rsid()
  show_char_per_run()
}

function get_char_per_unique_rsid() {
  let div_tag = document.getElementById(TAG_ID_CHAR_PER_UNIQUE_RSID);
  if (div_tag != null) {
    let string = div_tag.dataset.data;
    string = string.replaceAll("'", '"')
    CHAR_PER_UNIQUE_RSID = JSON.parse(string);
  }

}
function get_char_per_run() {
  let div_tag = document.getElementById(TAG_ID_CHAR_PER_RUN);
  if (div_tag != null) {
    let string = div_tag.dataset.data;
    string = string.replaceAll("'", '"')
    CHAR_PER_RUN = JSON.parse(string);
  }
}


function show_char_per_unique_rsid() {
  let div_tag = document.getElementById(GRAPH_CHAR_PER_UNIQUE_RSID)
  if (div_tag != null) {
    let data = []
    for (let docx in CHAR_PER_UNIQUE_RSID) {
      let char_per_unique_rsid = CHAR_PER_UNIQUE_RSID[docx]
      let histogram = {
        x : char_per_unique_rsid,
        type : "histogram",
        name : docx
      }
      data.push(histogram)
    }

    if (data.length != 0) {
      let layout = {
        barmode: "stack",
        title : "Characters per Run Unique RSID in a .docx",
        xaxis : {
          title : {
            text : "Characters per RSID"
          }
            
        },
        yaxis : {
          title : {
            text : "Count"
          }
        }
      }
      Plotly.newPlot(GRAPH_CHAR_PER_UNIQUE_RSID, data, layout);
    }
  }
}

function show_char_per_run() {
  let div_tag = document.getElementById(GRAPH_CHAR_PER_RUN)
  if (div_tag != null) {
    let data = []
    for (let docx in CHAR_PER_RUN) {
      let char_per_unique_run = CHAR_PER_RUN[docx]
      let histogram = {
        x : char_per_unique_run,
        type : "histogram",
        name : docx
      }
      data.push(histogram)
    }
    if (data.length != 0) {
      let layout = {
        barmode: "stack",
        title : "Characters per Run Histogram",
        xaxis : {
          title : {
            text : "Character per Run"
          }
        },
        yaxis : {
          title : {
            text : "Count"
          }
        }
      }
      Plotly.newPlot(GRAPH_CHAR_PER_RUN, data, layout);
    }
  }

}