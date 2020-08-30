<?php

function drawJdptTable($con, $level)
{
	// first join selects all kanji used in this drama
	// second join merges jlpt to this selection but keeps only allowed jlpt
	$query = "
	SELECT * from count, kanji_info, kanji
	WHERE count.drama_uid = 1 AND count.kanji_uid = kanji_info.kanji_uid  AND kanji.kanji_uid = kanji_info.kanji_uid
	ORDER BY count.count DESC
	";
	$result = mysqli_query($con,$query);
		
	
	
	//do word table
	
	echo "<table class='table table-bordered table-striped table-sm' id='myTable'>
		<tr>
			<th onclick='sortTable(0, ".$level.")'>Word</th>
			<th onclick='sortTable(1, ".$level.")'>Count</th>
			<th onclick='sortTable(2, ".$level.")'>Jlpt</th>
			<th onclick='sortTable(3, ".$level.")'>Jōyō </th>
			<th onclick='sortTable(4, ".$level.")'>Jdpt </th>
			<th onclick='sortTable(5, ".$level.")'>Jdpt to Jlpt </th>
		</tr>";

		$wordTable = "";
		while($row = mysqli_fetch_array($result))
		{
			if((int)$row['jdpt'] != $level){
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
				
				
				if(((int)$row['dist_to_jlpt']) == 0) {echo "<td>" . "Same level" . "</td>";}
				else if(((int)$row['dist_to_jlpt']) == $level) {echo "<td>" . "Not in JLPT" . "</td>";}
				else if(((int)$row['dist_to_jlpt'])!=99) {echo "<td>" . $row['dist_to_jlpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
				
			echo "</tr>";
		}
	echo "</table>";
}
		?>