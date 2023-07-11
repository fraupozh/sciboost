let userChoiceRecords; // Declare the global variable
const recordDetailsContainer = document.createElement('div'); // Create the record details container

document.addEventListener('DOMContentLoaded', function() {
  // Retrieve the savedDrugs array from localStorage
  const savedDrugsFromStorage = localStorage.getItem('savedDrugs');
  const savedDrugs = savedDrugsFromStorage ? JSON.parse(savedDrugsFromStorage) : [];

  // Use the retrieved savedDrugs array in your code
  console.log('Retrieved savedDrugs:', savedDrugs);

  // Fetch the JSON data from localStorage
  fetch('/download_json/')
    .then(response => response.json())
    .then(records => {
      // Create a new JSON file and save the records for the drugs in savedDrugs array
      userChoiceRecords = records.filter(record => {
        const drugs = record.drug_entities.replace(/[\[\]']+/g, '').split(', ');
        return drugs.some(drug => savedDrugs.includes(drug));
      });

      // Convert userChoiceRecords to JSON string
      const userChoiceJson = JSON.stringify(userChoiceRecords);

      // Store the JSON string in localStorage for later access
      localStorage.setItem('userChoiceData', userChoiceJson);

      // Process the user choice data
      processUserChoiceData(userChoiceRecords, savedDrugs);
    })
    .catch(error => console.error('Error:', error));
});

function processUserChoiceData(records, savedDrugs) {
  const uniqueDrugs = new Set();
  const uniqueSideEffects = new Set();
  const matchingRecordIds = [];

  // Extract unique drugs and side effects
  records.forEach(record => {
    const drugs = record.drug_entities.replace(/[\[\]']+/g, '').split(', ');
    const sideEffects = record.ade_normalized.replace(/[\[\]']+/g, '').split(', ');

    drugs.forEach(drug => uniqueDrugs.add(drug));
    sideEffects.forEach(sideEffect => uniqueSideEffects.add(sideEffect));
  });

  // Convert sets to arrays
  const drugsArray = Array.from(uniqueDrugs);
  const sideEffectsArray = Array.from(uniqueSideEffects);
  console.log('Unique drugs:', drugsArray);
  console.log('Unique side effects:', sideEffectsArray);

  // Generate the matching record IDs
  drugsArray.forEach(drug => {
    sideEffectsArray.forEach(sideEffect => {
      const matchedRecords = records.filter(record => {
        const drugs = record.drug_entities.replace(/[\[\]']+/g, '').split(', ');
        const sideEffects = record.ade_normalized.replace(/[\[\]']+/g, '').split(', ');

        return drugs.includes(drug) && sideEffects.includes(sideEffect);
      });

      if (matchedRecords.length > 0) {
        matchingRecordIds.push({
          drug,
          sideEffect,
          recordIds: matchedRecords.map(record => record.record_id)
        });
      }
    });
  });
  console.log(matchingRecordIds);

  // Generate the table HTML
  const tableContainer = document.createElement('div');
  tableContainer.id = 'tableContainer';

  // Generate the table
  const table = generateTable(drugsArray, sideEffectsArray, matchingRecordIds, savedDrugs, userChoiceRecords);
  tableContainer.appendChild(table);

  // Append the table container and record details container to the document body
  document.body.appendChild(tableContainer);
  document.body.appendChild(recordDetailsContainer);
}

function generateTable(drugsArray, sideEffectsArray, matchingRecordIds, savedDrugs, userChoiceRecords) {
  // Create the table element
  const table = document.createElement('table');

  // Create the table header row
  const headerRow = document.createElement('tr');
  headerRow.appendChild(document.createElement('th')); // Empty cell

  // Iterate over savedDrugs
  savedDrugs.forEach(drug => {
    // Check if the drug is present in drugsArray
    if (drugsArray.includes(drug)) {
      const cell = document.createElement('th');
      cell.textContent = drug;
      headerRow.appendChild(cell);
    }
  });

  table.appendChild(headerRow);

  // Store the current selected cell
  let selectedCell = null;

  // Event handler for cell click
  function cellClickHandler(event) {
    const cell = event.target;
    if (cell === selectedCell) {
      return; // Ignore if same cell is clicked
    }

    // Clear previous selected cell style
    if (selectedCell) {
      selectedCell.classList.remove('selected');
    }

    // Update selected cell and apply style
    selectedCell = cell;
    selectedCell.classList.add('selected');

    const rowIndex = cell.parentElement.rowIndex;
    const columnIndex = cell.cellIndex;

    // Get the corresponding drug and side effect for the clicked cell
    const drug = savedDrugs[columnIndex - 1];
    const sideEffect = sideEffectsArray[rowIndex - 1];

    // Find the matching recordIds for the selected cell
    const matchedRecord = matchingRecordIds.find(
      record => record.drug === drug && record.sideEffect === sideEffect
    );

    if (matchedRecord) {
      const recordIds = matchedRecord.recordIds;

      // Iterate through userChoiceRecords to find the matching records
      const matchedRecords = userChoiceRecords.filter(record => recordIds.includes(record.record_id));

      // Display the matched records below the table
      displayRecordDetails(matchedRecords);
    } else {
      clearRecordDetails();
    }
  }

  function displayRecordDetails(records) {
    // Clear previous record details
    clearRecordDetails();

    // Iterate through the matched records and display each record
    records.forEach(record => {
      const recordContainer = document.createElement('div');
      recordContainer.classList.add('record-container');

      // Iterate over the keys of the record
      Object.keys(record).forEach(key => {
        const keyElement = document.createElement('div');
        keyElement.classList.add('record-key');
        keyElement.textContent = key;
        recordContainer.appendChild(keyElement);

        const valueElement = createValueElement(record[key]);
        recordContainer.appendChild(valueElement);
      });

      recordDetailsContainer.appendChild(recordContainer);
    });
  }

  function createValueElement(value) {
    const valueElement = document.createElement('div');
    valueElement.classList.add('record-value');
    const truncatedValue = truncateText(value, 50);
    valueElement.textContent = truncatedValue;

    if (value.length > 50) {
      // Add click event listener to expand/collapse the value
      valueElement.addEventListener('click', function () {
        if (valueElement.classList.contains('expanded')) {
          valueElement.textContent = truncatedValue;
          valueElement.classList.remove('expanded');
        } else {
          valueElement.textContent = value;
          valueElement.classList.add('expanded');
        }
      });
      valueElement.classList.add('truncated');
    }

    return valueElement;
  }

  function truncateText(value, maxLength) {
    if (typeof value === 'string') {
      if (value.length <= maxLength) {
        return value;
      }
      return value.substring(0, maxLength) + '...';
    } else if (Array.isArray(value)) {
      return value.map(item => truncateText(item, maxLength)).join(', ');
    } else if (typeof value === 'object') {
      return Object.keys(value)
        .map(prop => `${prop}: ${truncateText(value[prop], maxLength)}`)
        .join(', ');
    }
    return value;
  }

  function clearRecordDetails() {
    while (recordDetailsContainer.firstChild) {
      recordDetailsContainer.removeChild(recordDetailsContainer.firstChild);
    }
  }

  // Iterate through combinations of drug and side effect
  sideEffectsArray.forEach(sideEffect => {
    const row = document.createElement('tr');
    const sideEffectCell = document.createElement('td');
    sideEffectCell.textContent = sideEffect;
    row.appendChild(sideEffectCell);

    // Iterate over savedDrugs to generate the cells for each drug and side effect combination
    savedDrugs.forEach(drug => {
      const cell = document.createElement('td');
      const matchedRecord = matchingRecordIds.find(
        record => record.drug === drug && record.sideEffect === sideEffect
      );

      if (matchedRecord) {
       const recordIdsCount = matchedRecord.recordIds.length;
        cell.textContent = recordIdsCount;
        cell.addEventListener('click', cellClickHandler);
      } else {
        cell.textContent = '0';
      }
      row.appendChild(cell);
    });
    table.appendChild(row);
  });
  return table;
}

// Clear localStorage on beforeunload event
window.addEventListener('beforeunload', function() {
  localStorage.removeItem('savedDrugs');
});







  
  
  


