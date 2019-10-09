5303-DB - Dr. Griffin

Assignment 6 - The Worst Flight Planner

9/17/2019

Corbin Matamoros

This program will list SQL queuries executed on a MySQL database
to produce a set of routes a plane could take to get from one
location to the next.


# Traveling through every country worldwide

```php
<?php

error_reporting(-1);
$conn = mysqli_connect('****', '****', '****', '****');
if (mysqli_connect_errno())
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
else
    echo "Connected...\n";

//Grabs a random airport from every country and puts it into an array
function getRandAirport()
{
    global $conn;
    $countries = [];//create an array called countries
    $sql = "SELECT DISTINCT(country) FROM `A6_airports`;";//selects every distinct country in the table...duh
    $result = $conn->query($sql);
    while($row = mysqli_fetch_assoc($result))
    {
        //will grab a row from the distinct countries query result earlier and select an airport at random from a list of all airports in that country
        $sql = "SELECT *, ST_X(geopoint) as lon, ST_Y(geopoint) as lat FROM `A6_airports` WHERE `country` = '{$row['country']}' order by RAND() LIMIT 1;";
        $result2 = $conn->query($sql);
        $row2 = mysqli_fetch_assoc($result2);
        $countries[] = $row2;//appends the selected airport's row onto the array 'countries'
    }
    return $countries;
}    

function createGeoJSON()
{
    $json = [];//creates an array
    $json['type'] = 'FeatureCollection';//sets the type of array
    $json['features'] = [];//creates an array within the element 'features'

    $airports = getRandAirport();

    //this for loop will create each feature for the geojson file, where
    //each feature is a country
    foreach($airports as $airport)
    {
        $json['features'][] = [ "type" => "Feature",
            "geometry" => [
                "type" => "Point",
                "coordinates" => [$airport['lon']*1.0, $airport['lat']*1.0]
                ],
            "properties" => [
                "title"=>"Starting Point",
                "description"=>"Somewhere in the world",
                "marker-size"=>"medium",
                "marker-symbol"=>"airport",
                "marker-color"=>"#f00",
                "stroke"=>"#555555",
                "stroke-opacity"=>1,
                "stroke-width"=>2,
                "fill"=>"#555555",
                "fill-opacity"=>0.5
                ]
            ];
        file_put_contents("output.txt",json_encode($json,JSON_PRETTY_PRINT));
        //print_r(json_encode($json,JSON_PRETTY_PRINT));
    }
}

createGeoJSON();
```

# Choosing 100 random countries to travel to

```php
/*
    This brief program will select 100 random countries with an airport and output
    a .geojson file with those locations.
*/

//Randoms grabs 100 countries with an airport
//This function is exactly the same as the function that selects every country
//once, except we will limit the number of coutries to 100
function get100Countries()
{
    global $conn;
    $countries = [];//create an array called countries
    $sql = "SELECT DISTINCT(country) FROM `A6_airports`;";
    $result = $conn->query($sql);
    $i = 0;//will be used to count to 100
    while($row = mysqli_fetch_assoc($result) and $i<100)
    {
        $sql = "SELECT *, ST_X(geopoint) as lon, ST_Y(geopoint) as lat FROM `A6_airports` WHERE `country` = '{$row['country']}' order by RAND() LIMIT 1;";
        $result2 = $conn->query($sql);
        $row2 = mysqli_fetch_assoc($result2);
        $countries[] = $row2;
        $i++;
    }
    return $countries;
}
function createGeoJson100()
{
    $json = [];//creates an array
    $json['type'] = 'FeatureCollection';//sets the type of array
    $json['features'] = [];//creates an array within the element 'features'

    $airports = get100Countries();//call function that will select 100 countries

    //this for loop will create each feature for the geojson file, where
    //each feature is a country
    foreach($airports as $airport)
    {
        $json['features'][] = [ "type" => "Feature",
            "geometry" => [
                "type" => "Point",
                "coordinates" => [$airport['lon']*1.0, $airport['lat']*1.0]
                ],
            "properties" => [
                "title"=>"Starting Point",
                "description"=>"Somewhere in the world",
                "marker-size"=>"medium",
                "marker-symbol"=>"airport",
                "marker-color"=>"#f00",
                "stroke"=>"#555555",
                "stroke-opacity"=>1,
                "stroke-width"=>2,
                "fill"=>"#555555",
                "fill-opacity"=>0.5
                ]
            ];
        file_put_contents("output100Countries.txt",json_encode($json,JSON_PRETTY_PRINT));
        //print_r(json_encode($json,JSON_PRETTY_PRINT));
    }
}
```

# Select all the cities and the airports associated with them and calculate the distance

```sql
/*  
    This program will bring two databases together - one of cities worldwide, and the other, airports worldwide.
    It will inner join these two tables and create a new database of cities and the closest airport to them.
    There will also be a column with the distance between the two.
*/

--creates the table we will populate
CREATE TABLE `A6_citiesAndAirports` (
      `airport_name` varchar(100) NOT NULL, 
      `city_name` varchar(100) NOT NULL, 
      `airport_geopoint` POINT, 
      `city_geopoint` POINT
      );

--inner joins two tables to form a large table of airports, their cities, and both's geopoints
INSERT INTO `A6_citiesAndAirports` 
    (SELECT A6_airports.name, A6_cities.name, A6_airports.geopoint, A6_cities.geopoint FROM A6_airports 
      INNER JOIN A6_cities ON A6_airports.city = A6_cities.name);

--adds a column called 'distance_between' to the table
ALTER TABLE `A6_citiesAndAirports` ADD `distance_between` FLOAT(16) NULL DEFAULT NULL AFTER `city_geopoint`;

--inner joins table above - plus the distance between an airport and its city - with the same table - plus the distance (ie, an inner join of identical tables)
--and inserts the result in the same table.
INSERT INTO A6_citiesAndAirports (SELECT A6_citiesAndAirports.airport_name, A6_citiesAndAirports.city_name, A6_citiesAndAirports.airport_geopoint, A6_citiesAndAirports.city_geopoint, st_distance_sphere(A6_citiesAndAirports.city_geopoint,A6_citiesAndAirports.airport_geopoint) from A6_citiesAndAirports 
	INNER JOIN (SELECT *, st_distance_sphere(city_geopoint,airport_geopoint) from A6_citiesAndAirports) AS B ON A6_citiesAndAirports.airport_name = B.airport_name);

--rids final table from duplicates
DELETE FROM A6_citiesAndAirports WHERE distance_between IS NULL;
```
