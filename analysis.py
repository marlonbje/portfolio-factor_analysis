from download import Ticker
from database import Database
from pathlib import Path
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class PFA:
    def __init__(self, file_path, interval="1d", start_date="2022-08-01"):
        self.logger = logging.getLogger(__class__.__name__)
        self.folder = Path("data")
        if not self.folder.exists() or not self.folder.is_dir():
            self.folder.mkdir()
        self.database = Database(f"{self.folder}/stockpricedata.db")
        self.file_path = Path(file_path)
        self.file_name = self.file_path.stem
        self.interval = interval
        try:
            self.start_date = pd.to_datetime(start_date)
        except Exception as e:
            self.logger.warning("Invalid Date Format")
            self.start_date = "2020-01-01"
        self.stocks = self.tickers()
        
    def tickers(self):
        try:
            with open(self.file_path, "r") as file:
                stocks = [stock.strip() for stock in file.readlines()]
                return stocks
        except FileNotFoundError:
            self.logger.error(f" {self.file_path} not found")
            return []
        
    def __repr__(self):
        return f"PortfolioAnalyzer({self.file_name})"
    
    def _multi_download(self):
        if self.stocks:
            for stock in self.stocks:
                name = f"{stock}_{self.interval}"
                if name not in self.database.tables():
                    data = Ticker(stock).price_data()
                    if not data.empty:
                        self.database.save_df(df=data, table_name=name)
            return True
        else:
            self.logger.warning("   No stocks available")
            return False
                    
    def _logreturns(self):
        alldata = []
        log_returns_df = pd.DataFrame()
        status = self._multi_download()
        if not status:
            return log_returns_df
        for stock in self.stocks:
            name = f"{stock}_{self.interval}"
            data = self.database.return_df(table_name=name)
            try:
                data.set_index("Date", drop=True, inplace=True)
                data.index = pd.to_datetime(data.index)
                data = data.loc[data.index >= self.start_date]
            except KeyError:
                self.logger.warning(f"   {stock}: Date not in Columns")
                continue
            alldata.append(data.Close.rename(stock))
                
        if alldata:
            df = pd.concat(alldata, axis=1, join="inner")
            try:
                log_returns = np.log(df / df.shift(1))
                log_returns_df = pd.DataFrame(columns=df.columns, index=df.index, data=log_returns).dropna()
            except TypeError:
                self.logger.error(" dataframe contains non-numeric values")
        return log_returns_df
    
    def pc_analysis(self):
        df = self._logreturns()
        if df.empty:
            return ()
        cols = df.columns
        scaler = StandardScaler()
        pca = PCA()
        scaled_arr = scaler.fit_transform(df)
        pca.fit(scaled_arr)
        cum_explained_var = np.cumsum(pca.explained_variance_ratio_)
        pc = [f"P{i + 1}" for i in range(len(cum_explained_var))]
        components = pd.DataFrame(data=pca.components_, index=pc, columns=cols)
        return (pd.Series(data=cum_explained_var, index=pc), components)
        
    def risk_analysis(self):
        df = self._logreturns()
        if df.empty:
            return ()
        std = df.std()
        cov = df.cov()
        return (std, cov)