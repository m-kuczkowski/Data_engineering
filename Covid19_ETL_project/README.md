## Description

The main purpose of the project was to create pipeline, that populates data about COVID-19 in AWS Redshift.

## Tech stack

In this project I used:

- Amazon S3 - used to store initial, raw data downloaded from the source. Then after completing transformations final tables were also uploaded to the bucket and then send to the Redshift

- AWS Glue / Crawler -  - used to perform 'jobs' that moved initial data from S3 to Athena, and transformed data from S3 to Redshift

- Amazon Athena - used to perform various checks on data quality, amount of data and structure of tables by generating DDL tables.

- Python Pandas - After analyzing data in Athena and creating data schema, I was able to pull data into Python and transform it using pandas library

- Redshift - Used as cloud-based data warehouse. Transformed tables were uploaded into it, and could be pull from there by analysts

## Data schema

Star schema was used, as it simplifies querying and aggregating data
!()

## Data pipeline

Steps:
- Relational data model,
- Connect to Athena and query data,
- ETL job in python,
- Save results to S3,
- Glue deployment
- Build tables on Redshift,
- Copy data to Redshift

!()

## Files

- etl_project.ipynb -> Covers steps from connecting to Athena to completing data transformations
- s3_to_redshift.py -> Code used in AWS Glue to move transformed data from S3 to Redshift

## Data source

Registry of Open Data on AWS - COVID-19 Data Lake:
https://registry.opendata.aws/aws-covid19-lake/
