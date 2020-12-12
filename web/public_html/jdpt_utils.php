<?php

function drawJdptTable($con, $level)
{
	$query;
	if($level != -1){
		$query = "
		SELECT * from count, kanji_info, kanji
		WHERE count.drama_uid = 0 AND count.kanji_uid = kanji_info.kanji_uid  AND kanji.kanji_uid = kanji_info.kanji_uid AND kanji_info.jdpt = ".$level." AND kanji_info.flag = 1
		ORDER BY count.count DESC
		";
	}
	else{
		$query = "
		SELECT * from count, kanji_info, kanji
		WHERE count.drama_uid = 0 AND count.kanji_uid = kanji_info.kanji_uid  AND kanji.kanji_uid = kanji_info.kanji_uid AND kanji_info.flag = 1
		ORDER BY count.count DESC
		";
	}
	
	$result = mysqli_query($con,$query);
		
	
	
	//do word table
	
	echo "<table class='table table-bordered table-striped table-sm' id='myTable'>
		<tr>
			<th onclick='sortTable(0, ".$level.")'>Kanji</th>
			<th onclick='sortTable(1, ".$level.")'>Count</th>
			<th onclick='sortTable(2, ".$level.")'>Frequency</th>
			<th onclick='sortTable(3, ".$level.")'>Cumulated Frequency</th>
			<th onclick='sortTable(4, ".$level.")'>Drama Frequency</th>
			<th onclick='sortTable(5, ".$level.")'>Episode Frequency</th>
			<th onclick='sortTable(6, ".$level.")'>JDPT</th>
			<th onclick='sortTable(7, ".$level.")'>JDPT Pos</th>
			<th onclick='sortTable(8, ".$level.")'>Jōyō</th>
			<th onclick='sortTable(9, ".$level.")'>Jōyō Pos</th>
		</tr>";

		$wordTable = "";
		while($row = mysqli_fetch_array($result))
		{
			echo "<tr>";
				echo "<td>" .$row['value'] . "</a></td>";
				
				echo "<td>" . $row['count'] . "</td>";

				echo "<td>" . number_format(100*$row['freq'],2) . "%</td>";
				
				echo "<td>" . number_format(100*$row['cumul_freq'],2) . "%</td>";
				
				echo "<td>" . number_format(100*$row['drama_freq'],2) . "%</td>";
				
				echo "<td>" . number_format(100*$row['episode_freq'],2) . "%</td>";
				
				if(((int)$row['jdpt'])>0) {echo "<td>" . $row['jdpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jdpt_pos'])>0) {echo "<td>" . $row['jdpt_pos'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jouyou'])>0) {echo "<td>" . $row['jouyou'] . "</td>";}
				else {echo "<td>Not in Jōyō</td>";}
				
				if(((int)$row['jouyou_pos'])>0) {echo "<td>" . $row['jouyou_pos'] . "</td>";}
				else {echo "<td>Not in Jōyō</td>";}
				
			echo "</tr>";
		}
	echo "</table>";
}
		?>