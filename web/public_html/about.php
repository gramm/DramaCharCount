<!DOCTYPE html>
<html>
<?php
// Declaration of global variables 
$page = "about-content.php";
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