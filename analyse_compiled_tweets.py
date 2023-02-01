import json
import operator
import nltk
import pandas as pd
import PyMediaRSS2Gen
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date, datetime
today = date.today()
now = datetime.now()

threshold_minutes = 30

def cargar_news():
	with open("Archivos Json/news_companies.json", 'r', encoding="utf-8") as news_file:
		diccionario_news_companies = json.load(news_file)
		return diccionario_news_companies

def obtener_top_companies():
	diccionario_news_companies = cargar_news()
	tuple_list = []
	for company in diccionario_news_companies.keys():
		num_articles = len(diccionario_news_companies[company])
		tuple_list.append((company, int(num_articles)))
	return sorted(tuple_list, key = lambda x: x[1])[:len(tuple_list)-3]

def obtener_top_companies_last_week():
	sorted_company_list =  obtener_top_companies()
	dict_news = cargar_news()
	date_today = today.strftime("%B %d, %Y").replace(",", "")
	elements_date_today = date_today.split(" ")
	month = elements_date_today[0]
	month = month[:3]
	elements_date_today[0] = month
	dict_news_companies = dict()
	for company, num_articles in sorted_company_list:
		dict_news_companies[company] = list()
		articles = dict_news[company]
		for article_dict in articles:
			date = article_dict["pubDate"]
			date.replace(",", "")
			elems_date = date.split(" ")
			try:
				day = elems_date[1]
				month = elems_date[2]
				year = elems_date[3]
				if month in elements_date_today and year in elements_date_today:
					if int(elements_date_today[1]) - int(day) < 7:
						dict_news_companies[company].append(article_dict)
			except:
				continue
	with open("Archivos Json/news_companies.json", 'w', encoding="utf-8") as news_file:
		json.dump(dict_news_companies, news_file)

def escribir_rss_xml_general(diccionario_contenido_noticias):
    mediaFeed = PyMediaRSS2Gen.MediaRSS2(
        title="News Sentiment Anlysis Stock Strategy",
        link="", #Cambiar a link Dropbox
        description="Stock's news throughout the day"
    )
    mediaFeed.copyright = "Owned by Matías Mingo"
    mediaFeed.lastBuildDate = datetime.now()
    mediaFeed.items = list()
    for key, value in diccionario_contenido_noticias.items():
        for noticia in value:
            mediaFeed.items.append(PyMediaRSS2Gen.MediaRSSItem(
                title=str("Company: "+key+"  "+noticia["titulo"]+"  Sentiment:"+noticia["sentiment"]),
                link=noticia["link"],
                description=noticia["summary"],
                pubDate=noticia["pubDate"]
            ))
    mediaFeed.write_xml(open("feed_rss.xml", "w"))

def sentiment_analysis():
	diccionario_news_companies = cargar_news()
	list_parser = []
	analyzer = SentimentIntensityAnalyzer()
	columns = ['Company','Date','Content']
	new_dict_news = {}
	sentiment_history_dict = {}
	for company, list_news in diccionario_news_companies.items():
		new_dict_news[company] = []
		sentiment_history_dict[company] = []
		for dict_news in list_news:
			sentiment = analyzer.polarity_scores("{} {}".format( dict_news["titulo"],dict_news["summary"]))
			compound_sentiment = sentiment["compound"]
			if compound_sentiment >=0.05:
				dict_news["sentiment"] = "positive"
				sentiment_history_dict[company].append([dict_news["pubDate"],"positive"])
			elif compound_sentiment <=-0.05:
				dict_news["sentiment"] = "negative"
				sentiment_history_dict[company].append([dict_news["pubDate"],"negative"])
			else:
				dict_news["sentiment"] = "neutral"
				sentiment_history_dict[company].append([dict_news["pubDate"],"neutral"])
			new_dict_news[company].append(dict_news)
	with open("Archivos Json/news_companies.json", 'w', encoding="utf-8") as news_file:
		json.dump(new_dict_news, news_file)
	escribir_rss_xml_general(new_dict_news)
	with open("Archivos Json/sentiment_history.json", "w", encoding="utf-8") as sentiment_history_file1:
		json.dump(sentiment_history_dict, sentiment_history_file1)

def analyse_sentiment_history():
	with open("Archivos Json/sentiment_history.json", "r", encoding="utf-8") as sentiment_history_file:
		history_dict = json.load(sentiment_history_file)
		for company, list_sentiments in history_dict.items():
			postive_count = 0
			negative_count = 0
			for sentiment_list in list_sentiments:
				date = sentiment_list[0]
				sentiment = sentiment_list[1]
				if sentiment == "positive":
					positive_count += 1
				elif sentiment == "negative":
					negative_count += 1
				date_news.replace(",", "")
				elems_date = date.split(" ")
				try:
					day = elems_date[1]
					month = elems_date[2]
					year = elems_date[3]
					time = elems_date[4]
					elems_time = time.split(":")
					hour = elems_time[0]
					minutes = elems_time[1]
					seconds = elems_time[2]
				except:
					continue


