<!DOCTYPE html>
<html lang = "en">
<head>
<meta charset = "UTF-8">
<title> My First Page </title>
<style>
#bgImg{
width:100%;
height:500px;
filter:blur(8px);
-webkit-filter:blur(8px);
}
 
#WebTitle {
font-size:60px;
font-weight:bold; 
position:absolute; 
top:10%; left:50%;
text-align:center;
transform:translate(-50%,-50%);
}

#whiteBorder{
background-color:#ffffff; 
width:65%; 
height:80%; 
position:fixed; 
top:17%;
left:235px; 
box-shadow: 0 0 10px navy;
}
#CarImgBorder{
width:350px; 
height:400px; 
position:absolute; 
top:25px; 
left:20px; 
border: 2px solid #000000;
}

#loadOwnerName {
display:inline-block; 
position:absolute; 
text-align:center;
top:27%; 
left:47%; 
font-weight:bold; 
font-size:40px; 
color:blue;
}

#OwnerInfo{
text-align:left;
font-size:17px; 
font-weight:bold; 
padding-top:20px; 
padding-left:20px; 
font-family:Arial;
color:black;
}

#OwnerInfoVal {
text-align:left;
font-size:17px; 
font-weight:normal; 
padding-top:20px; 
padding-left:30px; 
font-family:Arial; 
color: black;
}
</style>
</head>
<body>

<!-- Background Image of the website-->
<img id="bgImg" src="background.jpg" alt="background picture">

<!-- Website title as absolute position, written over the background image-->
<div id="WebTitle"> Smart Toll Tax System  
</div> 

<?php

$owner = file_get_contents('owner.txt');
//echo "Owner_id:" .$owner;
$servername = "localhost";
$username = "admin";
$password = "qwerty123";
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
//echo "<h1>Connected successfully</h1>";
$sql = $conn->query("USE ToolTax");
$result1 = $conn->query("SELECT owner_name FROM Owner WHERE owner_id='$owner'");
$row = $result1->fetch_assoc(); 
$owner_name=$row['owner_name']; //Here is where the single value is stored.
//echo "<h1>Owner Name:</h1> " .$owner_name;

$result2 = $conn->query("SELECT  vehicle_Brand, vehicle_No, Curr_Credit FROM Owner_Info WHERE owner_id='$owner'");

if ($result2->num_rows > 0) {
    // output data of each row
    while($row2 = $result2->fetch_assoc()) {
        $vehicle_Brand = $row2["vehicle_Brand"];
        $vehicle_No = $row2["vehicle_No"];
        $Curr_Credit = $row2["Curr_Credit"];
    }
}
//echo "Current_Credit:" .$Curr_Credit;
$result3= $conn->query("SELECT Arrival FROM Owner_Bill WHERE owner_id='$owner' AND Cr_Amount='$Curr_Credit'");
$row3=$result3->fetch_assoc();
$Arrival_time = $row3['Arrival'];
//echo "Arrival Time:" .$Arrival_time;
$conn->close();
//echo $vehicle_Brand;
//echo "vehicle_brand:".$vehicle_Brand;
//echo "<div id='WebTitle'>" .$owner_name. "</div>";
echo "<div id='whiteBorder'>";
//echo "<div id='CarImgBorder'> <img src=' . $vehicle_Brand . '.jpg alt='car brand' style='width:350px; height:400px;'> </img></div>";
echo "<div id='CarImgBorder'>";
echo '<img src="' . $vehicle_Brand . '.jpg" alt="car brand" style="width:350px; height:400px;"></div>';
echo "</div>";
echo "<div id='loadOwnerName'>" .$owner_name;
echo "<table> <tr> <td id='OwnerInfo'> Vehicle:</td>";
echo "<td id='OwnerInfoVal'>" .$vehicle_Brand. " </td></tr>";
echo "<tr> <td id='OwnerInfo'>Registration No:</td>"; 
echo "<td id='OwnerInfoVal'>" .$vehicle_No. " </td></tr>";
echo "<tr> <td id='OwnerInfo'>Station No:</td>";
echo "<td id='OwnerInfoVal'>M9-Motorway </td></tr>";
echo "<tr> <td id='OwnerInfo'>Arrival:</td>";
echo "<td id='OwnerInfoVal'>" .$Arrival_time. " </td></tr>";
echo "<tr> <td id='OwnerInfo'>Amount Deducted:</td>";
echo "<td id='OwnerInfoVal'>25.00 RS </td></tr>";
echo "<tr> <td id='OwnerInfo'>Amount In Balance:</td>";
echo "<td id='OwnerInfoVal'>" .$Curr_Credit. " RS </td></tr>";
echo "</table>";
echo "</div></div>"
//echo $owner_name;
//$data = array('vehicle_Brand' => $vehicle_Brand, 'owner_name' => $owner_name);
//$data_json = json_encode($data);
//header('Content-Type: application/json'); 
//echo $data_json;
//echo "<div id='CarImgBorder'>";

?>

<script type="text/javascript" src="http://ajax.googleapis.com/ajax/
libs/jquery/1.3.0/jquery.min.js"></script>

<script type="text/javascript">
//$(document).ready(function()
//{
var auto_refresh = setInterval(
function ()
{
cache_clear();
//$('#whiteBorder').load('index.php');
//$.getJSON("index.php", function(data) {
//			$("#loadImgFrmDatabase").attr('src',data.vehicle_Brand);
//
//$.get('index.php', function(data) { //data is a JS object with two properties, firstDiv and secondDiv
 //       $('#WebTitle').html(data.owner_name);
  //      $('#WhiteBorder').html(data.vehicle_brand);
   // });			});
},3000);
function cache_clear() {
  window.location.reload(true);
  // window.location.reload(); use this if you do not remove cache
}
//});
</script>
</body>
</html>

