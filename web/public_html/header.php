
<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="style.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
   <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>JDramaStuff - Learn Japanese using Vocabulary from Japanese Drama</title>
</head> 

	<script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
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
	// remove all and save
    while (table.rows.length > 1) {
        myRows[row++] = table.rows[1];
        table.rows[0].parentNode.removeChild(table.rows[1]);
    }
	// re insert in sorted order
    table.rows[0].parentNode.insertBefore(myRows[dict_c_to_r[dict[0][0]] - 1], table.rows[0]);
    table.rows[0].parentNode.insertBefore(table.rows[1], table.rows[0]);

    for (i = myRows.length - 1; i >= 0; i--) {
        table.rows[0].parentNode.insertBefore(myRows[dict_c_to_r[dict[i][0]] - 1], table.rows[1]);
    }
}
</script>
<nav class="navbar navbar-expand-sm bg-light navbar-light justify-content-center" >
	<a class="navbar-brand" href="index.php">JDramaStuff</a>
</div>
</nav>
<nav class="navbar navbar-expand-sm bg-secondary navbar-light justify-content-center " >
  <!-- Links -->
  <ul class="navbar-nav ">
    <li class="nav-item ">
      <a class="nav-link text-white" href="char_count.php">Character Count</a>
    </li>
    <li class="nav-item">
      <a class="nav-link text-white">|</a>
    </li>
    <li class="nav-item">
      <a class="nav-link text-white" href="intro.php">JDPT</a>
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
      <a class="nav-link text-white" href="about.php">About</a>
    </li>
    </li>
      <a class="nav-link text-white">|</a>
    </li>
    <li class="nav-item">
      <a class="nav-link text-white" href="kiku-nihongo.php">Kiku Nihongo</a>
    </li>
  </ul>
</nav>


