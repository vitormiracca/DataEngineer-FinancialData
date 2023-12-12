# encoding = utf-8


from modulos import objetos_investing as obj, search_quotes as inf



ativos_dict = obj.br_tickers()
ativos_list_yf = [ativos_dict[i] for i in ativos_dict]


df_ativos_historico = inf.get_historical_prices_stocks(tickers=ativos_list_yf, interval='1mo', start='2023-01-01')


