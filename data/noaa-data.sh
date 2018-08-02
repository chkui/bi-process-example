# Download cvs file from the NOAA website.
echo download 2015 weather data
curl -O ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/2015.csv.gz

echo download the meta data
curl -O ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt

echo unzip the 2015.csv.gz
gunzip 2015.csv.gz
