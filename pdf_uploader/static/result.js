// This Function you will use for the connection
// function generateButtons(data) {}
// !!! Try to replays line 5 with this function -> function generateButtons(data) {} !!!

document.addEventListener('DOMContentLoaded', function() {
    // Read the JSON file
    fetch('pubmed_records.json')
      .then(response => response.json())
      .then(data => {
        const drugEntities = data.flatMap(record => record.drug_entities.split(', '))
        .map(drug => drug.replace(/[\[\]']+/g, ''));

        const uniqueDrugs = [...new Set(drugEntities)];

        displayDrugButtons(uniqueDrugs, data); // Call the function to generate and display the drug buttons
    })
    .catch(error => console.error('Error:', error));
});


function displayDrugButtons(uniqueDrugs, data) {
    const vizDataContainer = document.getElementById('viz-data');
  
    for (const drug of uniqueDrugs) {
      const button = document.createElement('button');
      button.textContent = drug;
      button.classList.add('drug-button');
      button.dataset.drug = drug;
      button.addEventListener('click', function(event) {
        handleDrugButtonClick(event, button, data);
      });
      vizDataContainer.appendChild(button);
    }
  }
  

function handleDrugButtonClick(event, button, data) {
    const drug = button.dataset.drug; // Retrieve the drug name from the data attribute

    // Manipulate the data based on the clicked drug
    console.log('Clicked drug:', drug);
    // Add your code to manipulate the data as needed

    // Check if the button is already clicked
    const isClicked = button.classList.contains('clicked-button');

    if (isClicked) {
    // If the button is already clicked, unselect it
    button.classList.remove('clicked-button');

        
    // Remove the drug from localStorage
    const savedDrugsFromStorage = localStorage.getItem('savedDrugs');
    const updatedSavedDrugs = JSON.parse(savedDrugsFromStorage).filter(d => d !== drug);
    localStorage.setItem('savedDrugs', JSON.stringify(updatedSavedDrugs));
  } else {
    // If the button is not clicked, select it
    button.classList.add('clicked-button');

    // Save the drug in localStorage
    const savedDrugsFromStorage = localStorage.getItem('savedDrugs');
    const savedDrugs = savedDrugsFromStorage ? JSON.parse(savedDrugsFromStorage) : [];
    savedDrugs.push(drug);
    localStorage.setItem('savedDrugs', JSON.stringify(savedDrugs));
    console.log('Here are the savedDrugs:', savedDrugs);
  }

  // Share localStorage values with a new window
  const newWindow = window.open('table1.html');
}



  