<?php
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "sensorData";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$type = $_POST['type'];
$x = $_POST['x'];
$y = $_POST['y'];
$z = $_POST['z'];
$time = $_POST['time'];
$time_real = $_POST['time_real'];

$sql = "INSERT INTO sensor0 (type, x, y, z, time, time_real)
VALUES ('$type', '$x', '$y', '$z', '$time', '$time_real')";

if (mysqli_query($conn, $sql)) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

mysqli_close($conn);
?>
