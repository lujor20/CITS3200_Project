const dropzone = document.getElementById('dropzone');
const csvTable = document.getElementById('csvTable');
const filter = document.getElementById('filter');
const clearButton = document.getElementById('clearButton');
const downloadButton = document.getElementById('downloadButton');
const searchBar = document.getElementById('searchBar');
const searchButton = document.getElementById("searchButton");
const resetButton = document.getElementById("resetButton");
const internationalAnalysis = document.getElementById("internationalAnalysis");
const distanceAnalysis = document.getElementById("distanceAnalysis");

// dropzone
dropzone.addEventListener('dragover', function(event) {
    event.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', function(event) {
    event.preventDefault();
    dropzone.classList.remove('dragover');
});

function uploadFile(file, url, onSuccess) {
    const xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            document.getElementById('uploadProgress').innerText = percentComplete.toFixed(1) + '%';
        }
    }, false);
    xhr.addEventListener('load', function() {
        if (xhr.status == 200) {
            const response = JSON.parse(xhr.responseText);
            onSuccess(response);
        } else {
            console.error('Upload failed:', xhr.statusText);
        }
        hideLoader();
    });
    xhr.addEventListener('error', function() {
        console.error('Upload failed.');
        hideLoader();
    });
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'text/csv');

    showLoader();
    xhr.send(file);
}

dropzone.addEventListener('drop', function(event) {
    event.preventDefault();
    dropzone.classList.remove('dragover');

    //Check the number of files
    if(event.dataTransfer.files.length !== 1) {
        alert("please drop only one file");
        return;
    }
    const file = event.dataTransfer.files[0];

    //Check the file type
    const fileType = file.name.split('.').pop().toLowerCase();
    if (fileType !== 'csv') {
        alert('please drop CSV file');
        return;
    }

    showLoader();

    const reader = new FileReader();
    reader.onload = function(event) {
        const contents = event.target.result;

        fetch('/tool2', {
            method: 'POST',
            body: contents
        })
        .then(response => response.json())
        .then(data => {
            hideLoader();
            let tableHTML = '<tr>';

            // Generate table headers
            data.headers.forEach(header => {
                tableHTML += `<th>${header}</th>`;
            });
            tableHTML += '</tr>';

            // Generate table rows
            data.data.forEach(row => {
            tableHTML += '<tr>';
            data.headers.forEach(header => {
                tableHTML += `<td>${row[header]}</td>`;
            });
            tableHTML += '</tr>';
        });
        // Insert the generated table HTML into your page
        document.getElementById('csvTable').innerHTML = tableHTML;

        // Add click event listeners to each table row
        data.data.forEach((row, index) => {
        document.querySelectorAll('#csvTable tr')[index + 1].addEventListener('click', onRowClick);
        });
        });
    };
    reader.readAsText(file);
});   

//international analysis
internationalAnalysis.addEventListener('click', function() {
    fetch('/international_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        let tableHTML = '<tr>';
        // Generate table headers
        data.headers.forEach(header => {
            tableHTML += `<th>${header}</th>`;
        });
        tableHTML += '</tr>';
        
        // Generate table rows
        data.data.forEach(row => {
            tableHTML += '<tr>';
            data.headers.forEach(header => {
                tableHTML += `<td>${row[header]}</td>`;
            });
            tableHTML += '</tr>';
        });

        document.getElementById('csvTable').innerHTML = tableHTML;
    })
    .catch(error => {
        console.error('There was an error with the fetch operation', error);
    });
});

//distance analysis
distanceAnalysis.addEventListener('click', function() {
    fetch('/distance_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        let tableHTML = '<tr>';
        // Generate table headers
        data.headers.forEach(header => {
            tableHTML += `<th>${header}</th>`;
        });
        tableHTML += '</tr>';
        
        // Generate table rows
        data.data.forEach(row => {
            tableHTML += '<tr>';
            data.headers.forEach(header => {
                tableHTML += `<td>${row[header]}</td>`;
            });
            tableHTML += '</tr>';
        });

        document.getElementById('csvTable').innerHTML = tableHTML;
    })
    .catch(error => {
        console.error('There was an error with the fetch operation', error);
    });
});

//filter
var table = document.getElementById("csvTable");
var rows = table.getElementsByTagName("tr");
filter.addEventListener("change", function() {
    console.log("Filter change event triggered");
    var selectedValue = this.value;
    console.log("Selected value is: ", selectedValue);

    showLoader();

    // Ensure that the loader gets shown before filtering begins
    requestAnimationFrame(function() {
        // Start filtering after the loader has been shown
        requestAnimationFrame(function() {
            for (var i = 1; i < rows.length; i++) {
                var locationType = rows[i].getElementsByTagName("td")[6].innerText;

                if (selectedValue === "all" || locationType === selectedValue) {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }
            }
            hideLoader();
            console.log("Exiting filter change handler");
        });
    });
});

//download
downloadButton.addEventListener('click', () => {
    fetch('/download')
        .then(response => response.blob())
        .then(blob => {
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = window.URL.createObjectURL(blob);
            a.download = 'output.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        })
        .catch(e => console.error('Fetch error:', e));
});


//clean button
clearButton.addEventListener('click', function() {
    csvTable.innerHTML = '';
    filter.value = "all";
});

//search bar
searchButton.addEventListener('click', function() {
    showLoader();

    const searchString = String(searchBar.value);
    const table = document.getElementById("csvTable");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) { // i=1 to skip the header row
        const usernameCell = rows[i].getElementsByTagName("td")[0]; // assuming Username is the first column
        const username = String(usernameCell.textContent || usernameCell.innerText);

        if (username.toLowerCase().indexOf(searchString) !== -1) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }

    hideLoader();
});

//resetButton
resetButton.addEventListener('click', function() {
    const table = document.getElementById("csvTable");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = "";  // Show all rows
    }

    searchBar.value = "";  // Clear the searchBar content

    filter.value = "all";
});

//click row
function onRowClick(event) {
    const row = event.currentTarget;
    const id = row.cells[0].textContent;
    const longtitude = row.cells[4].textContent;
    const latitude = row.cells[5].textContent;

    showLoader();

    fetch('/get_user_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': id,
            'longitude': longtitude,
            'latitude': latitude
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoader();
        // data response from the flask
        showDetailsInModal(data);
    })
    .catch(error => {
        hideLoader();
        console.error('Error fetching user details:', error)
    });
}


const modal = document.getElementById('detailsModal');
const closeButton = modal.querySelector('.close-button');

closeButton.addEventListener('click', function() {
    modal.style.display = 'none';
});
window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

function showDetailsInModal(data) {
    //user details
    document.querySelector('.id').textContent = data.id;

    // add map into model
    const mapContainer = document.getElementById('mapContainer');
    mapContainer.innerHTML = '';
    if(data.map_html) {
        mapContainer.innerHTML = data.map_html;
    }

    // display model
    document.getElementById('detailsModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('detailsModal').style.display = 'none';
}

// loader
function showLoader() {
    document.getElementById('loader').classList.remove('hidden');
}

function hideLoader() {
    document.getElementById('loader').classList.add('hidden');
}
