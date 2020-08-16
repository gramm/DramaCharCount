<!DOCTYPE html>
<html>
<?php
// Declaration of global variables 
$allDramas; 
$selectedDrama;
$selectedDramaName;
$filteredJlptKanjiLevelCheckboxes = array_fill(0, 6, 0); /*fill from 0 to 6 with 0 */
$filteredJouyouKanjiLevelCheckboxes = array_fill(0, 8, 0); /*fill from 0 to 7 with 0 */
$selectedWord;
$currentUrl;
$filteredUserKanji;
$wordTable = "hello";
?>
<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="style.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</head> 

<?php

include('openConnection.php');	
openConnection();
init();
parseGetInfo();
?>
<body>

<?php
include('header.php');	
?>


	
<div id="gui" class="container">
	<div class="row">
		<div class="col align-self-center">
	
	<br />
	<form action="" method="get">
	<!-- Drama selection dropdown menu -->
	<select id="drama" name="drama" onchange="this.form.submit();" >
	<?php
		GLOBAL $allDramas;
		GLOBAL $selectedDramaName;
		echo "<option value=".$selectedDrama." >".$selectedDramaName."</option>";
		foreach($allDramas as $drama)
		{
			echo "<option value=".$drama[1]." >".$drama[0]."</option>";
		}
	?>
	</select>
	
	<!-- Jlpt selection checkboxes -->
	<br/>
	<br/>
	<table class='table' >
		<tr>
			<td>
			Hide kanji belonging to JLPT level:<br/>
			<table class='table table-striped table-bordered table-sm' style="height: 100px;">
			
			</label>
				<tr><td><label ><input class="checkbox" type="checkbox" name="jlpt_kanji_list[]" value="5"  <?php if($filteredJlptKanjiLevelCheckboxes[5]!=0){echo "checked";} ?>> JLPT 5</label>        </td></tr>
				<tr><td><label ><input class="checkbox" type="checkbox" name="jlpt_kanji_list[]" value="4"  <?php if($filteredJlptKanjiLevelCheckboxes[4]!=0){echo "checked";} ?>> JLPT 4</label>         </td></tr>
				<tr><td><label ><input class="checkbox" type="checkbox" name="jlpt_kanji_list[]" value="3"  <?php if($filteredJlptKanjiLevelCheckboxes[3]!=0){echo "checked";} ?>> JLPT 3</label>         </td></tr>
				<tr><td><label ><input class="checkbox" type="checkbox" name="jlpt_kanji_list[]" value="2"  <?php if($filteredJlptKanjiLevelCheckboxes[2]!=0){echo "checked";} ?>> JLPT 2</label>         </td></tr>
				<tr><td><label ><input class="checkbox" type="checkbox" name="jlpt_kanji_list[]" value="1"  <?php if($filteredJlptKanjiLevelCheckboxes[1]!=0){echo "checked";} ?>> JLPT 1</label>         </td></tr>	
				<tr><td><label ><input class="checkbox" type="checkbox" name="jlpt_kanji_list[]" value="0"  <?php if($filteredJlptKanjiLevelCheckboxes[0]!=0){echo "checked";} ?>> Not in JLPT</label>    </td></tr>
			</table>	
			</td>
			<td>
				<table class='table table-striped table-bordered table-sm' border='0'>
				Hide kanji belonging to jōyō level:<br/>
				
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="7"  <?php if($filteredJouyouKanjiLevelCheckboxes[7]!=0){echo "checked";} ?> > Secondary school</label></td></tr>	
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="6"  <?php if($filteredJouyouKanjiLevelCheckboxes[6]!=0){echo "checked";} ?> > 6th grade</label>	      </td></tr>
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="5"  <?php if($filteredJouyouKanjiLevelCheckboxes[5]!=0){echo "checked";} ?> > 5th grade</label>       </td></tr>
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="4"  <?php if($filteredJouyouKanjiLevelCheckboxes[4]!=0){echo "checked";} ?>>  4th grade</label>        </td></tr>
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="3"  <?php if($filteredJouyouKanjiLevelCheckboxes[3]!=0){echo "checked";} ?>>  3rd grade</label>        </td></tr>
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="2"  <?php if($filteredJouyouKanjiLevelCheckboxes[2]!=0){echo "checked";} ?>>  2nd grade</label>        </td></tr>
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="1"  <?php if($filteredJouyouKanjiLevelCheckboxes[1]!=0){echo "checked";} ?>>  1st grade</label>        </td></tr>
				<tr><td><label><input type="checkbox" name="jouyou_kanji_list[]" value="0"  <?php if($filteredJouyouKanjiLevelCheckboxes[0]!=0){echo "checked";} ?>>  Not in jōyō</label>      </td></tr>
				</table>
			</td>
		</tr>
	</table>
		
	Hide following kanji or characters:<br/>
	<textarea cols="120" rows="2" name="filteredUserKanji"><?php if(!empty($filteredUserKanji)){echo $filteredUserKanji;}else{echo "";} ?></textarea>
	<br />


	<input type="submit" value = "Refresh" />
	</form>
		</div>
	</div>
