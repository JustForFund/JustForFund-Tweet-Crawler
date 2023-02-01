import telegram_notifications
import json
from datetime import date, datetime
from calendar import monthrange
import yfinance as yf
import sys
import requests
import os
from justforfund_algorithms_interaction import *
from justforfund_resources_interaction import *

MAX_NUMBER_STOCKS_PORTAFOLIO = 100
STANDARD_COMISSION = 0.01
threshold_minutes = 60

def cargar_news():
    with open("Archivos Json/news_companies.json", 'r', encoding="utf-8") as news_file:
        diccionario_news_companies = json.load(news_file)
        return diccionario_news_companies

def load_news_history():
    with open("Archivos Json/news_history.json", 'r', encoding="utf-8") as news_history_file:
        diccionario_news_history = json.load(news_history_file)
        return diccionario_news_history	

def write_news_history(link, sentiment, company):
    dict_news_history = load_news_history()
    with open("Archivos Json/news_history.json", 'w', encoding="utf-8") as news_history_file:
        dict_news_history[link] = {"sentiment":sentiment, "company":company}
        json.dump(dict_news_history, news_history_file)

def post_news_to_db(instrument_symbol, title, content, href, sentiment):
    url = 'https://justfor.fund/post_news_article'
    headers = {'TOKEN_ADMIN': os.environ['TOKEN_ADMIN']}
    data_dict = {'title': title, 'url': href, 'description': content, 'instrument_symbol': instrument_symbol, 'sentiment': sentiment}
    response = requests.post(url, json=data_dict, headers=headers)
    print(response)

def post_news_to_jff_resource(instrument_symbol, title, href, sentiment):
    market = detect_market(instrument_symbol)
    resource_dict = {
        "Symbol": instrument_symbol,
        "Market": market,
        "Title": title,
        "URL": href,
        "Sentiment": sentiment
    }
    print(resource_dict)
    upload_resource(6, resource_dict)

def detect_market(symbol):
    with open("Archivos Json/nasdaq_stocks.json", 'r', encoding="utf-8") as all_stocks_file:
        diccionario_stocks = json.load(all_stocks_file)
        if symbol in diccionario_stocks.keys():
            return "Nasdaq"
    with open("Archivos Json/nyse_stocks.json", 'r', encoding="utf-8") as all_stocks_file:
        diccionario_stocks = json.load(all_stocks_file)
        if symbol in diccionario_stocks.keys():
            return "NYSE"
    return ""   

def detect_month(month):
    dict_months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    return dict_months[month]
    
