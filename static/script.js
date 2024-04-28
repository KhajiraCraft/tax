
// Function to open the delete modal
function openDeleteModal() {
    document.getElementById('deleteModal').style.display = 'block';
}

// Function to close the delete modal
function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
}


function deleteRecord(id) {
    if (confirm("Are you sure you want to delete this record?")) {
        fetch('/delete_tax_record?id=' + id, {
            method: 'DELETE'
        })
        .then(response => response.text())
        .then(data => {
            console.log(data); // Log the response from the server
            // Refresh the tax table to reflect the changes
            fetchTaxRecords();
        })
        .catch(error => console.error('Error deleting tax record:', error));
    }
}

        //Function to fetch tax records from the server and populate the tax table
        function fetchTaxRecords() {
            fetch('/get_tax_records')
                .then(response => response.json())
                .then(data => {
                    const taxTableBody = document.getElementById('taxTable').getElementsByTagName('tbody')[0];
                    taxTableBody.innerHTML = ''; // Clear previous rows
                    data.forEach(record => {
                        taxTableBody.innerHTML += '<tr><td>' + record.company + '</td><td>' + record.amount.toFixed(2) + '</td><td>' + record.payment_date + '</td><td>' + record.status + '</td><td>' + record.due_date + '</td><td><a href="#" onclick="openEditModal(' + record.id + ')">Edit</a> | <a href="#" onclick="deleteRecord(' + record.id + ')">Delete</a></td></tr>';
                    });
                })
                .catch(error => console.error('Error fetching tax records:', error));
        }
//OPENEDITMODAL!!
    //     function openEditModal(id) {
    //     // Fetch the tax record with the given ID
    //     fetch('/get_tax_record?id=' + id)
    //         .then(response => response.json())
    //         .then(data => {
    //             const record = data[0]; // Assuming only one record is returned
    //             // Populate the edit form fields with the record details
    //             document.getElementById('editId').value = record.id;
    //             document.getElementById('editCompany').value = record.company;
    //             document.getElementById('editAmount').value = record.amount;
    //             document.getElementById('editPaymentDate').value = record.payment_date;
    //             document.getElementById('editStatus').value = record.status;
    //             document.getElementById('editDueDate').value = record.due_date;
    //             // Display the edit modal
    //             document.getElementById('editModal').style.display = 'block';
    //         })
    //         .catch(error => console.error('Error fetching tax record:', error));
    // }

//NEW CODE FOR TEST START
function openEditModal(id) {
    // Fetch the tax record with the given ID
    fetch('/get_tax_record?id=' + id)
        .then(response => response.json())
        .then(data => {
            const record = data[0]; // Assuming only one record is returned
            // Populate the edit form fields with the record details
            document.getElementById('editId').value = record.id;
            document.getElementById('editCompany').value = record.company;
            document.getElementById('editAmount').value = record.amount;
            document.getElementById('editPaymentDate').value = record.payment_date;
            document.getElementById('editStatus').value = record.status;

            // Dynamically generate due date options
            generateEditDueDateOptions(record.due_date);

            // Display the edit modal
            document.getElementById('editModal').style.display = 'block';
        })
        .catch(error => console.error('Error fetching tax record:', error));
}