</div>
	
	
	
	
	<div id="mainNav" class="container">
	<div class="row">
		<div class="col align-self-center">
	<?php
		displayWordTable();
	?>
		</div>
	<div class="col align-self-top">

	<?php
	GLOBAL $selectedWord;
	
	if(is_null($selectedWord))
	{
		echo "No kanji selected.";
	}
	else
	{
		displayLines();
	}
	
	?>
	
	</div>
	</div>
	</div>
	
	<div id="mainArticle" class="container">
	<div class="row">
	</div>
	</div>
	
	<script language='javascript'>
	
	function doCsv() {
		var myVar = "<?php echo $wordTable; ?>";
		myVar = myVar.replace(/§/g, '\n');
		
		var csv = 'Kanji\tCount\tJLPT\tJouyou\t\n';
		csv += myVar;
		
		
		console.log(csv);
		var hiddenElement = document.createElement('a');
		hiddenElement.href = 'data:text/csv;charset=utf-8,' + (csv);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'data.txt';
		hiddenElement.click();
	
	}
	</script>
	
	</body>
	
	
	
	
<?php

function displayLines()
{
	GLOBAL $con;
	GLOBAL $selectedDrama;
	GLOBAL $selectedWord;
	
	$start_time = microtime(true); 

	$query = "
	select a.value
	from line a 
	INNER JOIN kanji_to_line b
	ON a.line_uid=b.line_uid
	WHERE (b.kanji_uid = ".$selectedWord.")
	";
	$result = mysqli_query($con,$query);
	
	
	$end_time = microtime(true); 
	$execution_time = ($end_time - $start_time); 
	//echo "displayLines took ".$execution_time." seconds to execute the script"; 
	
	while($row = mysqli_fetch_array($result)){
		echo $row['value']."<br/>";
	}
		echo "<br/>";
		echo "Line display limited to 100 results. <br/>";
	
	mysqli_close($con);
}


function init()
{
	GLOBAL $allDramas;
	GLOBAL $currentUrl;
	$allDramas = getDramaList();
	//Set http/https stuff for some reasons
	$currentUrl = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
	
	//Save the current url as global but remove &kanji...; This is to avoid appending &kanji multiple time when other kanji is selected 
	if(strpos($currentUrl, '&kanji=') !== false)
	{
		$currentUrl = substr( $currentUrl , 0 , strpos($currentUrl, '&kanji='));
	}
	
	
}


