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
      const userChoiceRecords = records.filter(record => {
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
  const table = generateTable(drugsArray, sideEffectsArray, matchingRecordIds, savedDrugs);

  // Append the table to the document body
  document.body.appendChild(table);
}


// !!!!!!!!!!!!!!!!!!!!!!
function generateTable(drugsArray, sideEffectsArray, matchingRecordIds, savedDrugs) {
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

  table.appendChild(headerRow)

  // Iterate through combinations of drug and side effect
  sideEffectsArray.forEach(sideEffect => {
    const row = document.createElement('tr');
    const sideEffectCell = document.createElement('td');
    sideEffectCell.textContent = sideEffect;
    row.appendChild(sideEffectCell);

    // Iterate over savedDrugs to generate the cells for each drug and side effect combination
    savedDrugs.forEach(drug => {
      const cell = document.createElement('td');
      const matchedRecord = matchingRecordIds.find(record => record.drug === drug && record.sideEffect === sideEffect);

      if (matchedRecord) {
        cell.textContent = matchedRecord.recordIds.length;
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





  
  
  


