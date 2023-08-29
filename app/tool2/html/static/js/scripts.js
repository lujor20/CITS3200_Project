const dropzone = document.getElementById('dropzone');
const csvTable = document.getElementById('csvTable');
const clearButton = document.getElementById('clearButton');
const downloadButton = document.getElementById('downloadButton');

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

        fetch('/', {
            method: 'POST',
            body: contents
        }).then(response => response.json())
        .then(data => {
            csvTable.innerHTML = '<tr><th>IP Address</th><th>Username</th><th>Country</th></tr>';
            data.forEach(row => {
                const newRow = csvTable.insertRow();
                newRow.insertCell().textContent = row['Last Edited by: IP Address'];
                newRow.insertCell().textContent = row['Username'];
                newRow.insertCell().textContent = row['Country'];
            });
        });
    };
    reader.readAsText(file);
});

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
    csvTable.innerHTML = '<tr><th>IP Address</th><th>Username</th><th>Country</th></tr>';
});
