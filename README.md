# Data Warehouse Project

## Table of Contents

- [Data Warehouse Project](#data-warehouse-project)
  - [Table of Contents](#table-of-contents)  
  - [Introduction](#introduction)
    - [Objectives](#objectives)  
    - [Star Schema Model](#star-schema-model)  
  - [What this repo contains](#what-this-repo-contains)
    - [Create_Table.py](#create_tablepy)
    - [ETL.py](#etlpy)
    - [Sql_queries.py](#sql_queriespy)
    - [dwg.cfg](#dwgcfg)
    - [Star_schema_model.png](#star_schema_modelpng)
    - [Requirements.txt](#requirementstxt)
  - [Get Started](#get-started)
    - [Prerequisites](#prerequisites)
  - [Project Datasets](#project-datasets)
    - [Song Dataset](#song-dataset)
    - [Log Dataset](#log-dataset)

## Introduction  
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. 
Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. 
You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

### Objectives  

- Apply what I've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. 

- Load data from S3 to staging tables on Redshift 

- Write the SQL statements that create the analytics tables from these staging tables.

### Star Schema Model  
![Star Schema Model](https://github.com/tatianamara/data-warehouse-with-redshift/blob/main/star_schema_model.png)

- The fact table `songplays` stores the records in log data associated with song plays i.e. records with page.

- The dimension table `users` stores the users in the app.

- The dimension table `songs` stores the songs in the music database.

- The dimension table `artists` stores the artists the in music database.

- The dimension table `time` stores the timestamps of records in songplays broken down into specific units.

## What this repo contains
```
create_tables.py
etl.py
sql_queries.py
dwh.cfg
star_schema_model.png
requirements.txt
```

#### Create_Table.py
This script contains the code to create the fact and dimension tables for the star schema in Redshift.

#### ETL.py
This script contains the code to load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.

#### Sql_queries.py
This script contains all the SQL statements, which will be imported into the two other files above.

#### dwg.cfg
Configuration file to add the redshift cluster data and credentials to be accessible by code.

#### Star_schema_model.png
The star schema model used to create the tables for this project.

#### Requirements.txt 
Contains all the dependencies to the project

## Get Started  

`git clone https://github.com/tatianamara/data-warehouse-with-redshift.git`

#### Run the etl.py file to load data from S3 to staging tables on Redshift and create the analytics tables in Redshift  
`python3 etl.py`

### Prerequisites

- Python3 installed (you can download [here](https://www.python.org/downloads/))
- Redshfit cluster connection. Please see detailed instructions in the [AWS documentation](https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html).
- Install requirements with pip3 install -r requirements.txt.
- Populate the dwh.cfg file with the cluster and role data with the necessary permissions.

## Project Datasets  

### Song Dataset  
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. 
The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

File path in s3: `s3://udacity-dend/song_data`  

```
song_data/A/B/C/TRABCEI128F424C983.json  
song_data/A/A/B/TRAABJL12903CDCF1A.json
```

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

### Log Dataset  

The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.
The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in this dataset.

File path in s3: `s3://udacity-dend/log_data`  
Log data json path: `s3://udacity-dend/log_json_path.json`  

```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```





