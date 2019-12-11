<?php
/*	Matamoros, Corbin
	5303-Databases, Dr. Griffin
	Assignment 4 (A4) - Load 4 tables onto personal database
	9/11/2019
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
$sql = "DROP TABLE `A4_airlines`;";

//runs the statement held in the $sql variable
$conn->query($sql);

$sql = "DROP TABLE `A4_airports`;";
$conn->query($sql);
$sql = "DROP TABLE `A4_planes`;";
$conn->query($sql);
$sql = "DROP TABLE `A4_routes`;";
$conn->query($sql);

//--------------------------------------------------------------------
// A4_airlines table
//--------------------------------------------------------------------

//create the SQL statement that will create a table
$sql = "CREATE TABLE `A4_airlines` (
		`airline id` int(6) NOT NULL,
		`name` varchar(100) NOT NULL,
		`alias` varchar(100) NOT NULL,
		`IATA` varchar(32) NOT NULL,
		`ICAO` varchar(32) NOT NULL,
		`callsign` varchar(64) NOT NULL,
		`country` varchar(64) NOT NULL,
		`active` varchar(1) NOT NULL
		);";
		
$conn->query($sql);
$sql = "ALTER TABLE `A4_airlines` ADD PRIMARY KEY (`airline id`);";
$conn->query($sql);

$data = file_get_contents('airlines.json');
$data = json_decode($data,true);

foreach($data as $u)
{
	$sql = "INSERT INTO A4_airlines VALUES ('{$u['Airline_ID']}','{$u['Name']}','{$u['Alias']}'
											,'{$u['IATA']}','{$u['ICAO']}','{$u['Callsign']}'
											,'{$u['Country']}','{$u['Active']}');";
	$result = $conn->query($sql);
	if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}
}

//--------------------------------------------------------------------
// A4_airports table
//--------------------------------------------------------------------

$sql = "CREATE TABLE `A4_airports` (
		`airport id` int(6) NOT NULL,
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
		`tz` varchar(64) NOT NULL,
		`type` varchar(32) NOT NULL,
		`source` varchar(11) NOT NULL
		);";

$conn->query($sql);
$sql = "ALTER TABLE `A4_airports` ADD PRIMARY KEY (`airport id`);";
$conn->query($sql);

$data = file_get_contents('airports.json');
$data = json_decode($data,true);

foreach($data as $u)
{
	$sql = "INSERT INTO A4_airports VALUES ('{$u['Airport_ID']}','{$u['Name']}','{$u['City']}'
											,'{$u['Country']}','{$u['IATA']}','{$u['ICAO']}'
											,'{$u['Latitude']}','{$u['Longitude']}','{$u['Altitude']}'
											,'{$u['Timezone']}','{$u['DST']}','{$u['TZ']}','{$u[' Type']}'
											,'{$u['Source']}');";
	$result = $conn->query($sql);
	if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}
}

//--------------------------------------------------------------------
// A4_planes table
//--------------------------------------------------------------------

$sql = "CREATE TABLE `A4_planes` (
		`name` varchar(100) NOT NULL,
		`IATA` varchar(32) NOT NULL,
		`ICAO` varchar(32) NOT NULL
		);";
		
$conn->query($sql);
$sql = "ALTER TABLE `A4_planes` ADD PRIMARY KEY (`name`);";
$conn->query($sql);

$data = file_get_contents('planes.json');
$data = json_decode($data,true);

foreach($data as $u)
{
	$sql = "INSERT INTO A4_planes VALUES ('{$u['Name']}','{$u['IATA']}','{$u['ICAO']}');";
	$result = $conn->query($sql);
	if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}
}

//--------------------------------------------------------------------
// A4_routes table
//--------------------------------------------------------------------

$sql = "CREATE TABLE `A4_routes` (
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

$data = file_get_contents('routes.json');
$data = json_decode($data,true);

foreach($data as $u)
{
	$sql = "INSERT INTO A4_routes VALUES ('{$u['Airline']}','{$u['Airline_ID']}','{$u['Source_AP']}'
											,'{$u['Source_AP_ID']}','{$u['Dest_AP']}','{$u['Dest_AP_ID']}'
											,'{$u['CodeShare']}','{$u['Stops']}','{$u['Equipment']}');";
	$result = $conn->query($sql);
	if(!$result)//just in case something doesn't work
	{
		echo "Error message: ". $conn->error."\n";
	}
}
