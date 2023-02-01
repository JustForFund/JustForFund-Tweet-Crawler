import json

def write_companies_json(diccionario_fuentes_noticias_rss):    
    with open("Archivos Json/news_companies.json", 'w', encoding="utf-8") as news_companies_file:
        json.dump(diccionario_fuentes_noticias_rss, news_companies_file)
        

def load_todo():
    diccionario_fuentes_noticias_rss = transform_rss.transformar()
    nuevo_diccionario_noticias = dict()
    for fuente in diccionario_fuentes_noticias_rss.keys():
        lista_noticias = diccionario_fuentes_noticias_rss[fuente]
        for dict_noticia in lista_noticias:
            company = dict_noticia["company"]
            if company in nuevo_diccionario_noticias.keys():
                nuevo_diccionario_noticias[company].append({"titulo":dict_noticia["titulo"],
                                                "link":dict_noticia["link"],
                                                       "summary": dict_noticia["summary"],
                                                       "pubDate": dict_noticia["pubDate"],
                                                       "fuente": dict_noticia["fuente"]})
            else:
                nuevo_diccionario_noticias[company] = [{"titulo":dict_noticia["titulo"],
                                                "link":dict_noticia["link"],
                                                       "summary": dict_noticia["summary"],
                                                       "pubDate": dict_noticia["pubDate"],
                                                       "fuente": dict_noticia["fuente"]}]
    write_companies_json(nuevo_diccionario_noticias)
    
