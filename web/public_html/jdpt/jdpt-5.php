	<canvas id="jdtp_to_jlpt" width="20" height="10"></canvas>
	<canvas id="jltp_to_jdpt" width="20" height="10"></canvas>
	<button onclick="resetZoom()">Reset Zoom</button>
	
	<script>
		var chart_array = [];
		window.resetZoom = function() {
			chart_array[0].resetZoom();
			chart_array[1].resetZoom();
		};
	</script>
		
	<?php
		include("jdpt_jlpt_dist.js");	
	?>
		
	<script>
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
		Below you can find the list of all JDPT 5 kanji.
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
		$ctr=0;
		while($row = mysqli_fetch_array($result))
		{
			if((int)$row['jdpt'] != 5){
				continue;
			}
			$ctr=$ctr+1;
			
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
	if($ctr == 100){
		echo "Kanji display limited to maximum 100 results for the moment.";
	}
		?>
	
	</div>