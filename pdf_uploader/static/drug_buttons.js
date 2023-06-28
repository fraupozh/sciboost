// drug_buttons.js

// Function to generate buttons for drug entities
function generateButtons() {
  fetch('/download_json/') // Fetch the JSON data from the backend
    .then(response => response.json())
    .then(data => {
      // Extract drug entities from the JSON data
      const drugEntities = data.flatMap(record => record.drug_entities.split(', '))
                               .map(drug => drug.replace("[", "").replace("]", "").replace(/'/g, ""));
      
      // Filter for unique drug entities
      const uniqueDrugs = [...new Set(drugEntities)];

      // Get the button container element
      const buttonContainer = document.getElementById('button-container');

      // Generate buttons for each drug entity
      uniqueDrugs.forEach(drug => {
        const button = document.createElement('button');
        button.textContent = drug;
        buttonContainer.appendChild(button);
      });
    })
    .catch(error => console.error('Error:', error));
}


  
  
 
  