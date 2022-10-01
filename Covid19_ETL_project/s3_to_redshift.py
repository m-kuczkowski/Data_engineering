#imports
import boto3
import pandas as pd
from io import StringIO
import configparser
import time
import redshift_connector

# Setting connection to the config file, to keep all the credentials safe
config = configparser.ConfigParser()
CONFIG_PATH = '/Users/maciej/data_eng/aws/covid_project/cluster.config'
config.read_file(open(CONFIG_PATH))

conf_aws = config['AWS']
conf_s3 = config['S3']
conf_dwh = config['DWH']
conf_red = config['REDSHIFT']

conn = redshift_connector.connect(
    host = conf_red['HOST'],
    database = conf_red['DATABASE'],
    user = conf_red['USER'],
    password = conf_red['PASSWORD']
)

conn.autocommit = True

cursor = redshift_connector.Cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE "dimDate" (
    "index" INTEGER,
    "fips" INTEGER,
    "date" TIMESTAMP,
    "year" INTEGER,
    "month" INTEGER,
    "day" INTEGER
    )
    ''')

cursor.execute('''
    CREATE TABLE "dimHospital" (
    "index" INTEGER,
    "fips" REAL,
    "state_name" TEXT,
    "longtitude" REAL,
    "latitude" REAL,
    "hq_address" TEXT,
    "hospital_name" TEXT,
    "hospital_type" TEXT,
    "hq_city" TEXT,
    "hq_state" TEXT
)
''')

cursor.execute(
    '''
    CREATE TABLE "dimRegion" (
    "index" INTEGER,
    "fips" REAL,
    "province_state" TEXT,
    "country_region" TEXT,
    "latitude" REAL,
    "longitude" REAL,
    "county" TEXT,
    "state" TEXT
)
    '''
)

cursor.execute(
    '''
    CREATE TABLE "factCovid" (
    "index" INTEGER,
    "fips" REAL,
    "state" TEXT,
    "region" TEXT,
    "confirmed" REAL,
    "deaths" REAL,
    "recovered" REAL,
    "active" REAL,
    "date" INTEGER,
    "positive" REAL,
    "negative" REAL,
    "hospitalizedcurrently" REAL,
    "hospitalized" REAL,
    "hospitalizedcumulative" REAL
)
    '''
)

cursor.execute(
    """
    copy dimDate from 's3://maciejs-bucket/pd-tables-output/dimDate.csv'
    credentials 'aws_iam_role=...'
    delimiter ','
    region 'eu-central-1'
    IGNOREHEADER 1
    """
)

cursor.execute(
    """
    copy dimHospital from 's3://maciejs-bucket/pd-tables-output/dimHospital.csv'
    credentials 'aws_iam_role=...'
    delimiter ','
    region 'eu-central-1'
    IGNOREHEADER 1
    """
)

cursor.execute(
    """
    copy dimRegion from 's3://maciejs-bucket/pd-tables-output/dimRegion.csv'
    credentials 'aws_iam_role=...'
    delimiter ','
    region 'eu-central-1'
    IGNOREHEADER 1
    """
)