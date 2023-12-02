from datetime import date
import pandas as pd
import investpy as inv
import yfinance as yf

country = 'brazil'


def br_stocks() -> pd.DataFrame:
    """
    Retorna um Dataframe com todas os valores mobiliarios do Brasil, listados no investing.com
    Seguintes colunas:
    ==================================================
    country	name | full_name | isin | currency | symbol
    ==================================================

    Os dados estão desatualizados. A função get_stocks não busca os ativos atualizados
    """
    br_stocks = inv.get_stocks_dict(country=country)
    br_stocks = pd.DataFrame(br_stocks)
    return br_stocks

def br_tickers() -> dict : 
    """
    Retorna a lista de ativos presentes em br_stocks
    Investing.com
    """
    symbols = br_stocks()['symbol'].to_list()
    tickers = {symbol : symbol + '.SA' for symbol in symbols}
    return tickers


def get_historical_prices_stocks(tickers, ):
    """

    """

    TickersYF = yf.Tickers(tickers)
    result_df = pd.DataFrame()

    for i in TickersYF.tickers:
        ativo = i.replace(".SA", "")
        df_history = TickersYF.tickers[i].history(period='1d', interval='1wk', start='2020-01-01', end=date.today())
        df_history['Ativo'] = ativo
        df_history = df_history[['Ativo', 'Open', 'Close', 'Low', 'High', 'Volume']]
        result_df = pd.concat([result_df, df_history])

    return result_df
