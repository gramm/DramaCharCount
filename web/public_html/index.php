<!DOCTYPE html>
<html>
<?php
// Declaration of global variables 
$page;
?>
<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="style.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <title>JDramaStuff - Learn Japanese using Vocabulary from Japanese Drama</title>
</head> 

<?php
include('openConnection.php');	
openConnection();
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