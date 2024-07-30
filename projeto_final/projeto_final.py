import requests, os 
from enum import Enum
from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_URL:str = "https://www.ipea.gov.br/atlasviolencia/" #url básico da API

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
   o decorator dataclass gera automaticamente métodos padrões (__init__ entre outros) para a classe e indica que a
   classe tem o propósito principal de armazenar dados de forma estruturada. Essa classe representa os dados sobre uma série histórica em um município.
   com todos os campos que serão necessários para transformar ele em um dataframe para análises nos dados.
   """
   valor:float
   ano:int
   cod_munic:int
   uf:str


def __get_api_response(time_series:TimeSeries)->list[dict]:
   """
   Faz uma request à API do IPEA atlas da violência dado um série histórica passada como argumento.

   Args:
      time_series (TimeSeries): Objeto que dita qual dado/série histórica será buscado na API
   
   Return:
      (list[dict]): retorno da API, consiste em uma lista de dicionários, cada dict tem as chaves: (id,periodo,valor,cod)
   """
   
   id:int = time_series.value["id"]
   SERIES_URL = f"api/v1/valores-series/{id}/4" #20 é o id do tema de taxa de homicídios e 4 é a abrangencia dos dados para cada município
   path = BASE_URL + SERIES_URL
   response = requests.get(path)
   if response.status_code != 200:
         raise RuntimeError(f"Falha na request, erro: {response.status_code}")
   response.encoding = 'utf-8'
   return response.json()

def __get_state_from_city_code(df:pd.DataFrame,city_code:int)->str:
   """
   Dado um df com os estados associados a cada código de município (df que veio do CSV do IBGE sobre municípios),
   e um código de cidade, retorna o nome do estado desse município.

   Args:
      df (pd.DataFrame): df do pandas com os nomes dos estados associados a cada código do município de um dado
      city_code (int): código do município
   
   Return:
      (str): nome do estado em que o município do código se localiza 
   """
   try:
      state:str = df.loc[city_code]["nome_uf"] #acessa o a linha e dps a coluna no dataframe
      return state
   except Exception as e:
        print(f"Erro durante a busca da UF pelo código do município: {e}")
        return ""

def __parse_api_results(api_response:list[dict], city_info_df:pd.DataFrame)->list[DataPoint]:
   """
   Faz um parsing no resultado da API do IPEA e retorna uma lista de objetos DataPoint

   Args:
      api_response (list[dict]): resposta da API do IPEA
      city_info_df (pd.DataFrame): df do pandas com os nomes dos estados associados a cada código do município de um dado

   Return:
      (list[DataPoint]): lista de objetos DataPoint, cada um contendo um dado, de um ano em uma cidade (com o nome do estado tbm)
   """
   
   parse_dates_to_years = lambda x : x[:x.find("-")] #função que transforma a string YYYY-MM-DD em uma string YYYY
   dict_to_datapoint =  lambda x: DataPoint( #função transforma um dict que veio da API em um objeto DataPoint
      valor=float(x["valor"]),
      ano= int(parse_dates_to_years(x["periodo"])),  
      cod_munic=int(x["cod"]),
      uf = __get_state_from_city_code(city_info_df,int(x["cod"]))
   )
   return list(map(dict_to_datapoint,api_response)) #aplica a função dict_to_datapoint em cada elemento da lista

def __map_num_to_time_series(time_series_num:int)->TimeSeries | None:
   """
   Dado um inteiro, mapea esse inteiro para um objeto do enum TimeSeries.
   
   Args:
      time_series_num (int): número que representa o dado/série histórica.

   Return:
      (TimeSeries | None): Retorna um objeto TimeSeries se achar o número correspondente, senão retorna None.
   """
   match (time_series_num): #associa cada número a um objeto TimeSeries
      case 1:
         return TimeSeries.HOMICIDE_RATE
      case 2:
         return TimeSeries.FEMALE_HOMICIDE_RATE
      case 3:
         return TimeSeries.SUICIDE_RATE
      case 4:
         return TimeSeries.FEMALE_SUICIDE_RATE
      
   return None

def print_available_time_series()->None:
   """
   Printa no terminal todas as séries históricas da API IPEA Atlas da Violência e seus IDs correspondentes.
   Essa lista é apenas para séries no tema geral de Violência, esses temas são ditados pela API e pelo sistema do 
   IPEA

   Args:
      (None)
   Return:
      (None)
   """
   
   TIME_SERIES_INFO_URL = "api/v1/series/0" #url para pegar todas as séries no tema de homicídios
   path = BASE_URL + TIME_SERIES_INFO_URL
   response = requests.get(path)
   if response.status_code != 200:
         raise RuntimeError(f"Falha na request, erro: {response.status_code}")
   response.encoding = 'utf-8'
   series_list = response.json()
   
   for series in series_list: #loop por cada série histórica 
      nome_series: str = series["titulo"]
      id: int = series["id"]
      print(f"Nome Série: {nome_series}, Id: {id}") #print nas informações

def plot_graphs_by_year(df:pd.DataFrame, time_series:TimeSeries)->None:
   """
   Dado um df agrupado por ano e estado e o dado/série histórica que será extraido(a), gera gráficos (cada um para um ano) dos dados
   presentes no df.

   Args:
      df (pd.DataFrame): df do pandas agrupado por ano e estado
      time_series (TimeSeries): objeto que representa a qual série histórica os gráficos pertencem
   
   Return:
      (None): Nenhum retorno
   """
  
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
   """
   Dado uma lista de anos e a série histórica a ser analisada, faz a request API e retorna um DF do pandas agrupado (group_by) pelo estado e ano
   e com uma coluna representando a média dos valores para cada combinação de colunas do group_by.

   Args:
      list_of_years (list[int]): lista de anos nos dados que serão analizados
      time_series (TimeSeries): objeto time series que dita qual dado/série histórica será analizada
   
   Return:
      (pd.Dataframe): Dataframe do pandas agrupado por estado e ano e com a média dos valores
   """
   CSV_CITY_INFO_PATH = "info_municipios_ibge.csv" #arquivo csv extraido do IBGE com informações sobre cidades do Brasil
   
   df = pd.read_csv(os.path.join(CSV_CITY_INFO_PATH),usecols=["nome_uf","codigo_municipio"]) #le o csv das informações do municípoo
   df.set_index('codigo_municipio', inplace=True) # código do município vira o index
   df.index = df.index.astype(int)

   api_response:list[dict] = __get_api_response(time_series) #chama a api
   data_points:list[DataPoint] = __parse_api_results(api_response,df) #processa o resultado
   final_df = pd.DataFrame(data_points) #cria um df com a lista de datapoints com a coluna de estado
   
   final_df =final_df.drop(["cod_munic"],axis="columns") #coluna de codigo do município não é mais necessária
   final_df = final_df[ final_df["ano"].apply(lambda x: x in list_of_years)] #filtra o df para ter apenas os anos especificados

   group_by_state_and_year = final_df.groupby(["uf","ano"]) #faz um groupby nas colunas de uf (estado) e ano
   return group_by_state_and_year.mean() #calcula a média da coluna de valores de cada agrupamento

def get_user_input()->tuple[list[int],TimeSeries]:
   """
   Lê o input do usuário sobre o dado que será analisado da API "Ipea Mapa da violência" e qual os anos que serão
   analisados.
   
   Args:
      (None)
      
   Return:
      (tuple[list[int],TimeSeries]): uma tupla com a lista dos anos a serem analizados e um objeto TimeSeries, que representa o dado a ser analizado
   """
   
   print("Olá, este programa utiliza a API do IPEA para buscar dados sobre a série histórica de taxa de homicídios em estados brasileiros \n")
   OLDEST_YEAR_IN_SERIES: int = 1989 #constantes para os anos de início e fim das séries históricas
   MOST_RECENT_YEAR_IN_SERIES:int = 2022
   years_list:list[int]
   
   while True:
      anos:str = input("Digite os anos dos dados que serão analizados, cada um com espaço: ")
      years:list[str] = anos.split(" ") #separa o input no espaço

      if not years:
         print("Nenhum ano foi digitado\n")
         continue
      try:
         years_list = list(map(lambda x: int(x),years)) #transforma strings de números em ints
         if any([x < OLDEST_YEAR_IN_SERIES for x in years_list] ):
            print("Ano mais antigo na série histórica é 1989, digite um ano igual o mais recente\n")
            continue

         if any([x > MOST_RECENT_YEAR_IN_SERIES for x in years_list] ):
            print("Ano mais recente na série histórica é 2022, digite um ano igual o mais antigo\n")
            continue

         print("Numeros colocados com sucesso!")
         break
      except:
         continue #continua loop

   while True:
      data_series: str = input( #pega input do usuário sobre qual dado será analisado
      """
      Digite o número do dado que será analisado: 
      1: Taxa de Homicídio \n
      2: Taxa de Homicídios Femininos \n
      3: Taxa de Suicídio \n
      4: Taxa de Suicídio Feminino
      """
      )
      try:
         series_num:int = int(data_series) #transforma string em int
         series:TimeSeries|None = __map_num_to_time_series(series_num) #acha qual objeto do Enum TimeSeries corresponde ao número
         if series is None:
            raise Exception #falha ao achar a série histórica a partir do número digitado, continua o loop

         return years_list, series #retona uma tupla com os anos da análise e qual o dado que será analizado
      except:
         print("falha ao entrar o dado buscado, tente de novo") #continua loop

if __name__ == "__main__":
   years_list, time_series = get_user_input() #pega input do usuário
   avg_homicide_rate_per_state_and_years = get_grouped_dataframe(years_list,time_series) #gera dataframe com os dados da API
   print("Gerando gráficos")
   plot_graphs_by_year(avg_homicide_rate_per_state_and_years,time_series) #gera os gráficos
   print("Gráficos gerados com sucesso")
 
   #print_available_time_series()  #caso o usuário queira ver todas as śeries históricas disponíveis é só chamar essa função
 