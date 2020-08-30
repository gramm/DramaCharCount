<!DOCTYPE html>
<html>
<?php
// Declaration of global variables 
$page;
?>

<?php
	if(empty($_GET["page"]))
	{
		$page="char_count.php";
	}
	else
	{
		$page=$_GET["page"];
	}
?>

<body class="d-flex flex-column min-vh-100 bg-light">

<?php
include('header.php');	
?>

<?php
include($page);	
?>

<?php
include('footer.php');	
?>
</body>

	
</html>