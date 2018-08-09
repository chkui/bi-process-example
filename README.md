# Business Intelligence Process Example 
An example of Business Intelligence From Origin Data to Dashboard

---
## Files/Folder Description
### ${project}/data/
NOAA daily weather data. 
There is a shell script who names `noaa-data.sh`.It will download the weather data from the NOAA FTP server.After of all, running this script.
### ${project}/src/
Python code. Process the data using the Pandas data analysis Python library.
### ${project}/IngestData.iptnb
Jupyter notebook script.
### ${project}/requirements.txt
Python dependence.

---
## Download And Install
### 1.Python environment. 
Superset using Python2.7 in production, but it support 3.x. Suggestting 2.7.x.
### 2.Python Virtual Environment
It is recommended to install Superset inside a virtualenv.Python 3 already ships virtualenv, for Python 2 need to install it.
```bash
$ sudo pip install virtualenv
```
Use the command to create the virtual folder any where:
```bash
$ virtualenv venv
```
Then execute this virtual environment:
```bash
#source venv\bin\activate
$ . venv\bin\activate
```
> To exit a virtualenv just type `deactivate`.

### 3.Install Superset
Modify the default pip server for china:
```
pip install -ihttp://mirrors.aliyun.com/pypi/simple/ flask。
```

Put all the chances on your side by getting the very latest pip and setuptools libraries.:
```bash
$ pip install --upgrade setuptools pip
```
Install superset:
```bash
$ pip install superset
```
### 4.Administrator And Run
Create administrator with Flask-AppBuilder.
```bash
# Create an admin user (you will be prompted to set username, first and last name before setting a password)
fabmanager create-admin --app superset

# Initialize the database
superset db upgrade

# Load some data to play with
superset load_examples

# Create default roles and permissions
superset init

# To start a development web server on port 8088, use -p to bind to another port
superset runserver -d
```
Supperset Already install!
### 5.Download The NOAA Weather Data
Excute the `#Root/data/noaa-data.sh` script to download and unzip NOAA weather data from the FTP server. 
Or use cURL command directly:
```bash
$ curl -O ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/2015.csv.gz
$ curl -O ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt
```
After downloading the data, gunzip it:
```bash
gunzip 2015.csv.gz
```
### 6.Python Requirements
Create virtual environment, and activating it:
```bash
virtualenv venv
#activating
. venv\bin\activate
```
Download the dependencies:
```bash
$ pip install -r requirements.txt
```
### 7.Setting up the PostgreSQL database 
Install PostgreSQL(pgsql) 10:
```bash
$ sudo apt-get install postgresql-10 
```
Then an account names postgres has bean created. 

Modify account password:
```bash
$ sudo -u postgres passwd
```

Login Database:
```bash
$ sudo -u postgres psql
```
Modify the Database password:
```
ALTER USER postgres WITH PASSWORD '123456';
```
### 8.Install jupyter
```bash
$ python -m pip install --upgrade pip
python -m pip install jupyter
```
```bash
$ jupyter nodebook
```
### 9.Examining Download Data
```
$ wc -l 2015.csv
```
```
$ cut -d, -f1 2015.csv | sort | uniq | wc -l
```
## Processing

### 1.Loading the data into PostgreSQL
Loading the download data——`${project}/data/2015.csv ghcnd-stations.txt)` into PostgreSQL Data base.
#### jupyter notebook
We can use jupter noteboot to execute python code: 
```
$ jupyter notebook IngestData.ipynb
```
But it exists some problems.
#### Execute Python
```bash 
$ python src/execute.py
```
This will take some time to complete.After of all, the data will be loaded into pgSQL, and three table will be created —— `weather_data`,`station_metadata` and `weather_types`.
### Denormalizing data
Execute blow SQL:
```sql
CREATE TABLE weather_data_denormalized AS 
    SELECT wd.station_identifier, 
           wd.measurement_date, 
           wd.measurement_type, 
           wt.weather_description, 
           wd.measurement_flag, 
           sm.latitude, 
           sm.longitude, 
           sm.elevation 
    FROM weather_data wd 
    JOIN station_metadata sm 
        ON wd.station_identifier = sm.station_id 
    JOIN weather_types wt 
        ON wd.measurement_type = wt.weather_type;
```
### Create Indexs
```sql
CREATE INDEX date_index ON weather_data_denormalized (measurement_date);
CREATE INDEX type_index ON weather_data_denormalized (measurement_type);
CREATE INDEX description_index ON weather_data_denormalized (weather_description);
CREATE INDEX flag_index ON weather_data_denormalized (measurement_flag);
CREATE INDEX elevation_index ON weather_data_denormalized (elevation);
```
## Superset Dashboard
Then using Superset to create your dashboard:
>http://superset.apache.org/tutorial.html

### Set Database
1. Sources->Database.
2. Input the SQLAlchemy URI string.
3. Then "Test Connection". 

### Set Table
1. Sources->Tables.
2. Select new Database.
3. Input the table name: weather_data_denormalized.

### Exploring Data
1. Sources->Tables. Simply click on the table name of the list of tables.

##Superset Development
### Front&&Chart
It's developed by React where '${install_path}/superset/static/assets'.
#### Folder
1. branding: Logo.
1. images: all of the images which supports superset web.
1. spec: Config file.
1. src: develop file.
1. stylesheets: style file, css,less e.g.
1. verdor: Third part lib implements with React.
#### add charts
- Add path:  ${superset_root}/static/assets/src/visualizations
- add custom charts as a React Component who includes .jsx/js and css part.such blow:
```javascript
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import { XYChart, AreaSeries, CrossHair, LinearGradient } from '@data-ui/xy-chart';

class Costom extends React.Component{
    //TODO
}
```
- Add costom component in index.js (${superset_root}/static/assets/src/visualizations):
- Add costom charts in ${superset_root}/static/assets/src/explore/visTypes.jsx for adding data options in slice.
- Add images in ${superset_root}/static/assets/images/viz_thumbnails/

> About front development details see https://github.com/chkui/superset(Forked from ryoha13/superset).
