const CSS_DROPZONE_HOVER = "dropzone_hover"

document.addEventListener('DOMContentLoaded', function() {
  init_fileupload();
}, false);

function init_fileupload () {
  const dropzone = document.getElementById("dropzone");
  const file_input = document.getElementById("file");

  dropzone.addEventListener('dragover', function(event) {
    event.preventDefault();
    dropzone.classList.add("dropzone_hover");

  });

  dropzone.addEventListener('dragleave', function(event) {
    event.preventDefault();
    dropzone.classList.remove("dropzone_hover");
  });

  dropzone.addEventListener('drop', function(event) {
    event.preventDefault();
    dropzone.classList.remove("dropzone_hover");


    let file = event.dataTransfer.files[0];

    let reader = new FileReader();
    reader.onload = function (e) {
      let container = new DataTransfer();
      container.items.add(file);

      file_input.files = container.files;
    }
    reader.onerror = function (e) {
      alert("Please don't place folders here!")
    }

    reader.readAsArrayBuffer(file);

  })
}

// https://stackoverflow.com/a/8857445

