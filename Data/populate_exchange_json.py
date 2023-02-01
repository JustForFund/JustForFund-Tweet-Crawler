import json

with open("nyse_american.json", 'r', encoding="utf-8") as nyse_american_file:
	exchange_symbols = list(json.load(nyse_american_file).keys())
	print(exchange_symbols)