import requests, csv
import pandas as pd
from requests_ntlm import HttpNtlmAuth
from datetime import datetime, date

def prepare_data():

	url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
	filename = 'latest.csv'
	filepath = './data/' + filename
	today = date.today()

	data = pd.read_csv(filepath)
	data['dateRep'] = pd.to_datetime(data['dateRep'], format='%d/%m/%Y')
	latest_date = max(data['dateRep'])

	# check for updates
	if (latest_date < today):
		r = requests.get(url, auth=HttpNtlmAuth(':',':'))
		with open(filepath, 'wb') as file:
			file.write(r.content)
		data = pd.read_csv(filepath)
		data['dateRep'] = pd.to_datetime(data['dateRep'], format='%d/%m/%Y')


	df = data.loc[data['countryterritoryCode'].isin(['ITA', 'ESP', 'GBR', 'CHN', 'USA', 'DEU', 'KOR', 'FRA', 'SWE']), :]

	df_piv = df.pivot_table(index='dateRep', columns=['countriesAndTerritories'], values=['cases', 'deaths'])

	df_piv = df_piv.cumsum()

	cumul = pd.melt(df_piv.reset_index(), id_vars='dateRep')
	cumul = cumul.rename(columns={None:'show'})

	return cumul