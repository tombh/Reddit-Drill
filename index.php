<?php
if(empty($_GET['depth'])){
  $depth = "_150";
}else{
  $depth = "_" . $_GET['depth'];
}
?>
<html>
	<head>
		<link href='http://fonts.googleapis.com/css?family=Ubuntu:400,500,700' rel='stylesheet' type='text/css'> 
		<link href='web/styles.css' rel='stylesheet' type='text/css'>
        <script language="javascript" type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
		<script language="javascript" type="text/javascript" src="web/thejit.js"></script>
		<script language="javascript" type="text/javascript" src="web/main.js"></script>
	</head>

	<body>
	  Mouse wheel zooms | Drag and drop to pan | Say "activate the teleportal now" to look silly
	  <div id="log"></div>
	  <div id="infovis"></div>
    
	</body>

</html>
