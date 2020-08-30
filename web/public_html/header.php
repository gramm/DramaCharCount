
<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="style.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <title>JDramaStuff - Learn Japanese using Vocabulary from Japanese Drama</title>
</head> 

<script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@0.7.0"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@0.7.7"></script>

<?php
	include('openConnection.php');	
	openConnection();
?>

	<script>
function sortTable(n, level) {
    var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    switchcount = 0;
    table = document.getElementById("myTable");

    var dict = new Object();
    var dict_c_to_r = new Object();
    rows = table.rows;
    for (i = 1; i < rows.length; i++) {

        c = rows[i].getElementsByTagName("TD")[0].innerHTML;
        x = rows[i].getElementsByTagName("TD")[n].innerHTML.toLowerCase();
        var ix = parseInt(x);
        if (isNaN(ix) == false) {
            x = ix;
        }
        if (x == "same level") {
            x = 0;
        }
        if (x == "not in jlpt") {
            x = level;
        }

        dict[c] = x;
		dict_c_to_r[c] = i;
    }
    // Create items array
    var items = Object.keys(dict).map(function (key) {
        return [key, dict[key]];
    });

    // Sort the array based on the second element
    items.sort(function (first, second) {
        return second[1] - first[1];
    });

    dict = items;
	let myRows = [];
	var row = 0;
	while(table.rows.length > 1){
		myRows[row++] = table.rows[1];
	    table.rows[0].parentNode.removeChild(table.rows[1]);
	}
		table.rows[0].parentNode.insertBefore(myRows[dict_c_to_r[dict[0][0]] - 1], table.rows[0]);
		table.rows[0].parentNode.insertBefore(table.rows[1], table.rows[0]);
		
    for (i = myRows.length - 1; i >= 0 ; i--) {
		table.rows[0].parentNode.insertBefore(myRows[dict_c_to_r[dict[i][0]] - 1], table.rows[1]);
		//table.appendChild(myRows[dict_c_to_r[dict[i][0]] - 1]);
	}
	
	//table.rows[0].parentNode.insertBefore(table.rows[0], table.rows[table.rows.length - 1]);
	
	
	/*
    for (i = 1; i < items.length; i++) {
		
		row_new = dict_c_to_r[items[i][0]];
		cur_top = rows[i].getElementsByTagName("TD")[0].innerHTML;
		dict_c_to_r[cur_top] = dict_c_to_r[items[i][0]]
		
		myRows = 

		
		
		//rows[1].parentNode.insertBefore(table.rows[row_new], table.rows[i]);
		//rows[1].parentNode.insertBefore(table.rows[2], table.rows[row_new + 1]);
		var shifted = table.rows[row_new];
	    rows[0].parentNode.removeChild(table.rows[row_new]);
		table.appendChild(shifted);
    }	
	*/
}
</script>
<nav class="navbar navbar-expand-sm bg-light navbar-light justify-content-center" >
	<a class="navbar-brand" href="index.php">JDramaStuff</a>
</div>
</nav>
<nav class="navbar navbar-expand-sm bg-secondary navbar-light justify-content-center" >
  <!-- Links -->
  <ul class="navbar-nav ">
    <li class="nav-item ">
      <a class="nav-link text-white" href="?page=char_count.php">Character Count</a>
    </li>
    <li class="nav-item">
      <a class="nav-link text-white">|</a>
    </li>
    <li class="nav-item">
      <a class="nav-link text-white" href="?page=jdpt.php">JDPT</a>
    </li>
      <a class="nav-link text-white">|</a>
    </li>
	<!--
    <li class="nav-item">
      <a class="nav-link text-white" href="?page=blog.php">Blog</a>
    </li>
    <li class="nav-item">
      <a class="nav-link text-white">|</a>
    </li>
	-->
    <li class="nav-item">
      <a class="nav-link text-white" href="?page=about.php">About</a>
    </li>
  </ul>
</nav>