// Function to generate due date options dynamically based on the current year
function generateEditDueDateOptions(selectedDueDate) {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();

    const dueDates = [
        { month: 0, day: 15, label: 'January 15' },
        { month: 3, day: 15, label: 'April 15' },
        { month: 5, day: 15, label: 'June 15' },
        { month: 8, day: 15, label: 'September 15' }
    ];

    const editDueDateSelect = document.getElementById('editDueDateSelect');
    if (!editDueDateSelect) {
        console.error('Element with ID "editDueDateSelect" not found.');
        return;
    }
    console.log('Dropdown element found:', editDueDateSelect); // Log the dropdown element
    editDueDateSelect.innerHTML = '';

    dueDates.forEach(dueDate => {
        // Calculate due year based on the current year and month
        let dueYear = currentYear + 1;
        const optionDate = new Date(dueYear, dueDate.month, dueDate.day);
        const optionLabel = dueDate.label + ' ' + dueYear;
        const optionValue = optionDate.toISOString().slice(0, 10);
        console.log('Adding option:', optionLabel); // Log each option being added
        const option = new Option(optionLabel, optionValue);
        if (optionValue === selectedDueDate) {
            option.selected = true;
        }
        editDueDateSelect.add(option);
    });
}
//NEW CODE END LINE



    // Function to close the edit modal
    function closeEditModal() {
        document.getElementById('editModal').style.display = 'none';
    }

    // Function to handle the submission of the edited record
    document.getElementById('editForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/update_tax_record', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            console.log(data); // Log the response from the server
            // Close the edit modal
            closeEditModal();
            // Refresh the tax table to reflect the changes
            fetchTaxRecords();
        })
        .catch(error => console.error('Error updating tax record:', error));
    });
    

    
    // Function to generate due date options dynamically based on the current year
    function generateDueDateOptions() {
        const currentDate = new Date();
        const currentYear = currentDate.getFullYear();

        const dueDates = [
            { month: 0, day: 15, label: 'January 15' },
            { month: 3, day: 15, label: 'April 15' },
            { month: 5, day: 15, label: 'June 15' },
            { month: 8, day: 15, label: 'September 15' }
        ];

        const dueDateSelect = document.getElementById('dueDate');
        if (!dueDateSelect) {
            console.error('Element with ID "dueDate" not found.');
            return;
        }
        console.log('Dropdown element found:', dueDateSelect); // Log the dropdown element
        dueDateSelect.innerHTML = '';

    //     const noneOption = new Option('None Selected', '');
    // dueDateSelect.add(noneOption);
        dueDates.forEach(dueDate => {
            // Calculate due year based on the current year and month
            let dueYear = currentYear + 1;
            const optionDate = new Date(dueYear, dueDate.month, dueDate.day);
            const optionLabel = dueDate.label + ' ' + dueYear;
            const optionValue = optionDate.toISOString().slice(0, 10);
            console.log('Adding option:', optionLabel); // Log each option being added
            const option = new Option(optionLabel, optionValue);
            dueDateSelect.add(option);
        });
    }


// Function to generate summary due date options dynamically based on the current year
function generateSummaryDueDateOptions(selectedDueDate) {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();

    const dueDates = [
        { month: 0, day: 15, label: 'January 15' },
        { month: 3, day: 15, label: 'April 15' },
        { month: 5, day: 15, label: 'June 15' },
        { month: 8, day: 15, label: 'September 15' }
    ];

    const summaryDueDateSelect = document.getElementById('summaryDueDate');
    if (!summaryDueDateSelect) {
        console.error('Element with ID "summaryDueDate" not found.');
        return;
    }
    console.log('Dropdown element found:', summaryDueDateSelect); // Log the dropdown element
    summaryDueDateSelect.innerHTML = '';

    const noneOption = new Option('None', '');
    summaryDueDateSelect.add(noneOption);

    dueDates.forEach(dueDate => {
        // Calculate due year based on the current year and month
        let dueYear = currentYear + 1;
        const optionDate = new Date(dueYear, dueDate.month, dueDate.day);
        const optionLabel = dueDate.label + ' ' + dueYear;
        const optionValue = optionDate.toISOString().slice(0, 10);
        console.log('Adding option:', optionLabel); // Log each option being added
        const option = new Option(optionLabel, optionValue);
        if (optionValue === selectedDueDate) {
            option.selected = true; // Set the option as selected if it matches the selected due date
        }
        summaryDueDateSelect.add(option);
    });
}

// Call the function to generate summary due date options when the page loads
// window.onload = function() {
//     const selectedDueDate = document.getElementById('summaryDueDate').value; // Get the currently selected due date
//     generateSummaryDueDateOptions(selectedDueDate); // Ensure summary due date options are generated initially with the selected due date
//     fetchTaxRecords(); // Ensure tax records are fetched initially
// };



//NEW CODE START
document.getElementById('summaryDueDate').addEventListener('change', updateSummaryTable);

