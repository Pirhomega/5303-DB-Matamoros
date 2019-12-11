<?php
/*	Matamoros, Corbin
	5303-Databases, Dr. Griffin
	Assignment 5 (A5) - Load 4 tables onto personal database
	9/15/2019
	This script will extract air travel data from 4 .dat files and
	create 4 tables for each file.
*/

//turns error-reporting on
error_reporting(-1);

//entering my login details
$host = 'localhost';
$username = 'matamoros';
$password = 'M20143170!';
$database = 'matamoros';

//Connect to database
$conn = mysqli_connect($host, $username, $password, $database);
if (mysqli_connect_errno())
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
else
	echo "Connected . . . \n";

//Everytime this script runs, it erases the 'airlines' table
$sql = "DROP TABLE `A5_airlines`;";

//runs the statement held in the $sql variable
$conn->query($sql);

$sql = "DROP TABLE `A5_airports`;";
$conn->query($sql);
$sql = "DROP TABLE `A5_planes`;";
$conn->query($sql);
$sql = "DROP TABLE `A5_routes`;";
$conn->query($sql);

//--------------------------------------------------------------------
// A5_airlines table
//--------------------------------------------------------------------

//create the SQL statement that will create a table
$sql = "CREATE TABLE `A5_airlines` (
		`airline_id` int(6) NOT NULL,
		`name` varchar(100) NOT NULL,
		`IATA` varchar(32) NOT NULL,
		`ICAO` varchar(32) NOT NULL,
		`country` varchar(64) NOT NULL,
		`active` varchar(1) NOT NULL
		);";
		
$conn->query($sql);
$sql = "ALTER TABLE `A5_airlines` ADD PRIMARY KEY (`airline_id`);";
$conn->query($sql);

$data = file_get_contents('airlines_mod.json');
$data = json_decode($data,true);

foreach($data as $u)
{
	$sql = "INSERT INTO A5_airlines VALUES ('{$u['Airline_ID']}','{$u['Name']}','{$u['IATA']}'
											,'{$u['ICAO']}','{$u['Country']}','{$u['Active']}');";
	$result = $conn->query($sql);
	if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}
}

//--------------------------------------------------------------------
// A5_airports table
//--------------------------------------------------------------------

$sql = "CREATE TABLE `A5_airports` (
		`airport_id` int(6) NOT NULL,
		`name` varchar(100) NOT NULL,
		`city` varchar(64) NOT NULL,
		`country` varchar(64) NOT NULL,
		`IATA` varchar(32) NOT NULL,
		`ICAO` varchar(32) NOT NULL,
		`latitude` float(32) NOT NULL,
		`longitude` float(32) NOT NULL,
		`altitude` int(16) NOT NULL,
		`timezone` float(16) NOT NULL,
		`DST` varchar(1) NOT NULL,
		`tz` varchar(64) NOT NULL
		);";

$conn->query($sql);
$sql = "ALTER TABLE `A5_airports` ADD PRIMARY KEY (`airport_id`);";
$conn->query($sql);

$data = file_get_contents('airports_mod.json');
$data = json_decode($data,true);

foreach($data as $u)
{
	$sql = "INSERT INTO A5_airports VALUES ('{$u['Airport_ID']}','{$u['Name']}','{$u['City']}'
											,'{$u['Country']}','{$u['IATA']}','{$u['ICAO']}'
											,'{$u['Latitude']}','{$u['Longitude']}','{$u['Altitude']}'
											,'{$u['Timezone']}','{$u['DST']}','{$u['TZ']}');";
	$result = $conn->query($sql);
	if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}
}

//--------------------------------------------------------------------
// A5_planes table
//--------------------------------------------------------------------

$sql = "CREATE TABLE `A5_planes` (
		`name` varchar(100) NOT NULL,
		`IATA` varchar(32) NOT NULL,
		`ICAO` varchar(32) NOT NULL
		);";
		
$conn->query($sql);
$sql = "ALTER TABLE `A5_planes` ADD PRIMARY KEY (`name`);";
$conn->query($sql);

$data = file_get_contents('planes_mod.json');
$data = json_decode($data,true);

foreach($data as $u)
{
	$sql = "INSERT INTO A5_planes VALUES ('{$u['Name']}','{$u['IATA']}','{$u['ICAO']}');";
	$result = $conn->query($sql);
	if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}
}

//--------------------------------------------------------------------
// A5_routes table
//--------------------------------------------------------------------

$sql = "CREATE TABLE `A5_routes` (
		`flight` int(16) NOT NULL,
		`airline` varchar(32) NOT NULL,
		`airline_id` int(16) NOT NULL,
		`src_airport` varchar(32) NOT NULL,
		`scr_airport_id` int(32) NOT NULL,
		`dst_airport` varchar(32) NOT NULL,
		`dst_airport_id` int(32) NOT NULL,
		`codeshare` varchar(1) NOT NULL,
		`stops` int(1) NOT NULL,
		`equipment` varchar(64) NOT NULL
		);";
		
$conn->query($sql);
$sql = "ALTER TABLE `A5_routes` ADD PRIMARY KEY (`flight`);";
$conn->query($sql);

$data = file_get_contents('routes_mod.json');
$data = json_decode($data,true);

//$counter will be used to assign a unique flight number to each route
$counter = 0;
foreach($data as $u)
{
	$sql = "INSERT INTO A5_routes VALUES ('{$counter}','{$u['Airline']}','{$u['Airline_ID']}','{$u['Source_AP']}'
											,'{$u['Source_AP_ID']}','{$u['Dest_AP']}','{$u['Dest_AP_ID']}'
											,'{$u['CodeShare']}','{$u['Stops']}','{$u['Equipment']}');";
	$result = $conn->query($sql);
	$counter = $counter + 1;
	/*if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}*/
}
/*INSERT INTO `A5_airlines_and_routes` (SELECT A5_routes.flight, A5_airlines.airline_id, A5_airlines.name, A5_airlines.IATA, A5_airlines.ICAO, A5_airlines.country, A5_airlines.active, A5_routes.src_airport, A5_routes.scr_airport_id, A5_routes.dst_airport, A5_routes.dst_airport_id
FROM A5_routes
INNER JOIN A5_airlines ON A5_airlines.airline_id=A5_routes.airline_id);*/