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
    global $conn;
    $countries = [];//create an array called countries
    $sql = "SELECT DISTINCT(country) FROM `A6_airports`;";
    $result = $conn->query($sql);
    while($row = mysqli_fetch_assoc($result))
    {
        $sql = "SELECT *, ST_X(geopoint) as lon, ST_Y(geopoint) as lat FROM `A6_airports` WHERE `country` = '{$row['country']}' order by RAND() LIMIT 1;";
        $result2 = $conn->query($sql);
        $row2 = mysqli_fetch_assoc($result2);
        $countries[] = $row2;
        //verified works
    }
    return $countries;
}    

function createGeoJSON()
{
    $json = [];
    $json['type'] = 'FeatureCollection';
    $json['features'] = [];

    $airports = getRandAirport();

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