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
    Retorna a lista de ativos presentes em br_stocks (dict{ticker_real, ticker_yf})
    Investing.com
    """
    symbols = br_stocks()['symbol'].to_list()
    tickers = {symbol : symbol + '.SA' for symbol in symbols}
    return tickers


def get_historical_prices_stocks_loop(tickers:list, interval:str, start:date, end=date.today(), period='1d'):
    """
    Retorna DF com cotações históricas para os ativos declarados em 'tickers'.
    Exemplos de intervalos entre as cotações:
        - 1m, 5m, 15m, 30m, 60m, 1h, 1d, 5d, 1wk, 1mo, 3mo

        ** Limites intraday:
            • 1m = máximo 7 dias nos últimos 30 dias
            • 60m, 1h = max 730 dias
    """

    TickersYF = yf.Tickers(tickers)
    result_df = pd.DataFrame()

    for i in TickersYF.tickers:
        ativo = i.replace(".SA", "")
        df_history = TickersYF.tickers[i].history(interval=interval, start=start, end=end, period=period)
        df_history['Ativo'] = ativo
        df_history = df_history[['Ativo', 'Open', 'Close', 'Low', 'High', 'Volume']]
        result_df = pd.concat([result_df, df_history])

    return result_df

def get_historical_prices_stocks(tickers:list, interval:str, start:date, end=date.today(), period='1d'):
    """
    ** Avaliar testes entre funções (x get_historical_prices_stocks_loop)
    
    Retorna DF com cotações históricas para os ativos declarados em 'tickers'.
    Exemplos de intervalos entre as cotações:
        - 1m, 5m, 15m, 30m, 60m, 1h, 1d, 5d, 1wk, 1mo, 3mo

        ** Limites intraday:
            • 1m = máximo 7 dias nos últimos 30 dias
            • 60m, 1h = max 730 dias
    """

    TickersYF = yf.Tickers(tickers)

    df_history = TickersYF.download(interval='1wk', start='2020-01-01', end=date.today(), period='1d')
    df_history = df_history.stack(level=1).rename_axis(['Date', 'Ativo']).reset_index(level=1)

    df_history = df_history[['Ativo', 'Open', 'Close', 'High', 'Low', 'Volume']]
    df_history['Ativo'] = df_history.Ativo.replace(".SA", "", regex=True)

    return df_history