<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</head> 

<body>

<?php
include('header.php');	
?>

<div id="gui" class="container">
	<div class="row">
		<div class="col align-self-center">
		<h1>About</h1>
		
		<h2>Introduction</h2>
		<p>
		Welcome to JDramaStuff! My name is Maxence Delattre, I am a software engineer with a passion for foreign languages. 
		<br /><br />
		Originally, I developped a small software I called "LearnByDrama" to count and display word occurences by analyzing its Japanese subtitles.
		The idea is that I can filter words I already know in order to find the most used words I don't know yet, and focus on learning these words. 
		By doing this, I avoid spending time on learning words which are almost never used.
		
		<br /><br />
		The software is written in Java, uses Kuromoji as tokenizer, and currently looks like this:
		<img src="img/ss_MyDramaWordList.png" />
		
		<br /><br />
		I thought that maybe someday I could share this software, but nowadays it's all about web applications, python libraries and sharing your stuff on github, and so here we are!
		<h2>Sources</h2>
		The sources of both the website and the python script to parse subtitles are available on GitHub at <a href="https://github.com/gramm/DramaCharCount">https://github.com/gramm/DramaCharCount</a>
		<br />
		The subtitles were all gathered from the JPSubbers website, currently at <a href="http://jpsubbers.xyz/">http://jpsubbers.xyz/</a>
		<!--
		<h2>Tokenization method</h2>
		The python script relies 
		-->
		</p>
		</div>
	</div>
</div>
		

</body>