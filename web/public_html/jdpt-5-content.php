
	<div class="blabla help text-left">
	This graph shows the distance in levels between a kanji from the JDTP and its equivalent level in the JLPT<br />
	For example, if the distance is 3, a JDPT kanji level 5 (extremely common in drama) is only level 2 in the JLPT.
	On the other side, a negative distance means that the kanji is learned earlier in the JLPT than in the JDPT.<br />
	For each possible distance, only the ten most common kanji are shown.
	</div>
	<br />	
	<canvas id="jdtp_to_jlpt" width="20" height="10"></canvas>
	<br />	
	<button onclick="resetZoom1()">Reset Zoom</button>
	<br />	
	<br />	
	
	<table class="table table-sm table-stripped text-left" id="table_jdtp_to_jlpt">
		<tr>
			<th>Distance</th>
			<th>Kanji(Count)</th>
		</tr>
	</table>
	
	<div class="blabla help text-left">
	This graph shows the distance in levels between a kanji from the JLPT and its equivalent level in the JDPT<br />
	</div>
	<canvas id="jltp_to_jdpt" width="20" height="10"></canvas>
	<br />	
	<button onclick="resetZoom2()">Reset Zoom</button>
	<br />	
	<table class="table table-sm table-stripped text-left" id="table_jltp_to_jdpt">
		<tr>
			<th>Distance</th>
			<th>Kanji(Count)</th>
		</tr>
	</table>
	
	
	<script>
		var chart_array = [];
		window.resetZoom1 = function() {
			chart_array[0].resetZoom();
		};
		window.resetZoom2 = function() {
			chart_array[1].resetZoom();
		};
	</script>
		
	<?php
		include("jdpt_jlpt_dist.js");	
	?>
		
	<script>
	 var current_table = 'table_jdtp_to_jlpt';
	 var current_level = 5;
	 var current_chart = 'jdtp_to_jlpt';
	 var current_label = jdpt_5_to_jlpt_label;
	 var current_data = jdpt_5_to_jlpt_data;
	 var current_title = 'Distance of JDPT kanji compared to the equivalent JLPT level';
	</script>
	
	<?php
		include("chart_jdtp_to_jlpt.js");
		include("table_jdtp_to_jlpt.js");	
	?>
			
	<script>
	 var current_table = 'table_jltp_to_jdpt';
	 var current_chart = 'jltp_to_jdpt';
	 var current_label = jlpt_5_to_jdpt_label;
	 var current_data = jlpt_5_to_jdpt_data;
	 var current_title = 'Distance of JLPT kanji compared to the equivalent JDPT level';
	</script>
	
	<?php
		include("chart_jdtp_to_jlpt.js");	
		include("table_jdtp_to_jlpt.js");	
	?>
			
			
	<div class="text-left blabla" >
		<br /> 
		Below you can find the list of all JDPT kanji for this level.
		<br /> 
	</div>
	
	<?php
		include("jdpt_utils.php");
		drawJdptTable($con, 5);
	?>