function displayWordTable()
{
	GLOBAL $con;
	GLOBAL $currentUrl;
	GLOBAL $selectedDrama;
	GLOBAL $filteredJlptKanjiLevel;
	GLOBAL $filteredJouyouKanjiLevel;
	GLOBAL $filteredJlptKanjiLevelCheckboxes;
	GLOBAL $filteredJouyouKanjiLevelCheckboxes;
	GLOBAL $filteredUserKanji;
	GLOBAL $wordTable;
	
	if(is_null($selectedDrama))
	{
		echo "No drama selected";
		return;
	}

	
	echo "<a href=\"#\" onclick=\"doCsv()\">Export as CSV</a><br/>";
	echo "Hint: to open in Excel copy-paste the CSV content directly into Excel<br/>";
	
	$sqlFilteredJlptKanjiLevel = implode(",",$filteredJlptKanjiLevel)/* for example "5,4" if jlpt 5 and 4 filtered */;
	$sqlFilteredJouyouKanjiLevel = implode(",",$filteredJouyouKanjiLevel)/* for example "5,4" if jlpt 5 and 4 filtered */;
	

	/* user filter to array with unicode support */
	$sqlFilteredUserKanji;
	if(!empty($filteredUserKanji)){
		$len = mb_strlen($filteredUserKanji, 'UTF-8');
		$filteredUserKanjiAsArray = [];
		for ($i = 0; $i < $len; $i++) {
			$filteredUserKanjiAsArray[] = mb_substr($filteredUserKanji, $i, 1, 'UTF-8');
	}
	
	/* put '' for SQL search */
	for ($i = 0; $i < count($filteredUserKanjiAsArray); $i++) {
		$filteredUserKanjiAsArray[$i] = '\''.$filteredUserKanjiAsArray[$i].'\'';
	}
	$sqlFilteredUserKanji = implode(",",$filteredUserKanjiAsArray);
	}
	else
	{
		$sqlFilteredUserKanji = '\'\'';
	}
	
	// first join selects all kanji used in this drama
	// second join merges jlpt to this selection but keeps only allowed jlpt
	
	$result = mysqli_query($con,"
	SELECT a.value, b.count, a.kanji_uid, c.jlpt, c.jouyou
	FROM kanji a
	INNER JOIN count b
	ON a.kanji_uid = b.kanji_uid
	INNER JOIN kanji_info c
	ON a.kanji_uid = c.kanji_uid
	AND c.jlpt NOT IN (".$sqlFilteredJlptKanjiLevel.")
	AND c.jouyou NOT IN (".$sqlFilteredJouyouKanjiLevel.")
	AND c.flag IN (1)
	AND a.value NOT IN (".$sqlFilteredUserKanji.")
	
	WHERE b.drama_uid = ".$selectedDrama."  
	ORDER BY `b`.`count` DESC
	LIMIT 25
	");
		
	
	
	//do word table
	
	echo "<table class='table table-striped table-sm' border='1'>
		<tr>
			<th>Word</th>
			<th>Count</th>
			<th>Jlpt</th>
			<th>Jōyō </th>
		</tr>";

		$wordTable = "";
		while($row = mysqli_fetch_array($result))
		{
			
			$wordTable = $wordTable.$row['value'].'\t';
			$wordTable = $wordTable.$row['count'].'\t';
			$wordTable = $wordTable.$row['jlpt'].'\t';
			$wordTable = $wordTable.$row['jouyou']."§";
			
			echo "<tr>";
				echo "<td><a href=\"".$currentUrl."&kanji=".$row['kanji_uid']."\">" . $row['value'] . "</a></td>";
				echo "<td>" . $row['count'] . "</td>";
				if(((int)$row['jlpt'])>0) {echo "<td>" . $row['jlpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jouyou'])>0) {echo "<td>" . $row['jouyou'] . "</td>";}
				else {echo "<td>-</td>";}
			echo "</tr>";
		}
	echo "</table>";
}

function getDramaList()
{
	GLOBAL $con;
	GLOBAL $allDrama;
	
	$allDrama = array();
	$i = 0;
	$query = mysqli_query($con,"SELECT name, drama_uid FROM drama");
	while($row = mysqli_fetch_array($query)){
		$allDrama[$i][0] = $row['name'];
		$allDrama[$i][1] = $row['drama_uid'];
		$i++;
	}

	return $allDrama ;

}

function parseGetInfo()
{
	GLOBAL $con;
	GLOBAL $selectedDrama;
	GLOBAL $selectedWord;
	GLOBAL $filteredJlptKanjiLevel;
	GLOBAL $filteredJouyouKanjiLevel;
	GLOBAL $filteredJlptKanjiLevelCheckboxes;
	GLOBAL $filteredJouyouKanjiLevelCheckboxes;
	GLOBAL $selectedDramaName;
	GLOBAL $allDrama;
	GLOBAL $filteredUserKanji;
	
	// find selected drama
	if((empty($_GET["drama"])) || ($_GET["drama"]=="NoSelection"))
	{
		$selectedDrama=null;
		$selectedDramaName= "Select drama...";
	}
	else
	{
		$selectedDrama=$_GET["drama"];
		$selectedDramaName= $allDrama[$selectedDrama - 1][0]; // - 1 because drama index starts at 1
	}
	
	// find selected word
	if(empty($_GET["kanji"]))
	{
		$selectedWord=null;
	}
	else
	{
		$selectedWord=$_GET["kanji"];
	}
	
	// find filtered JLPT kanji
	if(!empty($_GET['jlpt_kanji_list'])){
		foreach($_GET['jlpt_kanji_list'] as $selected){
			// set global var
			$filteredJlptKanjiLevel[$selected] = $selected;
			$filteredJlptKanjiLevelCheckboxes[$selected] = 1;
		}
	}
	else
	{
		$filteredJlptKanjiLevel[0] = 6;
	}
	
	// find filtered Jouyou kanji
	if(!empty($_GET['jouyou_kanji_list'])){
		foreach($_GET['jouyou_kanji_list'] as $selected){
			// set global var
			$filteredJouyouKanjiLevel[$selected] = $selected;
			$filteredJouyouKanjiLevelCheckboxes[$selected] = 1;
		}
	}
	else
	{
		$filteredJouyouKanjiLevel[0] = 6;
	}
	
	// find filtered user kanji
	if(!empty($_GET['filteredUserKanji'])){
		$filteredUserKanji = $_GET['filteredUserKanji'];
	}
	else
	{
		$filteredUserKanji = null;
	}
	
}

?>


</html>