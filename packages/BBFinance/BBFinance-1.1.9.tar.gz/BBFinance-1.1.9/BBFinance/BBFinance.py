#BIBLIOTECAS PARA ANALISE DE ATIVOS
import yfinance as yf
from scipy.stats import norm

#BIBLIOTECAS PARA WEBSCRAPING
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import requests
from bs4 import BeautifulSoup

#BIBLIOTECAS DE CHAMADAS DE API
from fastapi import FastAPI, Response
from fastapi.templating import Jinja2Templates
import json
import uvicorn

#BIBLIOTECAS DE ANALISE DE DATAFRAMES, DADOS E CRIAÇAO DE CLASSES
import pandas as pd
import numpy as np
from enum import Enum
from pydantic import BaseModel
from typing import List, Union, Optional

import warnings
warnings.filterwarnings("ignore")

# chromedriver_autoinstaller.install()
yf.pdr_override()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class TipoSetores(str, Enum):
    Corporativas = "Lajes Corporativas"
    Mobiliarios = "Títulos e Val. Mob."
    Shoppings = "Shoppings"
    Hibridos = 'Híbrido'
    Renda = 'Renda'
    Logistica = 'Logística'
    Hospital = 'Hospital'
    Residencial = 'Residencial'
    Outros = 'Outros'

def formataValoresNumero(df, nomeColuna):
    df[nomeColuna] = df[nomeColuna].replace('[.]', '', regex=True)
    df[nomeColuna] = df[nomeColuna].replace('[%]', '', regex=True)
    df[nomeColuna] = df[nomeColuna].replace('[,]', '.', regex=True)
    df[nomeColuna] = df[nomeColuna].astype(float)

    return df

## INFOS DAS AÇOES ##
@app.get("/stocks/{symbol}/info")
def get_info(symbol: str):
    
    """
    Usabilidade -> Busca as principais informaçoes sobre o ativo selecionado como Preço e Dividendos \n
    
    symbol -> Nome do Ativo para a busca \n
    
    """
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info #DADO Q VEM COMO UM DICIONARIO, SE NAO FOR UM DICIONARIO VAI APRESENTAR TICKER INVALIDO
        if isinstance(info, dict):
            pass #SE FOR VAI SO PASSAR 
    except:
        return {"error": print("Invalid ticker symbol")}
    
    # Obtenha o valor a mercado da açao
    current_price = stock.info['regularMarketPrice']

    # Obtenha o nome completo da empresa
    company_name = stock.info['longName']

    #Valor de Dividendos
    dividend = stock.dividends
    dividend = dividend.iloc[-1:].sum()
    
    # Crie um objeto JSON com as informações da ação
    json_data = {'symbol': symbol, 
                 'current_price': current_price, 
                 'company_name': company_name,
                 'dividends' : dividend}
    
    formatted_json = json.dumps(json_data, indent=5)
    print(formatted_json)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, default="stocks/{symbol}/info")
response = Response(media_type="application/json")


## HISTORICO DAS AÇOES ##

@app.get("/stocks/{symbol}/history")
def get_stock_history(symbol: str, period: str = '1y'):
    
    """
    Usabilidade -> Usada para verificar o histórico da açao selecionada e em qual periodo \n
    
    symbol -> Nome do Ativo para a busca \n
    period -> Data em ANOS para a busca das informaçoes do Ativo \n
    
    """
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info #DADO Q VEM COMO UM DICIONARIO, SE NAO FOR UM DICIONARIO VAI APRESENTAR TICKER INVALIDO
        if isinstance(info, dict):
            pass #SE FOR VAI SO PASSAR 
    except:
        return {"error": print("Invalid ticker symbol")}
    
    history = stock.history(period=period)
    
    if history.empty:
        return {"error": print("No data found")}
    else:
        history_dict = history.to_dict(orient="list")
        history_df = pd.DataFrame.from_dict(history_dict).reset_index(drop=False)     
        print(history_df)
        # json_data = {'symbol': symbol,
        # "history":  history_df.to_dict(orient="records"),
        # }

        # formatted_json = json.dumps(json_data, indent=2)
        # print(formatted_json)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, default="stocks/{symbol}/history")
responseHistory = Response(media_type="application/json")


## TENDENCIA DE PREÇO ##

