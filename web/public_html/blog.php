<?php
	if(empty($_GET["article"]))
	{
		$article="404";
	}
	else
	{
		$article=$_GET["article"];
	}
?>
<br />
<div id="gui" class="container  ">
	<div class="row ">
		<nav class="navbar bg-light navbar-light flex-column col-sm-2 ">
			<!-- Links -->
			<ul class="navbar-nav w-100 ">
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button p-2" href="?page=blog.php&article=kanji-frequency-in-every-drama">Complete list of kanji</a>
				</li>
			</ul>
		</nav>
		<div class="col ">
			<?php
			include("blog/".$article . ".php");	
			?>
		</div>
	</div>
</div>

<br />

	