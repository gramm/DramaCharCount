<script>

var myTable = document.getElementById(current_table);

/* build dict */
var dict = new Object();
for (var i in current_data) {
    var point = current_data[i];
    dist = point['x'];
    count = point['y'];
	
    if (dict[dist]) {
    } else {
        dict[dist] = new Object();
    }
		dict[dist][Object.keys(dict[dist]).length] = current_label[i] + "(" + count + ")";
}

/* sort dict */
var keyValues = [];

for (var key in dict) {
    keyValues.push([key, dict[key]]);
}

keyValues.sort(function compare(kv1, kv2) {
    return parseInt(kv1[0]) - parseInt(kv2[0])
})


/* publish */
row = myTable.insertRow();


for (var k in keyValues) {

    dist = keyValues[k][0];
    let cell = row.insertCell();

    if (dist == 0) {
        text = document.createTextNode("Same level");
    } else if (dist == current_level) {
        if (current_chart == 'jdtp_to_jlpt') {
            text = document.createTextNode("Not in JLPT");
        } else {
            text = document.createTextNode("Not in JDPT");
        }
    } else {
        text = document.createTextNode(dist)
    }

    cell.appendChild(text);
}

row = myTable.insertRow();

cells = new Object();
for (i = 0; i < 10; i++) {
    cells[i] = new Object();
    row = myTable.insertRow();
    for (var k in keyValues) {
        cell = row.insertCell();
        cells[i][k] = cell;
    }
}

var col = 0;
for (var k in keyValues) {
	var index = keyValues[k][0];
    if (dict[index]) {
        for (i = 0; i < 10; i++) {
            if (dict[index][i]) {
                text = document.createTextNode(dict[index][i])
                cells[i][col].appendChild(text);
            }
        }
		col++;
    }
}
</script>