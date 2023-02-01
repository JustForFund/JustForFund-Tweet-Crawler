import json

with open("NYSE_American.txt", "r") as stock_exchange_file:
	dict_stock_echange_listings = dict()
	for line in stock_exchange_file:
		list_elems_line = line.split("	")
		symbol = list_elems_line[1]
		name_company = list_elems_line[0]
		dict_stock_echange_listings[symbol] = name_company

with open("all_stocks.json", 'r', encoding="utf-8") as compiled_data_file:
    compiled_data_dict = json.load(compiled_data_file)
    for symbol, name_company in dict_stock_echange_listings.items():
    	compiled_data_dict[symbol] = name_company

with open("all_stocks.json", 'w', encoding="utf-8") as compiled_data_file:
    compiled_data_dict = json.dump(compiled_data_dict,compiled_data_file)
