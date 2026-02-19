import yfinance as yf
import pandas as pd
import logging

class Ticker:
    def __init__(self, ticker_symbol: str):
        self.logger = logging.getLogger(__class__.__name__)
        self.ticker_symbol = ticker_symbol.strip().upper()
        
    def __repr__(self):
        return f'   Ticker({self.ticker_symbol})'
        
    def __eq__(self, other):
        return other.ticker_symbol == self.ticker_symbol
        
    def price_data(self, interval: str ="1d"):
        try:
            df = yf.download(
                self.ticker_symbol, 
                period="max", 
                interval=interval, 
                auto_adjust=True, 
                multi_level_index=False,
                progress=False
            )
            return df
        except Exception as e:
            self.logger.error(f"    Failed to download {ticker_symbol}: {e}")
            return pd.DataFrame()
            
    def fundamental_data(self, freq: str ="quarterly"):
        try:
            freq = freq.lower().strip()
            ticker = yf.Ticker(self.ticker_symbol)
            income_stmt = ticker.get_income_stmt(freq=freq)
            balance_sheet = ticker.get_balance_sheet(freq=freq)
            cash_flow = ticker.get_cash_flow(freq=freq)
            df = pd.concat([income_stmt, balance_sheet, cash_flow]).T
            df.sort_index(inplace=True)
            if freq == "quarterly":
                df.index = df.index.to_period("Q").astype(str)
            else:
                df.index = df.index.year.astype(str)
            df.drop_duplicates(keep="first", inplace=True)
            return df
        except Exception as e:
            self.logger.error(f"    Failed to download {ticker_symbol}: {e}")
            return pd.DataFrame()
        