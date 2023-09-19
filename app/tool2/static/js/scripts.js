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
    dropzone.style.borderColor = 'blue';
    dropzone.style.backgroundColor = '#b9b6b6';
});

dropzone.addEventListener('dragleave', function(event) {
    event.preventDefault();
    dropzone.style.borderColor = '#a69999';
    dropzone.style.backgroundColor = 'white';
});

dropzone.addEventListener('drop', function(event) {
    event.preventDefault();
    dropzone.style.borderColor = '#a69999';
    dropzone.style.backgroundColor = 'white';

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

    const reader = new FileReader();
    reader.onload = function(event) {
        const contents = event.target.result;

        fetch('/tool2', {
            method: 'POST',
            body: contents
        }).then(response => response.json())
        .then(data => {
            csvTable.innerHTML = '<tr><th>Username</th><th>IP Address</th><th>Country</th><th>Flag</th></tr>';
            data.forEach(row => {
                const newRow = csvTable.insertRow();
                newRow.insertCell().textContent = row['Username'];
                newRow.insertCell().textContent = row['Last Edited by: IP Address'];
                newRow.insertCell().textContent = row['Country'];
                newRow.insertCell().textContent = row['Flag'];
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
    console.log("Selected value is: ", selectedValue);

    for (var i = 1; i < rows.length; i++) {
        var locationType = rows[i].getElementsByTagName("td")[3].innerText;

        if (selectedValue === "all" || locationType === selectedValue) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
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
    csvTable.innerHTML = '<tr><th>Username</th><th>IP Address</th><th>Country</th><th>Flag</th></tr>';
    filter.value = "all";
});
//search bar
searchButton.addEventListener('click', function() {
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
});

resetButton.addEventListener('click', function() {
    const table = document.getElementById("csvTable");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = "";  // Show all rows
    }

    searchBar.value = "";  // Clear the searchBar content
});

// Demo Button
runDemo.addEventListener('click', function() {
    fetch("/tool2/run_demo")  // Assuming you have set up a route called '/run-demo' on Flask to handle this request and return CSV data.
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(response => response.text())
    .then(data => {
        // Update table with CSV data
        updateTableWithCSVData(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function parseCSV(csvText) {
    const rows = csvText.trim().split("\n");
    const headers = rows[0].split(",");
    const data = [];

    for(let i = 1; i < rows.length; i++) {
        const rowData = rows[i].split(",");
        const record = {};
        headers.forEach((header, index) => {
            record[header] = rowData[index];
        });
        data.push(record);
    }
    return data;
}

function updateTableWithCSVData(csvText) {
    const data = parseCSV(csvText);
    const table = document.getElementById("csvTable");

    // Clear old data:
    table.innerHTML = `<tr>
        <th>IP</th>
        <th>Country</th>
        <th>City</th>
        <th>Latitude</th>
        <th>Longitude</th>
        <th>Flag</th>
    </tr>`;

    // Append new data to the table:
    data.forEach(row => {
        const tr = document.createElement("tr");

        Object.values(row).forEach(cellData => {
            const td = document.createElement("td");
            td.innerText = cellData;
            tr.appendChild(td);
        });

        table.appendChild(tr);
    });
}


//click row
function onRowClick(event) {
    const row = event.currentTarget;
    const username = row.cells[0].textContent;
    const ip = row.cells[1].textContent;

    fetch('/tool2/get_user_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'Username': username,
            'Last Edited by: IP Address': ip
        })
    })
    .then(response => response.json())
    .then(data => {
        // data response from the flask
        showDetailsInModal(data);
    })
    .catch(error => console.error('Error fetching user details:', error));
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
    document.querySelector('.ip').textContent = data['Last Edited by: IP Address'];
    document.querySelector('.latitude').textContent = data.Latitude;
    document.querySelector('.longitude').textContent = data.Longitude;

    // add map into model
    if(data.map_html) {
        document.getElementById('mapContainer').innerHTML = data.map_html;
    }

    // display model
    document.getElementById('detailsModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('detailsModal').style.display = 'none';
}






