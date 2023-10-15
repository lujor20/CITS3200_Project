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
const modal = document.getElementById('detailsModal');
const closeButton = modal.querySelector('.close-button');

// loader
function showLoader() {
    document.getElementById('loader').classList.remove('hidden');
}

function hideLoader() {
    document.getElementById('loader').classList.add('hidden');
}

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

    // Check the number of files
    if(event.dataTransfer.files.length !== 1) {
        alert("please drop only one file");
        return;
    }
    const file = event.dataTransfer.files[0];

    // Check the file type
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
            // generate header
            let headerHTML = '<tr>';
            data.headers.forEach(header => {
                headerHTML += `<th>${header}</th>`;
            });
            headerHTML += '</tr>';
            document.querySelector('#csvTable thead').innerHTML = headerHTML;
            
            
            // generate table rows
            let tableHTML = '';
            data.data.forEach(row => {
                let flagClass = '';

                if (row.flag === 'international') {
                    flagClass = 'international-flag';
                } else if (row.flag === 'suspicious') {
                    flagClass = 'suspicious-flag';
                } else if (row.flag === 'domestic') {
                    flagClass = 'domestic-flag';
                }

                tableHTML += `<tr class="${flagClass}">`;
            // add class for css
            data.headers.forEach(header => {
                let tdClass = '';

                if (header === 'flag') {
                    tdClass = 'flag-cell';
                }
                tableHTML += `<td class="${tdClass}">${row[header]}</td>`;
            });
                tableHTML += '</tr>';
            });
            document.querySelector('#csvTable tbody').innerHTML = tableHTML;

            // add event listeners of click rows
            data.data.forEach((row, index) => {
                document.querySelectorAll('#csvTable tbody tr')[index].addEventListener('click', onRowClick);
            });
        })
        .catch(err => {
            console.error('Error:', err);
            hideLoader();
            alert('An error occurred while processing the CSV file.');
        });
    };
    reader.readAsText(file);
});


//international analysis
internationalAnalysis.addEventListener('click', function() {

    filter.style.display = 'none'

    fetch('/international_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        // generate header
        let headerHTML = '<tr>';
        data.headers.forEach(header => {
            headerHTML += `<th>${header}</th>`;
        });
        headerHTML += '</tr>';
        document.querySelector('#csvTable thead').innerHTML = headerHTML;

        let tableHTML = '';
        // generate table rows
        data.data.forEach(row => {
            let flagClass = '';

            if (row.flag === 'low risk code') {
                flagClass = 'low-risk-code';
            } else if (row.flag === 'high risk code') {
                flagClass = 'high-risk-code';
            }

            tableHTML += `<tr class="${flagClass}">`;
            // class for css
            data.headers.forEach(header => {
                let tdClass = '';
                if (header === 'flag') {
                    tdClass = 'risk-cell-internationl';
                }
                tableHTML += `<td class="${tdClass}">${row[header]}</td>`;
            });
                tableHTML += '</tr>';
            });

        document.querySelector('#csvTable tbody').innerHTML = tableHTML;


        data.data.forEach((row, index) => {
            document.querySelectorAll('#csvTable tbody tr')[index].addEventListener('click', onRowClick);
        });
    })
    .catch(error => {
        console.error('There was an error with the fetch operation', error);
    });
});

//distance analysis
distanceAnalysis.addEventListener('click', function() {
    // hide filter
    filter.style.display = 'none'

    fetch('/distance_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        let headerHTML = '<tr>';

        data.headers.forEach(header => {
            headerHTML += `<th>${header}</th>`;
        });
        headerHTML += '</tr>';
        document.querySelector('#csvTable thead').innerHTML = headerHTML;

        // Generate table rows
        let tableHTML = '';
        data.data.forEach(row => {
            let flagClass = '';

            if (row.flag === 'medium risk') {
                flagClass = 'medium-risk';
            } else if (row.flag === 'high risk') {
                flagClass = 'high-risk';
            } else if (row.flag === 'low risk') {
                flagClass = 'low-risk';
            }

            tableHTML += `<tr class="${flagClass}">`;

        data.headers.forEach(header => {
            let tdClass = '';
            if (header === 'flag') {
                tdClass = 'risk-cell';
            }
            tableHTML += `<td class="${tdClass}">${row[header]}</td>`;
        });
            tableHTML += '</tr>';
        });

        document.querySelector('#csvTable tbody').innerHTML = tableHTML;
        data.data.forEach((row, index) => {
            document.querySelectorAll('#csvTable tr')[index + 1].addEventListener('click', onRowClick);
        });
    })
    .catch(error => {
        console.error('There was an error with the fetch operation', error);
    });
});

//filter
var table = document.getElementById("csvTable");
var rows = table.getElementsByTagName("tr");
filter.addEventListener("change", function() {
    var selectedValue = this.value;

    showLoader();

    let rows = document.querySelectorAll('#csvTable tbody tr');
    rows.forEach(row => {
        if (selectedValue === "all" || row.classList.contains(selectedValue + '-flag')) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
    hideLoader();
});


//download output.csv
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

    for (let i = 1; i < rows.length; i++) { // skip the header row
        const usernameCell = rows[i].getElementsByTagName("td")[0];
        const username = String(usernameCell.textContent || usernameCell.innerText);

        if (username.toLowerCase().indexOf(searchString) !== -1) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }

    hideLoader();
});

//click row
function onRowClick(event) {
    const row = event.currentTarget;
    // get coordinates
    const latitude1 = row.cells[4].textContent; 
    const longitude1 = row.cells[5].textContent; 
    const latitude2 = row.cells[9]?.textContent || null; 
    const longitude2 = row.cells[10]?.textContent || null; 

    const coordinates = [{'latitude': latitude1, 'longitude': longitude1}];
    if (latitude2 && longitude2) {
        coordinates.push({'latitude': latitude2, 'longitude': longitude2});
    }

    fetch('/get_user_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'coordinates': coordinates
        })
    })
    .then(response => response.json())
    .then(data => {
        // add map 
        const mapContainer = document.getElementById('mapContainer');
        mapContainer.innerHTML = data.map_html || '';

        // display the entire row data in the modal
        showDetailsInModal(row);
    })
    .catch(error => {
        console.error('Error fetching user details:', error)
    });
}

closeButton.addEventListener('click', function() {
    modal.style.display = 'none';
});
window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
// add data to model
function showDetailsInModal(row) {
    const headers = document.querySelectorAll('table thead th'); 
    const detailContainer = document.getElementById('userDataContainer');
    detailContainer.innerHTML = ''; 

    for (let i = 0; i < row.cells.length; i++) {
        const para = document.createElement('p');
        const headerText = headers[i].textContent.toUpperCase();
        para.innerHTML = `<strong>${headerText}</strong>: ${row.cells[i].textContent}`;
        detailContainer.appendChild(para);
    }

    // display model
    document.getElementById('detailsModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('detailsModal').style.display = 'none';
}