@app.get("/stock/{symbol}/trend")
def get_stock_trend(symbol: str):
    
    """
    Usabilidade -> Identifica a tendencia de preço de uma açao, se ira ser de ALTA ou BAIXA
    
    symbol -> Nome do Ativo para a busca \n
    
    """
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info #DADO Q VEM COMO UM DICIONARIO, SE NAO FOR UM DICIONARIO VAI APRESENTAR TICKER INVALIDO
        if isinstance(info, dict):
            pass #SE FOR VAI SO PASSAR 
    except:
        return {"error": print("Invalid ticker symbol")}

    history = stock.history(period='1d')
    close_prices = history['Close']
    trend = 'up' if close_prices.iloc[-1] > close_prices.iloc[0] else 'down'
    
    json_data = { "symbol": symbol,
                "trend": trend,
    }
    
    formatted_json = json.dumps(json_data, indent=2)
    print(formatted_json)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, default="stocks/{symbol}/trend")
responseHistory = Response(media_type="application/json")


## RSI ##

@app.get("/stock/{symbol}/technical")
def get_stock_technicals(symbol: str):
    
    """
    Usabilidade -> cálculo envolve a comparação da média de ganhos em um período de tempo com a média de perdas em um período de tempo. \n
    Como interpretar -> Quando o RSI está acima de 70, o ativo é considerado sobrecomprado, o que significa que pode estar prestes a sofrer uma correção para baixo. 
    Quando o RSI está abaixo de 30, o ativo é considerado sobrevendido, o que significa que pode estar prestes a subir novamente. \n 
    
    symbol -> Nome do Ativo para a busca \n
    
    """
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info #DADO Q VEM COMO UM DICIONARIO, SE NAO FOR UM DICIONARIO VAI APRESENTAR TICKER INVALIDO, SENAO VAI PASSAR
        if isinstance(info, dict):
            pass 
    except:
        return {"error": print("Invalid ticker symbol")}

    history = stock.history(period='max')
    close_prices = history['Close']
    
    # Calcula as médias móveis
    sma_50 = close_prices.rolling(window=50).mean().iloc[-1] #calcula as médias móveis de 50 períodos
    sma_200 = close_prices.rolling(window=200).mean().iloc[-1]  #calcula as médias móveis de 200 períodos
    
    # Calcula o Índice de Força Relativa (RSI)
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    if rsi >= 70:
        status = 'A chance do preco do ativo CAIR'
    else:
        status = 'A chance do preco do ativo SUBIR'
    
    json_data = {
        "symbol": symbol,
        "sma_50": sma_50,
        "sma_200": sma_200,
        "rsi": rsi,
        "tendency" : status
    }

    formatted_json = json.dumps(json_data, indent=4)
    print(formatted_json)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, default="stocks/{symbol}/technical")
responseHistory = Response(media_type="application/json")


## VOLATILIDADE ##

@app.get("stocks/{symbol}/volatility")
def get_volatility(symbol: str, start_date: str, end_date: str):
    
    """
    Usabilidade -> Método usado para verificar a volatilidade de um ativo em comparacao ao mercado em que esta  \n
    
    symbol -> Nome do Ativo para a busca \n
    start_date -> Data de Inicio da busca das infos (preco, volume, etc) do ativo \n
    end_date -> Data Final para a busca das infos (preco, volume, etc) do ativo \n
    """
    
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        if stock_data.empty:
            return {"error": print("Nao foi encontrado o historico nesse periodo, verificar.")}
    except:
        pass
    
    log_returns = np.log(stock_data['Close']/stock_data['Close'].shift(1))
    volatility = np.sqrt(252*log_returns.var())
    return {'volatility': print(volatility)}

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, default="stocks/{symbol}/volatility")
responseHistory = Response(media_type="application/json")


## BETA ##

