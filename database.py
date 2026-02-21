import sqlite3
import pandas as pd
import logging

class Database:
    def __init__(self, database_name: str):
        self.logger = logging.getLogger(__class__.__name__)
        self.database_name = database_name
        self.con = sqlite3.connect(database=database_name, check_same_thread=False)
        self.cur = self.con.cursor()
        
    def close(self):
        self.con.close()
        
    def __repr__(self):
        return f" Database({self.database_name})"
		
    def tables(self):
        self.cur.execute("SELECT NAME FROM sqlite_master WHERE TYPE='table'")
        return [table_name[0] for table_name in self.cur.fetchall()]

    def save_df(self, df: pd.DataFrame, table_name: str):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(" 'df' has to be a pandas-dataframe")
        try:
            df.to_sql(name=table_name, con=self.con, if_exists="fail")
            self.con.commit()
            self.logger.info(f" {table_name} saved to database")
            return True
        except Exception as e:
            self.logger.error(f" {table_name}:\n{e}")
        return False
		
    def return_df(self, table_name):
        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", con=self.con, parse_dates=True)
            return df
        except Exception as e:
            self.logger.warning(f" {table_name} not in database:\n{e}")
            return pd.DataFrame()