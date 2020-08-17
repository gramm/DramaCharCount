<?php
	if(empty($_GET["blog"]))
	{
		$page="404.php";
	}
	else
	{
		$page=$_GET["blog"];
	}
?>
<br />
<div id="gui" class="container  ">
	<div class="row ">
		<!-- A vertical navbar -->
		<nav class="navbar bg-light navbar-light ">
			<!-- Links -->
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="nav-link" href="#">Link 1</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="#">Link 2</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="#">Link 3</a>
				</li>
			</ul>
		</nav>
		<div class="col ">
			<?php
			include($page);	
			?>
		</div>
	</div>
</div>

<br />

	