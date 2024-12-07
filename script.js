(async () => {
	let data = await getData('./drugs.json');
	let bac = await getData('./bacs.json');
	//add suggestion
	let datalist1 = document.getElementById('suggestions1');
	Object.keys(data).forEach(item => {
		var option = document.createElement('option');
		option.value = item;
		datalist1.appendChild(option);
	})
	let  datalist2 = document.getElementById('suggestions2');
	Object.keys(bac).forEach(item => {
		var option = document.createElement('option');
		option.value = item;
		datalist2.appendChild(option);
	})
})();

document.getElementById('user-input1').addEventListener('submit', async (event) => {
	event.preventDefault();

	const data = await getData('./drugs.json');
	const bac = await getData('./bacs.json');
	const input = document.getElementById('input-field1').value.trim();
	
	if (data.hasOwnProperty(input)){
		//reorder array
		const outputArray = Object.keys(bac).filter(item => data[input].includes(item));

		const output = document.getElementById('output');
		output.innerHTML = outputArray.join('<br>');
	}
})

document.getElementById('user-input2').addEventListener('submit', async (event) => {
	event.preventDefault();

	const data = await getData('./drugs.json');
	const input = document.getElementById('input-field2').value.trim();
	
	let outputArray = Object.keys(data).filter(key => data[key].includes(input));
	outputArray = outputArray.sort((a, b) => data[a].length - data[b].length);
	console.log(input)

	const output = document.getElementById('output');
	output.innerHTML = outputArray.join('<br>');
})
async function getData(file){
	let res = await fetch(file);
	let data = await res.json();

	return data
	
}

function createAllTable(data) {
	// get container
	const container = document.getElementById('table-container')

	// Create table element
	const table = document.createElement('table');
	const thead = document.createElement('thead');
	const tbody = document.createElement('tbody');

	// Add table headers
	const headers = ['Antibiotic', 'Bacteria'];
	const headerRow = document.createElement('tr');
	headers.forEach(header => {
		const th = document.createElement('th');
		th.innerHTML = header;
		headerRow.appendChild(th);
	});
	thead.appendChild(headerRow);

	// Add table rows
	Object.entries(data).forEach(([key, value]) => {
	const row = document.createElement('tr');
	const keyCell = document.createElement('td');
	const valueCell = document.createElement('td');

	keyCell.innerHTML = key;
	valueCell.innerHTML = value;

	row.appendChild(keyCell);
	row.appendChild(valueCell);
	tbody.appendChild(row);
	});

	// Append thead and tbody to the table
	table.appendChild(thead);
	table.appendChild(tbody);

	container.appendChild(table);
}
