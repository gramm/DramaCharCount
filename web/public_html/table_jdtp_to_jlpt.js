<script>

var myTable = document.getElementById(current_table);

var dict = new Object();
for (var i in current_data) {
    var point = current_data[i];
    dist = point['x'];
    count = point['y'];
    if (dict[dist]) {
        dict[dist] = dict[dist] + current_label[i] + "(" + count + ")";
    } else {
        dict[dist] = current_label[i] + "(" + count + ")";
    }
    console.log(dist);
    console.log(count);
    console.log(dict[dist]);
}


for (var dist in dict) {
	let row = myTable.insertRow();
	let cell = row.insertCell();
	text = document.createTextNode(dist)
	cell.appendChild(text);
	
	cell = row.insertCell();
	text = document.createTextNode(dict[dist])
	cell.appendChild(text);
}

</script>