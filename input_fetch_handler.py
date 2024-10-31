import re
from random import randint as random

with open("products.txt", "r") as products_file:
    products = {product.split(": ")[0]: product.split(": ")[1] for product in products_file.read().split("\n")}

#---------------------------------------------------------------------------------------------------------------------------------------------

#input validation functions

def validate_chosen_products(response):
    global products
    #check if the response contains anything other than letters and commas
    if re.search(r'[^a-zA-Z,]', response.replace(" ", "")):
        return False  #invalid characters found
    else:

        #check if all chosen products exist
        chosen_products = response.replace(" ", "").split(",")
        for product in chosen_products:
            if not product in products:
                return False
        return True  #only letters and commas

def validate_postcode(response):
    return re.match(r"^[A-Z]{1,2}\d{1,2}[A-Z]?\s\d[A-Z]{2}$", response.upper())



#---------------------------------------------------------------------------------------------------------------------------------------------

def request_input(prompt, validation_object):
    global products
    #validation object is either a table containing all accepted responses or a function that returns true or false

    while True:
        response = input(prompt)

        if callable(validation_object):
            if validation_object(response):
                return response
            else:
                print("\ninvalid input, please retry\n\n")
        else:
            if response.lower() in validation_object:
                return response
            else:
                print("\ninvalid input, please retry\n\n")


def fetch_user_inputs():
    global products

    #fetch what the user wants to purchase
    chosen_products = request_input("type in the products you wish to purchase, separating each one with a comma\n", validate_chosen_products)

    #postcode
    postcode = request_input("\nenter the postcode for your purchase to be delivered to\n", validate_postcode)

    #delivery time slot
    available_slots = [f"({i + 1}) {time}" for i, time in enumerate(["9:00-12:00", "12:00-15:00", "15:00-18:00"])]
    #print([slot + 1 for slot in range(len(available_slots))])
    conv_time_slot = request_input(f"\nyour product can be delivered during the following times:\n\n{"\n".join(available_slots)}\n\nenter the number of the most suitable time slot\n", [str(slot + 1) for slot in range(len(available_slots))])#1, 2... n
    conv_time_slot = available_slots[int(conv_time_slot) - 1]

    #visa or mastercard
    v_or_m = request_input("\nwill you use visa or mastercard?\n", ["visa", "mastercard"])

    #currency to pay with
    currency = request_input("\nenter the preferred currency to pay with from this list:\n\nGBP\nUSD\nCAD\nBDT\nTRY\n\n", ["gbp", "usd", "cad", "bdt", "try"])

    return chosen_products, postcode, conv_time_slot, v_or_m, currency