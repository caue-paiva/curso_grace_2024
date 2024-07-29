import requests, os
from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#taxa de homi: id 20
#homi: id 328

base_url:str = "https://www.ipea.gov.br/atlasviolencia/"
fontes:str = "api/v1/fontes"
unidades:str = "api/v1/unidades"
indicadores:str = "api/v1/indicadores"
temas:str = "api/v1/temas"
series:str = "api/v1/valores-series/20/4" #url para taxa de homicídios por município
series_por_tema:str = "api/v1/series/0"
path = base_url + series

response = requests.get(path)
if response.status_code != 200:
      raise RuntimeError(f"Falha na request, erro: {response.status_code}")
response.encoding = 'utf-8'
response_text = response.json()

periods = {}
for dict_ in response_text:
   periods[dict_["periodo"]] = ""

print(periods.keys())
print(len(periods))

@dataclass
class DataPoint():
   valor:float
   ano:int
   cod_munic:int
   uf:str

df = pd.read_csv(os.path.join("info_municipios_ibge.csv"),usecols=["nome_uf","codigo_municipio"])
df.set_index('codigo_municipio', inplace=True)
df.index = df.index.astype(int)


def get_state_from_city_code(df:pd.DataFrame,city_code:int)->str:
   try:
      state:str = df.loc[city_code]["nome_uf"]
      return state
   except Exception as e:
        print(f"Erro durante a busca da UF pelo código do município: {e}")
        return ""

def parse_api_results(api_response:list[dict], city_info_df:pd.DataFrame)->list[DataPoint]:
   parse_dates_to_years = lambda x : x[:x.find("-")]
   dict_to_datapoint =  lambda x: DataPoint(
      valor=float(x["valor"]),
      ano= int(parse_dates_to_years(x["periodo"])),  
      cod_munic=int(x["cod"]),
      uf = get_state_from_city_code(city_info_df,int(x["cod"]))
   )
   return list(map(dict_to_datapoint,api_response))


data_points = parse_api_results(response_text,df)
final_df = pd.DataFrame(data_points)
final_df =final_df.drop(["cod_munic"],axis="columns")
analysis_years = [2000,2010]
final_df = final_df[ final_df["ano"].apply(lambda x: x in analysis_years)]
print(final_df.head())


group_by_state_and_year = final_df.groupby(["uf","ano"])
avg_homicide_rate_per_state_and_years = group_by_state_and_year.aggregate(func="mean")

print(avg_homicide_rate_per_state_and_years.info())
print(avg_homicide_rate_per_state_and_years.head())



# Reset index to plot using Matplotlib
df_reset = avg_homicide_rate_per_state_and_years.reset_index()

df_pivot = df_reset.pivot(index='ano', columns='uf', values='valor')


# Generate distinct colors for each state
colors = plt.cm.get_cmap('tab20', len(df_pivot.columns))

# Plot using Matplotlib with custom bar positions
fig, ax = plt.subplots(figsize=(14, 8))

bar_width = 0.1
bar_positions = np.arange(len(df_pivot.index))

for i, state in enumerate(df_pivot.columns):
    ax.bar(bar_positions + i * bar_width, df_pivot[state], width=bar_width, label=state, color=colors(i))

# Add labels and title
ax.set_xlabel('Ano')
ax.set_ylabel('Valor')
ax.set_title('Valores por Estado e Ano')
ax.set_xticks(bar_positions + bar_width * (len(df_pivot.columns) - 1) / 2)
ax.set_xticklabels(df_pivot.index)
ax.legend(title='UF', bbox_to_anchor=(1.05, 1), loc='upper left')

# Save the plot to a file
plt.savefig('estado_valores_plot.png', bbox_inches='tight')