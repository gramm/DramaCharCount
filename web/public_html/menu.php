
<div id="gui" class="container  ">
	<div class="row ">
		<!-- A vertical navbar -->
		<nav class="navbar bg-light navbar-light flex-column col-sm-2 ">
			<!-- Links -->
			<ul class="navbar-nav w-100 ">
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="intro.php">Introduction</a>
				</li>
				<br/>
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="jdpt-5.php">Level 5</a>
				</li>
				<br/>
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="jdpt-4.php">Level 4</a>
				</li>
				<br/>
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="jdpt-3.php">Level 3</a>
				</li>
				<br/>
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="jdpt-2.php">Level 2</a>
				</li>
				<br/>
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="jdpt-1.php">Level 1</a>
				</li>
				<br/>
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="jdpt-0.php">Not in JDPT</a>
				</li>
				<br/>
				<li class="nav-item text-center ">
					<a class="nav-link text-warning bg-secondary menu-button" href="jdpt-all.php">All kanji</a>
				</li>
				<br/>
			</ul>
		</nav>
		<div class="col ">
			<?php
			include($page);	
			?>
		</div>
	</div>
</div>
