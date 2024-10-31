from currency_exchange_tool import main as exchange
from input_fetch_handler import fetch_user_inputs
import requests
import sys
import math
import pyfiglet

#---------------------------------------------------------------------------------------------------------------------------------------------
#functions

def calculate_distance_from_laet(postcode):
    global laet_latitude_longitude

    #convert the postcode to longitude and latitude using an api

    postcode = postcode.replace(" ", "%20")
    url = f"http://api.postcodes.io/postcodes/{postcode}"
    

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 200:
            result = data['result']
            latitude = result['latitude']
            longitude = result['longitude']
            postcode_latitude_longitude = (latitude, longitude)

            #1 = postcode, 2 = laet
            lat1, lon1 = map(math.radians, postcode_latitude_longitude)
            lat2, lon2 = map(math.radians, laet_latitude_longitude)

            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
            c = 2 * math.asin(math.sqrt(a))

            # radius of earth in kilometers
            r = 6371.0

            distance = r * c
            return distance
    print("\nthere was an error calculating shipping costs. Please try again later")
    sys.exit()

def calculate_shipping_cost(distance):
    return distance * 0.0243098545093845434395948508950459495845904589450980000000000000000000000000000000000000000000000001

def calculate_total(chosen_products):
    global products

    total = sum([float(products[product]) for product in chosen_products])
    return total

def output_data():
    global raw_total
    global shipping_cost

    global currency

    global postcode
    global distance
    global conv_time_slot

    global chosen_products

    total = raw_total + shipping_cost
    if (total < 10) or ((total > 1000)) and (currency != "GBP"):
        if input(f"you must spend {total < 10 and "at least £10 GBP" or "under £1000 GBP"} to purchase in other currencies. Would you like to continue in GBP?").lower() == "yes":
            symbol = "£"
            exchanged_full_total = round(raw_total + shipping_cost, 2)
            exchanged_raw_total = round(raw_total, 2)
            exchanged_shipping_cost = round(shipping_cost, 2)
        else:
            sys.exit()
    else:
        symbol = currency_symbols[currency]
        exchanged_full_total = round(exchange(currency, raw_total + shipping_cost), 2)
        exchanged_raw_total = round(exchange(currency, raw_total), 2)
        exchanged_shipping_cost = round(exchange(currency, shipping_cost), 2)

    #convert all monetary values before displaying
    print(f"total cost:\n{symbol}{exchanged_full_total} {currency}\n({v_or_m} {symbol}{exchanged_raw_total} + {symbol}{exchanged_shipping_cost} shipping)\n")
    
    print(f"delivery address:\n{postcode} ({round(distance, 3)} kilometres)\n")
    print(f"your chosen time slot for delivery is:\n{conv_time_slot}\n")

    print(f"your order:\n{"\n".join(chosen_products)}")


#---------------------------------------------------------------------------------------------------------------------------------------------
#variables

currency_symbols = {
    'GBP': "£",
    'USD': "$",
    'CAD': "$",
    'BDT': "৳",
    'TRY': "₺",
}

laet_latitude_longitude = (51.6042, -0.067574)

with open("products.txt", "r") as products_file:
    products_data = products_file.read().splitlines()
    products = dict(sorted([(line.split(": ")[0], line.split(": ")[1]) for line in products_data]))


#---------------------------------------------------------------------------------------------------------------------------------------------
#main


#display all options
print('please select what you would like to buy:\n')
for option in dict.fromkeys(products): print(option + "\n£" + products[option] + "\n")

#fetch all required inputs
chosen_products, postcode, conv_time_slot, v_or_m, currency = fetch_user_inputs()

#format inputs
chosen_products = chosen_products.replace(" ", "").split(",")
postcode = postcode.upper()
conv_time_slot = conv_time_slot[4:]
currency = currency.upper()

#calculate information using the inputs
distance = calculate_distance_from_laet(postcode)
shipping_cost = calculate_shipping_cost(distance)
raw_total = calculate_total(chosen_products)

#output
print("\ninformation about your purchase:\n")
output_data()
print("\n\n")

#pyfiglet.figlet_format()