<script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@0.7.0"></script>
<script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@0.7.7"></script>

	<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "desc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n].innerHTML.toLowerCase();
      y = rows[i + 1].getElementsByTagName("TD")[n].innerHTML.toLowerCase();
	  
	  var ix = parseInt(x);
	  var iy = parseInt(y);
	  if( isNaN(ix) == false){
		  x = ix;
		  y = iy;
	  }
	  
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x > y) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x < y) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "desc") {
        dir = "asc";
        switching = true;
      }
    }
  }
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


