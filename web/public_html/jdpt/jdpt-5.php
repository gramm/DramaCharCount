
	
	<div class="blabla help text-left">
	This graph shows the distance in levels between a kanji from the JDTP and its equivalent level in the JLPT<br />
	For example, if the distance is 3, a JDPT kanji level 5 (extremely common in drama) is only level 2 in the JLPT.
	On the other side, a negative distance means that the kanji is learned earlier in the JLPT than in the JDPT.<br />
	For each possible distance, only the ten most common kanji are shown.
	</div>
	<canvas id="jdtp_to_jlpt" width="20" height="10"></canvas>
	<button onclick="resetZoom1()">Reset Zoom</button>
	
	
	<div class="blabla help text-left">
	This graph shows the distance in levels between a kanji from the JLPT and its equivalent level in the JDPT<br />
	</div>
	<canvas id="jltp_to_jdpt" width="20" height="10"></canvas>
	<button onclick="resetZoom2()">Reset Zoom</button>
	
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
	 var current_level = 5;
	 var current_chart = 'jdtp_to_jlpt';
	 var current_label = jdpt_5_to_jlpt_label;
	 var current_data = jdpt_5_to_jlpt_data;
	 var current_title = 'Distance of JDPT kanji compared to the equivalent JLPT level';
	</script>
	
	<?php
		include("chart_jdtp_to_jlpt.js");	
	?>
			
	<script>
	 var current_chart = 'jltp_to_jdpt';
	 var current_label = jlpt_5_to_jdpt_label;
	 var current_data = jlpt_5_to_jdpt_data;
	 var current_title = 'Distance of JLPT kanji compared to the equivalent JDPT level';
	</script>
	
	<?php
		include("chart_jdtp_to_jlpt.js");	
	?>
			
			
	<script>

</script>

	<div class="text-left blabla">
		<br /> 
		Below you can find the list of all JDPT kanji for this level.
		<br /> 
		
		<?php

	// first join selects all kanji used in this drama
	// second join merges jlpt to this selection but keeps only allowed jlpt
	$query = "
	SELECT * from count, kanji_info, kanji
	WHERE count.drama_uid = 1 AND count.kanji_uid = kanji_info.kanji_uid  AND kanji.kanji_uid = kanji_info.kanji_uid
	ORDER BY count.count DESC
	";
	$result = mysqli_query($con,$query);
		
	
	
	//do word table
	
	echo "<table class='table table-bordered table-striped table-sm'>
		<tr>
			<th>Word</th>
			<th>Count</th>
			<th>Jlpt</th>
			<th>Jōyō </th>
			<th>Jdpt </th>
			<th>Jdpt to Jlpt </th>
		</tr>";

		$wordTable = "";
		while($row = mysqli_fetch_array($result))
		{
			if((int)$row['jdpt'] != 5){
				continue;
			}
			
			echo "<tr>";
				echo "<td>" . $row['value'] . "</a></td>";
				
				echo "<td>" . $row['count'] . "</td>";
				
				if(((int)$row['jlpt'])>0) {echo "<td>" . $row['jlpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jouyou'])>0) {echo "<td>" . $row['jouyou'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jdpt'])>0) {echo "<td>" . $row['jdpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['dist_to_jlpt'])!=99) {echo "<td>" . $row['dist_to_jlpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
			echo "</tr>";
		}
	echo "</table>";
		?>
	
	</div>