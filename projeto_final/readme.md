# Projeto Final Monitores Curso GRACE 2024

## Análise de Dados da Série Histórica do IPEA Mapa Da Violência.

Esse projeto implementa um script em Python para análise de dados e geração de **gráficos** a partir dos dados do **IPEA** (Instituto de Pesquisas Econômicas Aplicadas) e de sua base do "Mapa da Violência", permitindo analisar dados como Taxa de Homicídio e Suicídio com uma análise por estado e por gênero.

A utilização do script se dá por **comandos no terminal**, no qual o usuário digita quais anos serão utilizados para a análise e qual dado/série histórica será analisado.

O **programa automaticamente gera gráficos, um para cada ano especificado**, a partir dos dados obtidos. Os gráficos serão salvos no diretório atual.

Os dados/séries históricas atualmente implementados são:

* taxa de homicídio

* taxa de homicídio de mulheres

* taxa de suicídio

* taxa de suicídio de mulheres

**OBS:** Os dados da API são por município, mas eles são agregados por Estado para facilitar a análise e desenho de gráficos.

### Como utilizar o código

1) Criar um ambiente virtual para baixar as dependências de forma isolada

```Bash
python3 -m venv nome_ambiente
```

2) Ativar o ambiente virtual:

* Comando no terminal do linux
   ```bash
   source nome_ambiente/bin/activate
   ```

* Terminal do Windows:
   ```bash
   nome_ambiente/Scripts/activate
   ```

3) Baixar as dependências do projeto:
```bash
pip install -r requirements.txt
```

4) Rodar o projeto:
```bash
python3 projeto_final.py
```

### Arquivo Auxiliar
O arquivo "info_municipios_ibge.csv" é um csv extraido das bases do IBGE contendo informações sobre os municípios do Brasil. Ele é necessário pois a API do IPEA apenas retorna o código do município dos dados coletados, portanto é necessário mapear cada código ao seu estado para permitir uma agregação e análise pelos estados.

### Libraries do Python Utilizadas 

* **Pandas**: Library para manipulação de dados tabulares com DataFrames, permite operações similares a GROUP BY e tabelas pivô nos dataframes


* **Requests**: Library para realizar requests HTTP de forma mais fácil, permitindo acesso a API mais facilmente

* **Matplotlib**: Lib para criar os gráficos a partir dos dados extraidos


### Inspiração
Eu estou atualmente desenvolvendo um [projeto](https://github.com/caue-paiva/intelli.gente_data_extraction) com bolsa FAPESP sobre **coleta e análise de dados públicos**. Portanto eu achei pertinente fazer um projeto final do curso de monitores da GRACE que também englobasse esse tema. 

Além disso, a base do IPEA do Mapa da Violência contém diversas séries históricas, incluindo análise da violência por gênero, violência Psicológica... entre outras, então seria possível **expandir o projeto e focar em coletar ainda mais dados sobre a violência contra as mulheres no Brasil**, com uma série histórica permitindo ver a mudança nesse cenário ao longo do tempo.