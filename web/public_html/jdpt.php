<?php
	if(empty($_GET["article"]))
	{
		$article="intro";
	}
	else
	{
		$article=$_GET["article"];
	}
?>
<br />
<div id="gui" class="container  ">
	<div class="row ">
		<!-- A vertical navbar -->
		<nav class="navbar bg-light navbar-light flex-column col-sm-2 ">
			<!-- Links -->
			<ul class="navbar-nav w-100 ">
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="?page=jdpt.php&article=jdpt-5">Level 5</a>
				</li>
			</ul>
		</nav>
		<div class="col ">
			<?php
			include("jdpt/".$article . ".php");	
			?>
		</div>
	</div>
</div>

<br />

	