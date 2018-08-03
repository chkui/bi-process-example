# Business Intelligence Process Example 
标签（空格分隔）： superset chkui
An Example of BI.

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
## Check List
### 1.Python environment. 
Superset using Python2.7 in production, but it support 3.x. Suggestting 2.7.x.
### 2.Python Virtual Environment
It is recommended to install Superset inside a virtualenv.Python 3 already ships virtualenv, for Python 2 you need to install it.
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
### Administrator And Run
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
### 4.Download The NOAA Weather Data
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
### Requirements
Create virtual environment, and activating it:
```bash
$ virtualenv venv
$ . venv\bin\activate
```
Download the dependencies:
```bash
$ pip install -r requirements.txt
```
### 