@app.get("stocks/{symbol}/beta")
def get_beta(symbol: str):
    
    """
    Usabilidade -> O beta é uma medida estatística que indica a relação entre a volatilidade de uma ação e a volatilidade do mercado como um todo.
    O valor do beta é utilizado para medir o risco de uma ação em relação ao mercado em que ela é negociada. \n
    
    symbol -> Nome do Ativo para a busca \n
    market -> Como padrao, Mercado: IBOVESPA / BVSP
    """
    
    # Obter os dados do ativo e do mercado
    try:
        asset = yf.Ticker(symbol)
        market = yf.Ticker("^BVSP") # Índice Bovespa como mercado de referência
        info = asset.info #DADO Q VEM COMO UM DICIONARIO, SE NAO FOR UM DICIONARIO VAI APRESENTAR TICKER INVALIDO, SENAO VAI PASSAR
        infoMarket = market.info
        if isinstance(info, dict) | isinstance(infoMarket, dict) :
            pass 
    except:
        return {"error": print("Invalid ticker symbol")}

    asset_history = asset.history(period="max")
    market_history = market.history(period="max")

    # Calcular os retornos diários
    asset_returns = asset_history['Close'].pct_change()
    market_returns = market_history['Close'].pct_change()

    # Calcular o beta
    cov = asset_returns.cov(market_returns)
    var = market_returns.var()
    beta = cov / var

    if beta > 1:
        status = 'Acao mais Volatil que o mercado em geral'
    if beta < 1:
        status = 'Acao menos Volatil que o mercado em geral'
    if beta == 1:
        status =  'Acao com a mesma Volatilidade que o mercado em geral'


    json_data =  {"beta": beta,
                  "status" : status}
    
    formatted_json = json.dumps(json_data, indent=2)
    print(formatted_json)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, default="stocks/{symbol}/beta")
responseHistory = Response(media_type="application/json")


## VAR ##

def calculate_historical_var(symbol: str, confidence_level: float, lookback_period: int) -> float:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info #DADO Q VEM COMO UM DICIONARIO, SE NAO FOR UM DICIONARIO VAI APRESENTAR TICKER INVALIDO, SENAO VAI PASSAR
        if isinstance(info, dict):
            pass 
    except:
        return {"error": print("Invalid ticker symbol")}

    # Obter os dados de preços do ativo
    prices = stock.history(period=f"{lookback_period}d")["Close"]

    # Calcular o retorno diário da ação
    returns = np.log(prices / prices.shift(1))

    # Calcular o desvio padrão e o VaR histórico
    std_dev = returns.std()
    var = std_dev * norm.ppf(1 - confidence_level)

    return round(var * prices[-1], 2)

@app.get("stocks/{symbol}/VaR")
def var(symbol: str, confidence_level: float, lookback_period: int):
    
    """
    Usabilidade -> O Value at Risk (VaR) é uma medida de risco que indica a perda máxima esperada, com um determinado nível de confiança, em um intervalo de tempo pré-determinado. \n
    
    symbol -> Nome do Ativo para fazer a busca \n
    confidence_level -> Nivel de confiança para o VAR (0 a 1), normalmente usado em 0.95 \n
    lookback_period -> Periodo EM DIAS a ser considerado para o cálculo do VaR

    """
    
    return {"VaR": print(calculate_historical_var(symbol, confidence_level, lookback_period))}

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, default="stocks/{symbol}/VaR")
responseHistory = Response(media_type="application/json")


## LIST QUOTE ##

