const dropzone = document.getElementById('dropzone');
const csvTable = document.getElementById('csvTable');
const filter = document.getElementById('filter');
const clearButton = document.getElementById('clearButton');
const downloadButton = document.getElementById('downloadButton');
const searchBar = document.getElementById('searchBar');
const searchButton = document.getElementById("searchButton");
const resetButton = document.getElementById("resetButton");

// dropzone
dropzone.addEventListener('dragover', function(event) {
    event.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', function(event) {
    event.preventDefault();
    dropzone.classList.remove('dragover');
});

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
        }).then(response => response.json())
        .then(data => {

            hideLoader();

            csvTable.innerHTML = '<tr><th>Username</th><th>IP Address 1</th><th>IP Address 2</th><th>Country(last attempt)</th><th>Flag</th></tr>';
            data.forEach(row => {
                const newRow = csvTable.insertRow();
                newRow.insertCell().textContent = row['Username'];
                newRow.insertCell().textContent = row['IPAddress1'];
                newRow.insertCell().textContent = row['IPAddress2'];
                newRow.insertCell().textContent = row['Country'];

                const flagCell = newRow.insertCell();
                flagCell.textContent = row['Flag'];
                flagCell.classList.add('flag-cell');
                if (row['Flag'] === 'INTERNATIONAL') {
                    newRow.classList.add('international-flag');
                } else if (row['Flag'] === 'SUSPICIOUS') {
                    newRow.classList.add('suspicious-flag');
                } else {
                    newRow.classList.add('domestic-flag');
                }

                newRow.addEventListener('click', onRowClick);
            });
        });
    };
    reader.readAsText(file);
});

//filter
var table = document.getElementById("csvTable");
var rows = table.getElementsByTagName("tr");
filter.addEventListener("change", function() {
    console.log("Filter change event triggered");
    var selectedValue = this.value;
    showLoader();
    console.log("Selected value is: ", selectedValue);

    for (var i = 1; i < rows.length; i++) {
        var locationType = rows[i].getElementsByTagName("td")[4].innerText;

        if (selectedValue === "all" || locationType === selectedValue) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
    hideLoader();
    console.log("Exiting filter change handler");  
}); 

//download
downloadButton.addEventListener('click', function() {
    const csvData = tableToCSV(csvTable);
    downloadCSV(csvData, 'data.csv');
});

function tableToCSV(table) {
    const rows = Array.from(table.querySelectorAll('tr'));
    let csvContent = '';

    rows.forEach(row => {
        const rowData = Array.from(row.querySelectorAll('td, th')).map(cell => '"' + cell.textContent.replace(/"/g, '""') + '"');
        csvContent += rowData.join(',') + '\n';
    });

    return csvContent;
}

function downloadCSV(csvContent, filename) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);

    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = 'hidden';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

clearButton.addEventListener('click', function() {
    csvTable.innerHTML = '<tr><th>Username</th><th>IP Address 1</th><th>IP Address 2</th><th>Country(last attempt)</th><th>Flag</th></tr>';
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
});

//click row
function onRowClick(event) {
    const row = event.currentTarget;
    const username = row.cells[0].textContent;
    const ip1 = row.cells[1].textContent;
    const ip2 = row.cells[2].textContent;

    showLoader();

    fetch('/get_user_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'Username': username,
            'IP Address 1': ip1,
            'IP Address 2': ip2
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
    document.querySelector('.username').textContent = data.Username;

    // Details for IP1
    document.querySelector('.ip1').textContent = data['IP Address 1'];
    document.querySelector('.country1').textContent = data.Country1; 
    document.querySelector('.city1').textContent = data.City1
    document.querySelector('.latitude1').textContent = data.Latitude1;
    document.querySelector('.longitude1').textContent = data.Longitude1;


    // Details for IP2
    document.querySelector('.ip2').textContent = data['IP Address 2'] || 'None';
    document.querySelector('.country2').textContent = data.Country2 || 'None';
    document.querySelector('.city2').textContent = data.City2 || 'None';
    document.querySelector('.latitude2').textContent = data.Latitude2 || 'None';
    document.querySelector('.longitude2').textContent = data.Longitude2 || 'None';

    document.querySelector('.distance').textContent = data.distance;
    document.querySelector('.risk').textContent = data.risk;


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
