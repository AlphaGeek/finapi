import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sqltext
import sys

class SqlServerDataManager:
  def __init__(self, server='.', database='PortfolioAI'):
    self.server = server
    self.database = database
    self.connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};Trusted_Connection=yes;multiSubnetFailover=yes;"
    self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.connection_string}")
    self.conn = None
    self.df = None

  def executeQuery(self, sql_query):
    try:
      self.conn = self.engine.connect()
      self.df = pd.read_sql(sqltext(sql_query), self.conn)
    except:
      raise Exception("Unexpected DB error: ", sys.exc_info()[0])
    finally:
      self.conn.close()
      self.engine.dispose()
    
    return self.df.to_json


               