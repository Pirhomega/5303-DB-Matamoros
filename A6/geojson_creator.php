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

//Randoms grabs 100 countries with an airport
function get100Countries()
{
    global $conn;
    $countries = [];//create an array called countries
    $sql = "SELECT DISTINCT(country) FROM `A6_airports`;";
    $result = $conn->query($sql);
    $i = 0;
    while($row = mysqli_fetch_assoc($result) and $i<100)
    {
        $sql = "SELECT *, ST_X(geopoint) as lon, ST_Y(geopoint) as lat FROM `A6_airports` WHERE `country` = '{$row['country']}' order by RAND() LIMIT 1;";
        $result2 = $conn->query($sql);
        $row2 = mysqli_fetch_assoc($result2);
        $countries[] = $row2;
        $i++;
        //verified works
    }
    return $countries;
}

function createGeoJsonRandAiports()
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
                "title"=>[$airport['name']],
                "description"=>[$airport['city'], $airport['country']],
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
        file_put_contents("allCountries.geojson",json_encode($json,JSON_PRETTY_PRINT));
        //print_r(json_encode($json,JSON_PRETTY_PRINT));
    }
}

function createGeoJson100()
{
    $json = [];
    $json['type'] = 'FeatureCollection';
    $json['features'] = [];

    $airports = get100Countries();

    foreach($airports as $airport)
    {
        $json['features'][] = [ "type" => "Feature",
            "geometry" => [
                "type" => "Point",
                "coordinates" => [$airport['lon']*1.0, $airport['lat']*1.0]
                ],
            "properties" => [
                "title"=>[$airport['name']],
                "description"=>[$airport['city'], $airport['country']],
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
        file_put_contents("hundredCountries.geojson",json_encode($json,JSON_PRETTY_PRINT));
        //print_r(json_encode($json,JSON_PRETTY_PRINT));
    }
}

createGeoJsonRandAiports();
createGeoJson100();