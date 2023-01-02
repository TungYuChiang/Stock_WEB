from flask import Flask, request, render_template
import requests
import pandas as pd
from datetime import date, timedelta
import mysql.connector
import pymysql
from sqlalchemy import create_engine
import os
import yfinance as yf
from stocker import Stocker  #記得放在stocker下

#connect db
#engine = create_engine('mysql+pymysql://root:fdhg4322@localhost:3306/test')
#'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

stockNo=["2330.TW","2317.TW","2454.TW","2412.TW","6505.TW","2308.TW","2881.TW","1303.TW","1301.TW","2882.TW",
"2303.TW","2002.TW","2886.TW","2891.TW","3711.TW","1326.TW","1216.TW","5880.TW","2892.TW","5871.TW",
"2603.TW","2884.TW","3045.TW","2207.TW","2880.TW","3008.TW","2912.TW","2885.TW","2382.TW","2395.TW",
"0050.TW","1101.TW","2609.TW","2615.TW","4904.TW","5876.TW","2883.TW","2357.TW","6488.TW","2327.TW",
"2890.TW","8069.TW","1590.TW","2801.TW","3034.TW","2887.TW","9910.TW","1605.TW","3037.TW","4938.TW"]

for i in stockNo:
    start_date = '2012-01-01'
    df = yf.download(i, start=start_date)#(stockNo, start=start_date)
    df = df.reset_index()
    stock = Stocker(i, df)
    
    #歷史股價
    #stock.plot_stock()

    #未來X天股價
    model, model_data = stock.create_prophet_model(days=7)

    #轉換日期型態(當天)
    stock.max_date=stock.max_date.to_pydatetime()

    #預測的表格
    sel_toDB=model_data[model_data['ds'] > stock.max_date]

    #data load to database
    #sel_toDB[["ds", "trend"]].to_sql(i[0:4], engine, chunksize=10000,index=None)

