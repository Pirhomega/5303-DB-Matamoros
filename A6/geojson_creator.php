<?php

error_reporting(-1);
$conn = mysqli_connect('localhost', 'matamoros', 'M20143170!', 'matamoros');
if (mysqli_connect_errno())
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
else
    echo "Connected...\n";

//Grabs a random airport from every country and puts it into an array
function getRandAirport()
{
    global = $conn;
    $countries = [];//create an array called countries
    $sql = "SELECT DISTINCT(country) FROM `A6_airports`;";
    $result = $conn->query($sql);
    while($row = mysqli_fetch_assoc($result))
    {
        $sql = "SELECT `airport_id`, `name`, `city`, `country` FROM `A6_airports` WHERE `country` = '{$row['country']}' order by RAND() LIMIT 1;";
        $result2 = $conn->query($sql);
        $countries[] = $result2;
    }
}