@app.get("stocks/{symbol}/AnnualReturn", response_model=None)
def carteira_ativos(symbols: Union[str, list], start_date: str, end_date: str) -> pd.DataFrame:
    """
    ## Usabilidade
    - Recebe uma lista e retorna um DataFrame com as informações dos ativos e algumas estatísticas básicas. \n
    
    ## Parâmetros
    - symbols -> Recebe uma lista ou um unico ativo para buscar na base \n
    - start_date -> Data de Inicio da busca das infos (preco, volume, etc) do ativo \n
    - end_date -> Data Final para a busca das infos (preco, volume, etc) do ativo \n
    
    """
    # Importar dados dos ativos
    
    if isinstance(symbols, str):
        print(f"Você digitou uma string: {symbols}")
        dados = yf.download(tickers= symbols, start= start_date, end= end_date, group_by= 'ticker')
            
        try:
            #Exibe o preço a mercado da açao
            data = yf.Ticker(symbols).info
            valueMarket = data['regularMarketPrice']
            
            #Retorna o preço de fechamento da açao
            close = dados['Close']
            
            # Calcular retornos diários
            retorno_diario = close.pct_change()
            
            # Calcular retornos anuais
            retorno_anual = retorno_diario.mean() * 252
                    
            # Calcular desvio padrão anual
            desvio_padrao_anual = retorno_diario.std() * (252 ** 0.5)
            
            # Calcular valor total investido
            valor_investido = close.iloc[0] * 100
            
            # Calcular valor atual
            valor_atual = close.iloc[-1] * 100
            
            # Calcular retorno total
            retorno_total = (valor_atual - valor_investido) / valor_investido
            
            # Organizar em um DataFrame
            valueSymbols = pd.DataFrame({
                'Ativo' : symbols,
                'Preço a Mercado' : valueMarket,
                'Retorno anual': retorno_anual,
                'Desvio padrão anual': desvio_padrao_anual,
                'Retorno total': retorno_total
            }, index=[1])
            
            print(valueSymbols)

        except:
            print("Ticker inválido")
  
    elif isinstance(symbols, list):
        valueDF = pd.DataFrame()
        print(f"Você digitou uma lista: {symbols}")
        for simbolo in symbols:
            dados = yf.download(tickers= simbolo, start= start_date, end= end_date, group_by= 'ticker')
        
            # Selecionar preços de fechamento
            close = dados['Close']
            
            # Calcular retornos diários
            retorno_diario = close.pct_change()
            
            # Calcular retornos anuais
            retorno_anual = retorno_diario.mean() * 252
                        
            # Calcular desvio padrão anual
            desvio_padrao_anual = retorno_diario.std() * (252 ** 0.5)
            
            # Calcular valor total investido
            valor_investido = close.iloc[0] * 100
            
            # Calcular valor atual
            valor_atual = close.iloc[-1] * 100
            
            # Calcular retorno total
            retorno_total = (valor_atual - valor_investido) / valor_investido
            
            # Organizar em um DataFrame
            returnSymbols = pd.DataFrame({
                'Ativo' : simbolo,
                'Retorno anual': retorno_anual,
                'Desvio padrão anual': desvio_padrao_anual,
                'Retorno total': retorno_total
            }, index=[len(symbols)])
            
            valueDF = pd.concat([returnSymbols, valueDF])
        print(valueDF)

    else:
        print("Tipo inválido. Digite uma string ou uma lista.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, default="stocks/{symbol}/AnnualReturn")
responseHistory = Response(media_type="application/json")


@app.get("stocks/{symbol}/MarkowitzAllocationn")
def markowitz_allocation(symbols= list, star_date= str, end_date=str) -> str: 
    
    """
    ## Usabilidades 
    Alocação de Markowitz é uma técnica de otimização de portfólio que visa encontrar a combinação ideal de ativos para maximizar o retorno do investimento enquanto minimiza o risco. \n
    
    ## O Retorno Esperado
    - representa a taxa de retorno média que se espera obter do portfólio de investimentos \n
    ## O Risco 
    - representa a medida de volatilidade do portfólio, ou seja, 
    quanto mais instável for o retorno dos ativos, maior será o risco do portfólio como um todo \n
    
    ## Parâmetros
    
    - symbols -> Recebe uma lista de ativos para buscar na base \n
    - start_date -> Data de Inicio da busca das infos (preco, volume, etc) do ativo \n
    - end_date -> Data Final para a busca das infos (preco, volume, etc) do ativo \n

    """
    
    dados = yf.download(symbols, start=star_date, end=end_date)['Adj Close']

    # Calculando os retornos diários dos ativos
    retornos = dados.pct_change().dropna()

    # Calculando a matriz de covariância dos retornos
    matriz_covariancia = retornos.cov()

    # Definindo o vetor de pesos de igual peso para todos os ativos
    pesos = np.array([1/len(lista)] * len(lista))

    # Calculando o retorno esperado e o risco da carteira com pesos iguais
    retorno_esperado = np.sum(retornos.mean() * pesos) * 252
    risco = np.sqrt(np.dot(pesos.T, np.dot(matriz_covariancia, pesos))) * np.sqrt(252)

    # Imprimindo os resultados
    # print("Retorno esperado: ", retorno_esperado)
    # print("Risco: ", risco) 
    
    # Calculando a alocação de Markowitz
    cov_inv = np.linalg.inv(matriz_covariancia)
    vetor_uns = np.ones((len(lista),1))
    w_markowitz = np.dot(cov_inv, vetor_uns) / np.dot(np.dot(vetor_uns.T, cov_inv), vetor_uns)
    w_markowitz = w_markowitz.flatten()

    # Imprimindo a alocação de Markowitz
    markowitzList = []
    for i in range(len(lista)):
        taxas = f"O ativo {lista[i]} deve ser alocado em {w_markowitz[i] * 100:.2f}% da carteira"
        markowitzList.append(taxas)
    json_data = {'Retorno Esperado' : retorno_esperado,
                 'Risco da Carteira' : risco,
                 'Alocacao Markowitz' : markowitzList}
    
    formatted_json = json.dumps(json_data, indent=2)
    print(formatted_json)
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, default="stocks/{symbol}/MarkowitzAllocation")
responseHistory = Response(media_type="application/json")



