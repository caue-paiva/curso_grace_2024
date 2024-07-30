import requests, os 
from enum import Enum
from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#taxa de homi: id 20 (id para os dados na API)
#num homi: id 328

BASE_URL:str = "https://www.ipea.gov.br/atlasviolencia/"


class TimeSeries(Enum):
   """
   Enum para enumerar e configurar a extração de cada tipo de dado/série histórica pela API, cada opção do ENUM tem um nome e id
   associado para ser usado na chamada de API e ao salvar os gráficos.
   Para adicionar uma nova série histórica é somente colocar um novo membro com os valores de id e nome
   """
   HOMICIDE_RATE = {
      "name": "taxa de homicídio",
      "id": 20
   }
   FEMALE_HOMICIDE_RATE = {
      "name": "taxa de homicídio de mulheres",
      "id": 52
   }
   SUICIDE_RATE = {
      "name": "taxa de suicídio",
      "id": 323
   }
   FEMALE_SUICIDE_RATE = {
      "name": "taxa de suicídio de mulheres",
      "id": 52
   }


@dataclass
class DataPoint():
   """
   o decorator dataclass gera automaticamente métodos padrões (__init__ entre outros) para a classe e indicada que a
   classe tem o propósito principal de armazenar dados de forma estruturada. Essa classe representa os dados sobre a taxa de homicídio em um município
   com todos os campos que serão necessários para transformar ele em um dataframe para análises nos dados.
   """
   valor:float
   ano:int
   cod_munic:int
   uf:str

def print_available_time_series()->None:
   TIME_SERIES_INFO_URL = "api/v1/series/0" #url para pegar todas as séries no tema de homicídios
   path = BASE_URL + TIME_SERIES_INFO_URL
   response = requests.get(path)
   if response.status_code != 200:
         raise RuntimeError(f"Falha na request, erro: {response.status_code}")
   response.encoding = 'utf-8'
   series_list = response.json()
   
   for series in series_list:
      nome_series: str = series["titulo"]
      id: int = series["id"]
      print(f"Nome Série: {nome_series}, Id: {id}")

def get_api_response(time_series:TimeSeries)->list[dict]:
   id:int = time_series.value["id"]
   SERIES_URL = f"api/v1/valores-series/{id}/4" #20 é o id do tema de taxa de homicídios e 4 é a abrangencia dos dados para cada município
   path = BASE_URL + SERIES_URL
   response = requests.get(path)
   if response.status_code != 200:
         raise RuntimeError(f"Falha na request, erro: {response.status_code}")
   response.encoding = 'utf-8'
   return response.json()

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

def plot_graphs_by_year(df:pd.DataFrame, time_series:TimeSeries)->None:
   df_reset = df.reset_index() #reset no index para plotar os gráficos
   df_pivot = df_reset.pivot(index='ano', columns='uf', values='valor')
   colors = plt.colormaps.get_cmap('tab20')
   series_name:str = time_series.value["name"]

   for year in df_pivot.index: #loop por todos os anos dos dados
      fig, ax = plt.subplots(figsize=(14, 8))

      bar_width = 0.35
      bar_positions = np.arange(len(df_pivot.columns))

      for i, state in enumerate(df_pivot.columns):
         ax.bar(bar_positions[i], df_pivot.loc[year, state], width=bar_width, label=state, color=colors(i))

      ax.set_xlabel('Estado') #cria o gráfico
      ax.set_ylabel(f'{series_name}')
      ax.set_title(f'{series_name} por Estado no ano: {year}')
      ax.set_xticks(bar_positions)
      ax.set_xticklabels(df_pivot.columns, rotation=90)
      ax.legend(title='UF', bbox_to_anchor=(1.05, 1), loc='upper left')

      #salva o gráfico num arquivo
      plt.savefig(f'{series_name}_estados_grafico_{year}.png', bbox_inches='tight')
      plt.close()

def get_grouped_dataframe(list_of_years:list[int], time_series:TimeSeries)->pd.DataFrame:
   df = pd.read_csv(os.path.join("info_municipios_ibge.csv"),usecols=["nome_uf","codigo_municipio"])
   df.set_index('codigo_municipio', inplace=True)
   df.index = df.index.astype(int)

   api_response = get_api_response(time_series)
   data_points = parse_api_results(api_response,df)
   final_df = pd.DataFrame(data_points)
   final_df =final_df.drop(["cod_munic"],axis="columns")
   final_df = final_df[ final_df["ano"].apply(lambda x: x in list_of_years)]

   group_by_state_and_year = final_df.groupby(["uf","ano"])
   return group_by_state_and_year.mean()
 
def __map_num_to_time_series(time_series_num:int)->TimeSeries | None:
   match (time_series_num):
      case 1:
         return TimeSeries.HOMICIDE_RATE
      case 2:
         return TimeSeries.FEMALE_HOMICIDE_RATE
      case 3:
         return TimeSeries.SUICIDE_RATE
      case 4:
         return TimeSeries.FEMALE_SUICIDE_RATE
      
   return None

def get_user_input()->tuple[list[int],TimeSeries]:
   print("Olá, este programa utiliza a API do IPEA para buscar dados sobre a série histórica de taxa de homicídios em estados brasileiros \n")
   OLDEST_YEAR_IN_SERIES: int = 1989
   MOST_RECENT_YEAR_IN_SERIES:int = 2022
   years_list:list[int]
   
   while True:
      anos:str = input("Digite os anos dos dados que serão analizados, cada um com espaço: ")
      years:list[str] = anos.split(" ")

      if not years:
         print("Nenhum ano foi digitado\n")
         continue
      try:
         years_list = list(map(lambda x: int(x),years))
         if any([x < OLDEST_YEAR_IN_SERIES for x in years_list] ):
            print("Ano mais antigo na série histórica é 1989, digite um ano igual o mais recente\n")
            continue

         if any([x > MOST_RECENT_YEAR_IN_SERIES for x in years_list] ):
            print("Ano mais recente na série histórica é 2022, digite um ano igual o mais antigo\n")
            continue

         print("Numeros colocados com sucesso!")
         break
      except:
         continue

   while True:
      data_series: str = input(
      """
      Digite o número do dado que será analisado: 
      1: Taxa de Homicídio \n
      2: Taxa de Homicídios Femininos \n
      3: Taxa de Suicídio \n
      4: Taxa de Suicídio Feminino
      """
      )
      try:
         series_num:int = int(data_series)
         series:TimeSeries|None = __map_num_to_time_series(series_num)
         if series is None:
            raise Exception #falha ao acha a série histórica a partir do número digitado, continua o loop

         return years_list, series #retona uma tupla com os anos da análise e qual o dado que será analizado
      except:
         print("falha ao entrar o dado buscado, tente de novo")

if __name__ == "__main__":
   years_list, time_series = get_user_input()
   avg_homicide_rate_per_state_and_years = get_grouped_dataframe(years_list,time_series)
   print("Gerando gráficos")
   plot_graphs_by_year(avg_homicide_rate_per_state_and_years,time_series)
   print("Gráficos gerados com sucesso")
 
   #print_available_time_series()
 