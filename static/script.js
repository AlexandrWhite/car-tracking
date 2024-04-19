function fetchSlonik() {
    fetch('/slonik')
    .then(response => response.json())
    .then(data => {
        document.getElementById('best_animal').innerHTML = data.animal_table;
    })
    .catch(error => console.error('Error:', error));
}
//setInterval(fetchSlonik, 1000);