def get_news():
    today = date.today()
    now = datetime.utcnow()
    dict_news = cargar_news()
    date_today = today.strftime("%B %d, %Y").replace(",", "")
    time_now = now.strftime("%H:%M:%S")
    elems_time_now = time_now.split(":")
    hour_now = elems_time_now[0]
    minutes_now = elems_time_now[1]
    seconds_now = elems_time_now[2]
    elements_date_today = date_today.split(" ")
    month = elements_date_today[0]
    month = month[:3]
    elements_date_today[0] = month
    list_posible_orders_buy = list()
    list_posible_orders_sell = list()
    for company, list_news in dict_news.items():
        symbol = identify_symbol(company)
        sentiment_score = 0
        links = ""
        list_news = list_news[::-1]
        for news in list_news:
            fuente = news["fuente"]
            date_news = news["pubDate"]
            date_news.replace(",", "")
            links += "\n {}".format(news["link"])
            try:
                if fuente in ["Yahoo Finance", "Harvard Business"]:
                    elems_date = date_news.split("T")
                    date_list = elems_date[0].split("-")
                    time_str = elems_date[1][0:7]
                    elems_date = [" "]
                    elems_date.extend([date_list[2], date_list[1], date_list[0], time_str, "GMT"])
                elif fuente == "IB Times":
                    elems_date = date_news.split("T")
                    date_list = elems_date[0].split("-")
                    time_str = elems_date[1]
                    time_zone = time_str[8:13]
                    time_str = time_str[0:7]
                    elems_date = [" "]
                    elems_date.extend([date_list[2], date_list[1], date_list[0], time_str, time_zone])
                elif fuente == "Investing.com":
                    elems_date = date_news.split(" ")
                    date_list = elems_date[0].split("-")
                    time_str = elems_date[1]
                    elems_date = [" "]
                    elems_date.extend([date_list[2], date_list[1], date_list[0], time_str, "GMT"])
                elif fuente == "GlobeNewsWire":
                    date_list = date_news.split(" ")
                    elems_date = [" "]
                    time_str = date_list[4]+":00"
                    elems_date.extend([date_list[1], detect_month(date_list[2]), date_list[3], time_str, date_list[5]])			
                else:
                    elems_date = date_news.split(" ")
            except:
                continue
            try:
                day = elems_date[1]
                month = elems_date[2]
                year = elems_date[3]
                time = elems_date[4]
                elems_time = time.split(":")
                hour = int(elems_time[0])
                minutes = int(elems_time[1])
                seconds = int(elems_time[2])
                time_zone = ""
                if len(elems_date[5]) >3:
                    time_zone = int(str(elems_date[5])[0]+str(elems_date[5])[2])
                else:
                    time_zone = str(elems_date[5])[0:3]
                if time_zone == "EST":
                    hour += 4
                elif time_zone == "PST":
                    hour += 7
                elif time_zone == "GMT":
                    hour = hour
                elif time_zone == "PDT":
                    hour += 8
                else:
                    hour -= time_zone
                    if hour < 0:
                        hour += 24
                        day = str(int(day) - 1)
                        if len(day)==1:
                            day = "0{}".format(day)
                        if int(day) <=0:
                            month = str(int(detect_month(month)) - 1)
                            day = str(int(monthrange(int(year), int(month)-1)[1]) + int(day))
                            if len(day)==1:
                                day = "0{}".format(day)
                            if len(month)==1:
                                month = "0{}".format(month)
                            if int(month) <= 0:
                                month = str(12 + int(month))
                                year = str(int(year) - 1)
                                day = str(int(monthrange(int(year), int(month))[1]) + int(day))
                                if len(day)==1:
                                    day = "0{}".format(day)
                    elif hour > 24:
                        hour -= 24
                        day = str(int(day) + 1)
                        if len(day)==1:
                            day = "0{}".format(day)
                        if int(day) > int(monthrange(int(year), int(detect_month(month)))[1]):
                            day = str(int(day)-int(monthrange(int(year), int(detect_month(month)))[1]))
                            if len(day)==1:
                                day = "0{}".format(day)
                            month = str(int(detect_month(month)) + 1)
                            if len(month)==1:
                                month = "0{}".format(month)
                            if int(month) > 12:
                                month = str(int(month)-12)
                                year = str(int(year) + 1)
                if month in elements_date_today and year in elements_date_today and day in elements_date_today:
                    dif_hour = int(hour_now) - int(hour)
                    if dif_hour < 0:
                        dif_hour += 24
                    difference_time_minutes = (dif_hour)*60 + int(minutes_now) - int(minutes)
                    if difference_time_minutes <= 30 and difference_time_minutes >=-30:
                        sentiment = news["sentiment"]
                        dict_news_history = load_news_history()
                        if news["link"] in dict_news_history.keys():
                            print("link noticia se repite {}".format(news["link"]))
                            continue
                        else:
                            if sentiment == "positive":
                                sentiment_score += 1
                            elif sentiment == "negative":
                                sentiment_score -= 1
                            telegram_notifications.send("Company:{} \n Sentiment: {} \n {}".format(company, sentiment, news["link"]))
                            post_news_to_jff_resource(symbol, news["titulo"], news["link"], sentiment)
                            write_news_history(news["link"], sentiment, company)
                            post_news_to_db(company, news["titulo"], news["summary"], news["link"], sentiment)
                        telegram_notifications.send("{} Now:{}:{} news:{}:{} {} {}".format(company, hour_now, minutes_now, hour, minutes, difference_time_minutes, sentiment))
                        print("{} Now:{}:{} news:{}:{} {} {}".format(company, hour_now, minutes_now, hour, minutes, difference_time_minutes, sentiment))
            except Exception as e:
                print(elems_date)
                print(fuente)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(exc_type, exc_tb.tb_lineno)
                print(e)
                telegram_notifications.send(" {} ".format(e))
                continue
        if sentiment_score > 0:
            list_posible_orders_buy.append({"company": company, "score": sentiment_score, "links":links})
        elif sentiment_score < 0:
            list_posible_orders_sell.append({"company": company, "score": sentiment_score, "links":links})
    list_posible_orders_buy = sorted(list_posible_orders_buy, key = lambda i: i['score'], reverse = True)
    list_posible_orders_sell = sorted(list_posible_orders_sell, key = lambda i: i['score'])
    return list_posible_orders_buy, list_posible_orders_sell

def identify_symbol(stock_name):
    with open("Archivos Json/all_stocks.json", 'r', encoding="utf-8") as all_stocks_file:
        diccionario_stocks = json.load(all_stocks_file)
        if stock_name in diccionario_stocks.keys():
            return stock_name
        else:
            for symbol in diccionario_stocks.keys():
                if diccionario_stocks[symbol] == stock_name.lower():
                    return symbol


def get_realtime_price(ticker):
    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    price = float(last_quote)
    return price

