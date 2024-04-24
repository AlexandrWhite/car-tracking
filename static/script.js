function fetchCountTable() {
    fetch('/count_table')
    .then(response => response.json())
    .then(data => {
        document.getElementById('count_table').innerHTML = data.data;
    })
    .catch(error => console.error('Error:', error));
}
//Запрашивать таблицу каждую секунду
setInterval(fetchCountTable, 1000);