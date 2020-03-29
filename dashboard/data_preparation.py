import requests, csv
import pandas as pd
from requests_ntlm import HttpNtlmAuth
import plotly.express as px
from datetime import date

def get_cumul_plot():
	today = date.today().strftime('%Y-%m-%d')
	url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
	filename = today + '.csv'
	filepath = '../data/' + filename

	# r = requests.get(url, auth=HttpNtlmAuth(':',':'))

	# with open(filepath, 'wb') as file:
	#     file.write(r.content)

	data = pd.read_csv(filepath, encoding='cp1252')
	data['dateRep'] = pd.to_datetime(data['dateRep'], format='%d/%m/%Y')
	# data


	# In[6]:


	df = data.loc[data['countryterritoryCode'].isin(['ITA', 'ESP', 'GBR', 'CHN', 'USA', 'DEU', 'KOR', 'FRA', 'SWE']), :]
	# df


	# In[7]:


	# fig = px.line(df, x='dateRep', y='deaths', color='countryterritoryCode')
	# fig.write_image('plots/plot1.png')
	# fig.show()


	# In[8]:


	df_piv = df.pivot_table(index='dateRep', columns=['countriesAndTerritories'], values=['cases', 'deaths'])
	# df_piv


	# In[9]:


	df_piv = df_piv.cumsum()
	# df_piv


	# In[10]:


	# cumul = pd.melt(df_piv.reset_index(), id_vars='dateRep', value_vars=['cases', 'deaths'])
	cumul = pd.melt(df_piv.reset_index(), id_vars='dateRep')
	cumul = cumul.rename(columns={None:'show'})
	cumul


	# In[14]:


	# px.line(cumul[cumul.show=='deaths'], x='dateRep', y='value', color='countriesAndTerritories')


	# In[12]:


	cumul_align = cumul[cumul['value'] > 60]

	fig = px.line(cumul_align[cumul_align['show'] == 'deaths'], y='value', color='countriesAndTerritories', log_y=False)

	return fig



