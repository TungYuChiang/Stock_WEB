<?php      
$connection = mysqli_connect("localhost", "root", "fdhg4322", "test");
if(!$connection){
   die("could not connect".mysqli_connect_error());
}
else{
   echo 'connect!!!';
}

$query = "SELECT * FROM test.`2330`";

$ss = mysqli_query($connection, $query);

while($row = mysqli_fetch_array($ss, MYSQLI_ASSOC)){
   echo $row['trend'].'</br>';
}

?> 