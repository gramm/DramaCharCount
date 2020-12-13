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

<?php
include('header.php');	
?>

<?php

init();
parseGetInfo();
?>



<body class="d-flex flex-column min-vh-100 bg-light">

	
<div id="gui" class="container">
	<div class="row">
		<div class="col align-self-center">
	
	<br />
	<form action="" method="get">
	<div class="text-left blabla help">
		<!-- Introduction text -->
		Here you can see the list of the most used kanji for a specific JDrama, or between all JDrama alltogether.
		<br /> 
		You can also whatever kanji you want by writing it in the text box.
		<br /> 
		Finally, you can click any kanji to show some examples of sentences using this kanji.
		<br /> 
		Have fun!
		<br /> 
	</div>
	<div class="intro">
	<!-- Drama selection dropdown menu -->
	<br />
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
	
		
	Hide following kanji or characters:<br/>
	<textarea cols="120" rows="2" name="filteredUserKanji"><?php if(!empty($filteredUserKanji)){echo $filteredUserKanji;}else{echo "";} ?></textarea>
	<br />


	<input type="submit" value = "Refresh" />
	</form>
		</div>
	</div>
	</div>
	
	
	
	<hr/><br />
	<div id="mainNav" class="container">
	<div class="row">
		<div class="col align-self-center">
	<?php
		displayWordTable();
	?>
		</div>
	<div class="col align-self-top text-left">
	<?php
	GLOBAL $selectedWord;
	
	if(is_null($selectedWord))
	{
		echo "<div class=\"text-center\">No kanji selected.</div>";
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
	if($selectedDrama != 0){
		$query = $query."AND (a.drama_uid = ".$selectedDrama.")";
	}
	else{
		$query = $query."LIMIT 10";
	}
	
	
	$result = mysqli_query($con,$query);
	
	
	$end_time = microtime(true); 
	$execution_time = ($end_time - $start_time); 
	//echo "displayLines took ".$execution_time." seconds to execute the script"; 
	echo "<br/>";
	echo "<br/>";
	while($row = mysqli_fetch_array($result)){
		echo $row['value']."<br/>";
	}
		echo "<br/>";
		echo "Line display limited to 10 results for the moment. <br/>";
	
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
	GLOBAL $filteredUserKanji;
	GLOBAL $wordTable;
	
	if($selectedDrama == -1)
	{
		echo "No drama selected";
		return;
	}

	
	echo "<a href=\"#\" onclick=\"doCsv()\">Export as CSV</a><br/>";
	//echo "Hint: to open in Excel copy-paste the CSV content directly into Excel<br/>";
	echo "<br />";
	

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
	SELECT a.value, b.count, a.kanji_uid, c.jdpt, c.jouyou
	FROM kanji a
	INNER JOIN count b
	ON a.kanji_uid = b.kanji_uid
	INNER JOIN kanji_info c
	ON a.kanji_uid = c.kanji_uid
	AND c.flag IN (1)
	AND a.value NOT IN (".$sqlFilteredUserKanji.")
	WHERE b.drama_uid = ".$selectedDrama."  
	ORDER BY `b`.`count` DESC
	LIMIT 100
	");
	
	
	//do word table
	
	echo "<table class='table table-bordered table-striped table-sm'>
		<tr>
			<th>Word</th>
			<th>Count</th>
			<th>JDPT</th>
			<th>Jōyō </th>
		</tr>";

		$wordTable = "";
		$ctr=0;
		while($row = mysqli_fetch_array($result))
		{
			$ctr=$ctr+1;
			$wordTable = $wordTable.$row['value'].'\t';
			$wordTable = $wordTable.$row['count'].'\t';
			$wordTable = $wordTable.$row['jdpt'].'\t';
			$wordTable = $wordTable.$row['jouyou']."§";
			
			echo "<tr>";
				echo "<td><a href=\"".$currentUrl."&kanji=".$row['kanji_uid']."\">" . $row['value'] . "</a></td>";
				echo "<td>" . $row['count'] . "</td>";
				if(((int)$row['jdpt'])>0) {echo "<td>" . $row['jdpt'] . "</td>";}
				else {echo "<td>-</td>";}
				
				if(((int)$row['jouyou'])>0) {echo "<td>" . $row['jouyou'] . "</td>";}
				else {echo "<td>-</td>";}
			echo "</tr>";
		}
	echo "</table>";
	if($ctr == 100){
		echo "Kanji display limited to maximum 100 results for the moment.";
	}
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
	GLOBAL $selectedDramaName;
	GLOBAL $allDrama;
	GLOBAL $filteredUserKanji;
	
	// find selected drama
	if((isset($_GET["drama"]) == false) || ($_GET["drama"]=="NoSelection"))
	{
		$selectedDrama=-1;
		$selectedDramaName= "Select drama...";
	}
	else
	{
		$selectedDrama=$_GET["drama"];
		$selectedDramaName= $allDrama[$selectedDrama][0]; // - 1 because drama index starts at 1
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

<script>
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});
</script>

<?php
include('footer.php');	
?>

</html>