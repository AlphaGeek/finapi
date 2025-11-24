import sys
from numpy import isnan
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.sql import text as sqltext
from datetime import datetime

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
      #self.df = pd.read_sql(sqltext(sql_query), self.conn)
      #print(sql_query)
      self.conn.execute(text(sql_query))
      self.conn.commit()
    except Exception as e:
      #print(f"DM Unexpected DB error: {e}")
      raise Exception("Unexpected DB error: ", sys.exc_info()[0])
    finally:
      self.conn.close()
      self.engine.dispose()
    
    return self.df.to_json
  

def getLatestCapitalTrades(): 
  dataMgr = SqlServerDataManager()
  for page in range(172,349):
    print(f"Getting data for page {page}")
    df = pd.read_html(f"https://www.capitoltrades.com/trades?txType=buy&pageSize=300&page={page}")[0]
    for index, trade in df.iterrows():
      politician = ""
      party = ""
      owner = ""
      company = ""
      trade_date = ""
      published_date = ""
      trade_side = ""
      size_min = "null"
      size_max = "null"
      trade_price = 'null'
      
      if trade.Politician != None and "Democrat" in trade.Politician:
        politician = trade.Politician.split("Democrat", 1)[0]
        party = "Democrat"
      elif trade.Politician != None and "Republican" in trade.Politician:
        politician = trade.Politician.split("Republican", 1)[0]
        party = "Republican"
      owner = trade.Owner
      company = trade["Traded Issuer"]
      try:
        date_obj = datetime.strptime(trade.Traded, "%d %b%Y")
        trade_date = date_obj.strftime("%Y-%m-%d")
      except: 
        trade_date = "1900-01-01" 
      try:
        date_obj = datetime.strptime(trade.Published, "%d %b%Y")
        published_date = date_obj.strftime("%Y-%m-%d")
      except: 
        published_date = "1900-01-01" 
      trade_side = trade.Type
      
      try:
        if trade.Size == '< 1K':
          size_min = 0
          size_max = 1000
        else:  
          trade_split = trade.Size.split("–", 1)
          if len(trade_split) > 1: 
            size_min = trade_split[0]
            size_max = trade_split[1]
            if size_min.endswith("K"): 
              size_min = int(size_min.rstrip("K"))*1000    
            elif size_min.endswith("M"): 
              size_min = int(size_min.rstrip("M"))*1000000    
            if size_max.endswith("K"): 
              size_max = int(size_max.rstrip("K"))*1000    
            elif size_max.endswith("M"): 
              size_max = int(size_max.rstrip("M"))*1000000   
          else: 
            print(trade_split) 
      except Exception as e:
        print("Error splitting trade size:   " + str(trade.Size.split("-", 1)) + e)
      trade_price = str(trade.Price).lstrip('$').replace(",", "")
      if trade_price == 'nan':
        trade_price = 'null'
      key = (str(index) + politician + company + str(trade_date) + trade_side + trade_price + str(size_min) + str(size_max)).replace(" ", "").replace(".", "")
      sql = f"""insert into capital_trades (p_key, politician, party, owner, company, trade_date, published_date, trade_side, size_min, size_max, trade_price)
              values('{key}', '{politician}', '{party}', '{owner}', '{company}', '{trade_date}', '{published_date}', '{trade_side}', {size_min}, {size_max}, {trade_price})"""
      #print(sql)
      try:
        dataMgr.executeQuery(sql)
      except Exception as e:
        continue
        #print(f"Unexpected DB error: {e}")
      
      

getLatestCapitalTrades()
print("DONE!")