// function updateSummaryTable() {
//     const dueDate = document.getElementById('summaryDueDate').value;
//     console.log(dueDate)
//     fetch('/get_tax_summary_records?due_date=' + dueDate)
//         .then(response => response.json())
//         .then(data => {
//             populateSummaryTable(data);
//         })
//         .catch(error => console.error('Error fetching tax records:', error));
// }

// function populateSummaryTable(records) {
//     const summaryTableBody = document.getElementById('summaryTable').getElementsByTagName('tbody')[0];
//     summaryTableBody.innerHTML = ''; // Clear previous rows

//     let totalAmount = 0;
//     records.forEach(record => {
//         summaryTableBody.innerHTML += '<tr><td>' + record.company + '</td><td>' + record.amount.toFixed(2) + '</td><td>' + record.status + '</td><td>' + record.due_date + '</td></tr>';
//         totalAmount += record.amount;
//     });

//     // Update total amount in the summary table
//     document.getElementById('totalAmount').textContent = totalAmount.toFixed(2);

//     // Update tax due based on tax rate
//     const taxRate = parseFloat(document.getElementById('taxRateField').value);
//     const taxDue = totalAmount * taxRate;
//     document.getElementById('taxDue').textContent = taxDue.toFixed(2);
// }

//NEW CODE END


// Function to update the summary table based on selected due date and tax rate
function updateSummaryTable() {
    const dueDate = document.getElementById('summaryDueDate').value;
    fetch('/get_tax_summary_records?due_date=' + dueDate)
        .then(response => response.json())
        .then(data => {
            populateSummaryTable(data);
        })
        .catch(error => console.error('Error fetching tax records:', error));
}

// Function to populate the summary table with records and calculate tax due based on tax rate
function populateSummaryTable(records) {
    const summaryTableBody = document.getElementById('summaryTable').getElementsByTagName('tbody')[0];
    summaryTableBody.innerHTML = ''; // Clear previous rows

    let totalAmount = 0;
    records.forEach(record => {
        summaryTableBody.innerHTML += '<tr><td>' + record.company + '</td><td>' + record.amount.toFixed(2) + '</td><td>' + record.status + '</td><td>' + record.due_date + '</td></tr>';
        totalAmount += record.amount;
    });

    // Update total amount in the summary table
    document.getElementById('totalAmount').textContent = totalAmount.toFixed(2);

    // Update tax due based on tax rate entered by the user
    const taxRate = parseFloat(document.getElementById('taxRateField').value);
    const taxDue = totalAmount * taxRate;
    document.getElementById('taxDue').textContent = taxDue.toFixed(2);
    document.getElementById('taxRate').textContent = taxRate.toFixed(2)*100 + '%';
}   

// Add event listener to taxRateField to trigger updateSummaryTable() on input change
document.getElementById('taxRateField').addEventListener('input', updateSummaryTable);

// Call updateSummaryTable() initially to ensure it updates the summary table with default tax rate
updateSummaryTable();



    // Call the function to generate due date options when the page loads
    window.onload = function() {
        generateDueDateOptions();
        fetchTaxRecords();
        const selectedDueDate = document.getElementById('summaryDueDate').value; // Get the currently selected due date
        generateSummaryDueDateOptions(selectedDueDate);
        console.log('Due date options generated.');
    };

    function submitForm() {
        // Get form data
        var formData = new FormData(document.getElementById('taxForm'));

        // Send form data asynchronously using AJAX
        fetch('/taxes', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // If the response is successful, display a success message
                alert('Record added successfully.');
                // Optionally, you can reset the form here:
                // document.getElementById('taxForm').reset();
            } else {
                // If there's an error, display an error message
                alert('Error adding record.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding record.');
        });
    }

    document.getElementById("taxForm").addEventListener("submit", function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();
        
        // Perform any necessary form validation here
        
        // Submit the form data asynchronously using fetch or XMLHttpRequest
        fetch('/taxes', {
            method: 'POST',
            body: new FormData(document.getElementById('taxForm'))
        })
        .then(response => {
            if (response.ok) {
                // If the request was successful, redirect to the home page
                window.location.href = '/all';
            } else {
                // Handle errors if needed
                console.error('Failed to save tax data');
            }
        })
        .catch(error => {
            console.error('Error occurred while saving tax data:', error);
        });
    });