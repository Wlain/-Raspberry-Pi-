<?php
$action=$_POST["action"];
$cmd=$_POST["cmd"];
if($action=="set-linux-cmd"){ 
	$myfile=fopen("linuxcmd.txt","w") or die("unable to open file!");
	fwrite($myfile,$cmd); 
	$str=file_get_contents("linuxcmd.txt");
	echo($str);	
}
?>