@app.get("/infoFunds", response_model=None)
def get_funds(symbol= str) -> pd.DataFrame:
    url = "https://www.fundsexplorer.com.br/ranking"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table")[0]
    fundsDF = pd.read_html(str(table))[0]    
    fundsDF['Código do fundo'] = fundsDF['Código do fundo'].apply(lambda x: x+'.SA')
        
    valuesFI = fundsDF.loc[(fundsDF['Código do fundo'] == symbol)]
    valuesFI = valuesFI[['Código do fundo', 'Setor', 'Preço Atual', 'Dividendo', 'Variação Preço', "Rentab. Período"]]
    
    return print(valuesFI)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, default="/infoFunds")
responseHistory = Response(media_type="application/json")



@app.get("/compareSetorFunds")
def compare_setor_funds(setor: TipoSetores, rentabilidade_min = 0) -> pd.DataFrame:
        
    url = "https://www.fundsexplorer.com.br/ranking"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all("table")[0]
    fundsDF = pd.read_html(str(table))[0]

    formataValoresNumero(fundsDF, "Rentab. Período")
    rentabilidade_min = rentabilidade_min / 100
    valuesFI = fundsDF.loc[(fundsDF["Rentab. Período"]/100) > rentabilidade_min]
    valuesFI = valuesFI[['Código do fundo', 'Setor', 'Preço Atual', 'Dividendo', 'Variação Preço', "Rentab. Período"]]
    valuesFI = valuesFI.dropna()
    rentabilidade_media = valuesFI['Rentab. Período'].mean()
    rentabilidade_mercado = valuesFI.loc[valuesFI["Setor"] == setor]["Rentab. Período"].mean()
    
    desvio_padrao = valuesFI["Rentab. Período"].std()
    
    resultados = pd.DataFrame({
        "Rentabilidade Média dos FIIs Selecionados": [rentabilidade_media],
        "Rentabilidade Média do Mercado": [rentabilidade_mercado],
        "Desvio Padrão das Rentabilidades dos FIIs Selecionados": [desvio_padrao]
    })
    
    resultados = resultados.fillna('O setor/valor nao foi encontrado')
    
    return print(resultados)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, default="/compareSetorFunds")
responseHistory = Response(media_type="application/json")

lista = ['MXRF11.SA', 'VGIR11.SA']
def compare_funds(listfund= None, fund_1= str, fund_2= str) -> pd.DataFrame:

    if fund_1 and fund_2 != None:
        url = "https://www.fundsexplorer.com.br/ranking"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find_all("table")[0]
        fundsDF = pd.read_html(str(table))[0]    
        fundsDF['Código do fundo'] = fundsDF['Código do fundo'].apply(lambda x: x+'.SA')
        fundsDF = fundsDF[['Código do fundo', 'Setor', 'Preço Atual', 'Dividendo', 'Variação Preço', "Rentab. Período", 'Dividend Yield', 'DY (3M) Acumulado']]
        fundsDF = fundsDF.drop_duplicates(subset=['Código do fundo'])
        
        fund1 = fundsDF.loc[fundsDF["Código do fundo"] == fund_1]
        fund2 = fundsDF.loc[fundsDF["Código do fundo"] == fund_2]

        unit = pd.concat([fund1, fund2])
        if unit.empty:
            print('Nao foram apresentado dados dos fundos para verificaçao unica')
        else:
            print(unit)
        
    if listfund is None:
        listfund = []
    else:
        max_risco = -1
        ticker_max_risco = ''
        for ticker in lista:
            fundo = yf.Ticker(ticker)
            df = fundo.history(period='max')
            desvio_padrao = df['Close'].pct_change().std()
            if desvio_padrao > max_risco:
                max_risco = desvio_padrao
                ticker_max_risco = ticker
            
        valuerisk = pd.DataFrame({'Fund' : ticker_max_risco,
                    'Max risk (%)' : max_risco * 100}, index=[len(lista)])
        
        if valuerisk.empty:
            print('Nao foram apresentado dados dos fundos para verificaçao multipla')
        else:
            print(valuerisk)

compare_funds(listfund=['MXRF11.SA', 'VGIR11.SA'])