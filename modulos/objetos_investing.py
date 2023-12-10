from datetime import date
import investpy as inv

country = 'brazil'

def br_stocks():
    """
    Retorna um Dataframe com todas os valores mobiliarios do Brasil, listados no investing.com
    Seguintes colunas:
    ==================================================
    country	name | full_name | isin | currency | symbol
    ==================================================

    Os dados estão desatualizados. A função get_stocks não busca os ativos atualizados
    """
    br_stocks = inv.get_stocks_dict(country=country)
    br_stocks_json = {empresa['symbol']: {chave: valor for chave, valor in empresa.items() if chave != 'symbol'} for empresa in br_stocks}
    return br_stocks_json

def br_tickers() -> dict : 
    """
    Retorna a lista de ativos presentes em br_stocks (dict{ticker_real, ticker_yf})
    Investing.com
    """
    symbols_list = [symbol for symbol in br_stocks()]
    tickers = {symbol : symbol + '.SA' for symbol in symbols_list}
    return tickers

def cryptos_json():
    dic_list = inv.get_cryptos_dict()
    cryptos_json = {f"{crypto['symbol']}-{crypto['currency']}" : {chave: valor for chave, valor in crypto.items() if chave != 'symbol'} for crypto in dic_list}

    return cryptos_json

def get_cryptos_tickers():
    tickers = [i for i in cryptos_json()]

    return tickers