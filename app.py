from flask import Flask, render_template, request, jsonify,url_for,redirect
import requests
import pandas as pd
from datetime import date, timedelta
import os
import yfinance as yf
import datetime as dt
import datetime
import matplotlib.pyplot as plt
from stocker import Stocker  #記得放在stocker下

#創建Flask物件app并初始化
app = Flask(__name__)

#通過python裝飾器的方法定義路由地址
@app.route("/index")
def root():
    #製作當日台股加權指數圖
    

    return render_template("index.html")


@app.route('/table')#url地址
def table():
    return render_template("tables.html")   

@app.route("/chart", methods=["POST"])
def fetchdata_to_js():
    if request.method == 'POST':
        #從tables.html拿股票代號
        stockNo=request.values['stockNo']

        #用股票代號抓預測資料
        start_date = '2012-01-01'
        df = yf.download(stockNo, start=start_date)#(stockNo, start=start_date)
        df = df.reset_index()
        stock = Stocker(stockNo, df)
        
        #未來30天股價
        stock.create_prophet_model(days = 30)
        #短中長期趨勢
        stock.changepoint_prior_analysis(changepoint_priors=[0.001, 0.05, 0.1, 0.2])
        #回測
        stock.evaluate_prediction()
        #轉換日期型態(當天)
        stock.max_date=stock.max_date.to_pydatetime()
 
        #data load to database
        #sel_toDB[["ds", "trend"]].to_sql(i[0:4], engine, chunksize=10000,index=None)
        return render_template("charts.html", chart_name=stockNo)
    
    return render_template("charts.html")


if __name__ == '__main__':
    #定義app在8080埠運行
    app.run(host="localhost",port=8000,debug=True)
