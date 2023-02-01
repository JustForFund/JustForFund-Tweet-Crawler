import json

palabras = []
all_stocks_dict = {}

with open("Filtros_Stocks.json", 'r', encoding="utf-8") as compiled_data_file:
    compiled_data_dict = json.load(compiled_data_file)
    lista_palabras = compiled_data_dict["palabras"]

with open("nasdaq_stocks.json", 'r', encoding="utf-8") as nasdaq_data_file:
    lista_borrar = ["inc", "dlt", "inc.", "limited", "corp.", "corp", "plc", "ltd."]
    nasdaq_data_dict = json.load(nasdaq_data_file)
    for symbol in nasdaq_data_dict.keys():
        palabras.append(nasdaq_data_dict[symbol]["Name"].lower())
        palabras.append(symbol)
        company = nasdaq_data_dict[symbol]["Name"].lower()
        lista_words = company.split(" ")
        lista_words_instance = company.lower().split(" ")
        for borrar in lista_borrar:
            if borrar in lista_words_instance:
                index_borrar = lista_words.index(borrar)
                del lista_words[index_borrar]
            company_words = " ".join(lista_words)
            company_words = company_words.replace(",", "")
            company = company_words
        all_stocks_dict[symbol] = company



with open("nyse_stocks.json", 'r', encoding="utf-8") as nyse_data_file:
    lista_borrar = [" inc", " dlt", " inc.", " limited", " corp.", " corp", " plc", " ltd.", " corporation", "incorporated", "group", "pharmaceutical", "holdings", "ltd", "laboratories", "therapeutics", "incorporated", "holding", "technologies"]
    nyse_data_dict = json.load(nyse_data_file)
    for symbol in nyse_data_dict.keys():
        palabras.append(nyse_data_dict[symbol]["Name"].lower())
        palabras.append(symbol)
        company = nyse_data_dict[symbol]["Name"].lower()
        lista_words = company.split(" ")
        lista_words_instance = company.lower().split(" ")
        for borrar in lista_borrar:
            if borrar in lista_words_instance:
                index_borrar = lista_words.index(borrar)
                del lista_words[index_borrar]
            company_words = " ".join(lista_words)
            company_words = company_words.replace(",", "")
            company = company_words
        all_stocks_dict[symbol] = company

"""
with open("Filtros_Stocks.json", 'w', encoding="utf-8") as final_compiled_data_file:
    nueva_lista_palabras = []
    lista_borrar = ["inc", "dlt", "inc.", "limited", "corp.", "corp", "plc", "ltd."]
    for palabra in palabras:
        lista_words = palabra.split(" ")
        lista_words_instance = palabra.lower().split(" ")
        for borrar in lista_borrar:
            if borrar in lista_words_instance:
                index_borrar = lista_words.index(borrar)
                del lista_words[index_borrar]
        index_palabrax = 0
        company_words = " ".join(lista_words)
        company_words = company_words.replace(",", "")
        nueva_lista_palabras.append(company_words)
    print(nueva_lista_palabras)
    compiled_data_dict["palabras"] = nueva_lista_palabras
    json.dump(compiled_data_dict, final_compiled_data_file)
"""
with open("all_stocks.json", 'w', encoding="utf-8") as final_compiled_data_file:
    json.dump(all_stocks_dict, final_compiled_data_file)