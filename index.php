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
<!-- 		<script language="javascript" type="text/javascript" src="/ore/drill<?php echo $depth ?>.json"></script> -->
    <script language="javascript" type="text/javascript" >
      <?php echo file_get_contents("ore/drill" . $depth . ".json") ?>
    </script>
		<script language="javascript" type="text/javascript" src="web/thejit.js"></script>
		<script language="javascript" type="text/javascript" src="web/main.js"></script>
	</head>

	<body>
	  <a href="/?depth=400">400</a> | <a href="/?depth=250">250</a> | <a href="/?depth=150">150</a> | <a href="/?depth=20">20_all</a>
	  <div id="log"></div>
	  <div id="infovis"></div>
    
	</body>

</html>
