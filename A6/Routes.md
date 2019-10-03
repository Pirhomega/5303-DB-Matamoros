# THIS IS A TEST IF VS CODE IS CONNECTED TO GITHUB!!!
5303-DB - Dr. Griffin

Assignment 6 - The Worst Flight Planner

9/17/2019

Corbin Matamoros

This program will list SQL queuries executed on a MySQL database
to produce a set of routes a plane could take to get from one
location to the next.


# Traveling through every country worldwide

```php
function getRandomAirportPerCountry()
{
    global $conn;
	$sql = "CREATE TABLE `A6_visitAllCountries` (
			`airport_id` int(6) NOT NULL,
			`name` varchar(64) NOT NULL,
			`city` varchar(64) NOT NULL,
			`country` varchar(64) NOT NULL);";
	$conn->query($sql);
	
	//add a primary key to the table
	$sql = "ALTER TABLE `A6_visitAllCountries` ADD PRIMARY KEY(`airport_id`);";
	$conn->query($sql);
	
    $sql = "SELECT distinct(country) FROM `A6_airports`;";
    $result = $conn->query($sql);
    while($row = mysqli_fetch_assoc($result))
	{
        $sql = "INSERT INTO `A6_visitAllCountries` (SELECT `airport_id`, `name`, `city`, `country` FROM `A6_airports` 
					WHERE `country` = '{$row['country']}' order by RAND() LIMIT 1);";
		$conn->query($sql);
    }
}
```

# Select all the cities and the airports associated with them and calculate the distance

```sql
CREATE TABLE `A6_citiesAndAirports` (
      `airport_name` varchar(100) NOT NULL, 
      `city_name` varchar(100) NOT NULL, 
      `airport_geopoint` POINT, 
      `city_geopoint` POINT
      );
INSERT INTO `A6_citiesAndAirports` 
    (SELECT A6_airports.name, A6_cities.name, A6_airports.geopoint, A6_cities.geopoint FROM A6_airports 
      INNER JOIN A6_cities ON A6_airports.city = A6_cities.name);
ALTER TABLE `A6_citiesAndAirports` ADD `distance_between` FLOAT(16) NULL DEFAULT NULL AFTER `city_geopoint`;
INSERT INTO A6_citiesAndAirports (SELECT A6_citiesAndAirports.airport_name, A6_citiesAndAirports.city_name, A6_citiesAndAirports.airport_geopoint, A6_citiesAndAirports.city_geopoint, st_distance_sphere(A6_citiesAndAirports.city_geopoint,A6_citiesAndAirports.airport_geopoint) from A6_citiesAndAirports 
	INNER JOIN (SELECT *, st_distance_sphere(city_geopoint,airport_geopoint) from A6_citiesAndAirports) AS B ON A6_citiesAndAirports.airport_name = B.airport_name);
DELETE FROM A6_citiesAndAirports WHERE distance_between IS NULL;/*gets rid of the duplicates*/
```
