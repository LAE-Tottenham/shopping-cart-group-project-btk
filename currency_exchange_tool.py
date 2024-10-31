import requests

def fetch_exchange_rate(currency):
    api_key = "afb6b9a93110e7e55e8e5c0a"
    base_currency = 'GBP'

    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        rate = data['conversion_rates'][currency]
        return rate
    else:
        print("Error:", data['error-type'])


exchange_rates = {
    "USD": fetch_exchange_rate("USD"),
    "EUR": fetch_exchange_rate("EUR"),
    "CAD": fetch_exchange_rate("CAD"),
    "BDT": fetch_exchange_rate("BDT"),
    "TRY": fetch_exchange_rate("TRY")
}
#print(exchange_rates["TRY"])

def check_currency_exists(currency):
    return currency in exchange_rates.keys()

def convert_currency(target_currency, amount):
    exchange_rate = exchange_rates[target_currency]
    return exchange_rate * amount


#---------------------------------------------------------------------------------------------------------------------------------------

def main(currency, amount):
    if not check_currency_exists(currency.upper()): return currency.upper() == "GBP" and amount or -1

    return convert_currency(currency, amount)
#print(main("GBP", 100))


