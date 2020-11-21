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
			<th onclick='sortTable(0, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='The actual kanji'>Word</div></th>
			<th onclick='sortTable(1, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='Number of occurences in all dramas'>Count</div></th>
			<th onclick='sortTable(2, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='JLPT level'>Jlpt</div></th>
			<th onclick='sortTable(3, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='Jōyō level'>Jōyō</div></th>
			<th onclick='sortTable(4, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='JDPT level'>Jdpt</div></th>
			<th onclick='sortTable(5, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='JLPT position (sorted by level then by count between all dramas)'>Jlpt pos</div></th>
			<th onclick='sortTable(6, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='Jōyō position (sorted by level then by count between all dramas)'>Jōyō pos</div></th>
			<th onclick='sortTable(7, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='JSPT position (sorted by count between all dramas)'>Jdpt pos</div></th>
			<th onclick='sortTable(8, ".$level.")'><div data-toggle='tooltip' data-placement='right' title='Position difference between the JLPT and JDPT position. For example, 1500 means that the JLPT position is positioned 1500 kanji later than in the JDPT.'>Diff Jdpt to Jlpt</div></th>
		</tr>";

		$wordTable = "";
		while($row = mysqli_fetch_array($result))
		{
			echo "<tr>";
				echo "<td>" . $row['value'] . "</a></td>";
				
				echo "<td>" . $row['count'] . "</td>";
				
				if(((int)$row['jlpt'])>0) {echo "<td>" . $row['jlpt'] . "</td>";}
				else {echo "<td>Not in JLPT</td>";}
				
				if(((int)$row['jouyou'])>0) {echo "<td>" . $row['jouyou'] . "</td>";}
				else {echo "<td>Not in Jōyō</td>";}
				
				if(((int)$row['jdpt'])>0) {echo "<td>" . $row['jdpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jlpt_pos'])>0) {echo "<td>" . $row['jlpt_pos'] . "</td>";}
				else {echo "<td>Not in JLPT</td>";}
				
				if(((int)$row['jouyou_pos'])>0) {echo "<td>" . $row['jouyou_pos'] . "</td>";}
				else {echo "<td>Not in Jōyō</td>";}
				
				if(((int)$row['jdpt_pos'])>0) {echo "<td>" . $row['jdpt_pos'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jdpt_to_jlpt'])!= -32768) {echo "<td>" . $row['jdpt_to_jlpt'] . "</td>";}
				else {echo "<td>Not in JLPT</td>";}
				
				/*
				if(((int)$row['dist_to_jlpt']) == 0) {echo "<td>" . "Same level" . "</td>";}
				else if(((int)$row['dist_to_jlpt']) == $level) {echo "<td>" . "Not in JLPT" . "</td>";}
				else if(((int)$row['dist_to_jlpt'])!=99) {echo "<td>" . $row['dist_to_jlpt'] . "</td>";}
				else {echo "<td>-</td>";}
				*/
				
				
			echo "</tr>";
		}
	echo "</table>";
}
		?>