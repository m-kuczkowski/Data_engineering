import configparser
import pandas as pd
import requests
from datetime import date


def run_api_etl():
    # Setting connection to the config file, to keep all the credentials safe
    config = configparser.ConfigParser()
    CONFIG_PATH = '/Users/maciej/data_eng/aws/twitter_airflow/cluster.config'
    config.read_file(open(CONFIG_PATH))

    KEY     = config.get('xrapid', 'KEY')
    HOST    = config.get('xrapid', 'HOST')

    url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/"

    headers = {
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": HOST
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
    else:
        print('Connection problems')

    countries = []

    #First two record are headers and total
    n = 2
    max = len(response_json)

    while n < max:
        redefined_response = {"country": response_json[n]['Country'],
                            "country_code": response_json[n]['TwoLetterSymbol'],
                            "total_cases": response_json[n]['TotalCases'],
                            "total_deaths": response_json[n]['TotalDeaths'],
                            "new_cases": response_json[n]['NewCases'],
                            "new_deaths": response_json[n]['NewDeaths'],
                            "cases_per_one_milion_": response_json[n]['TotCases_1M_Pop'],
                            "deaths_per_one_milion": response_json[n]['Deaths_1M_pop'],
                            "refresh": date.today().strftime("%d/%m/%Y")}
        countries.append(redefined_response)
        n += 1

    df = pd.DataFrame(countries)
    df.to_csv('s3://covid-airflow-etl/covid_cases.csv')
