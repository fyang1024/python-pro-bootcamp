MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

currency_value = {
    "quarters": 0.25,
    "dimes": 0.10,
    "nickles": 0.05,
    "pennies": 0.01
}

money = 0


def report():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${money}")


def check_resources(drink):
    ingredients = MENU[drink]["ingredients"]
    for key in resources:
        if key in ingredients and resources[key] < ingredients[key]:
            print(f"Sorry there is not enough {key}.")
            return False
    return True


def take_money():
    total = 0
    for currency in currency_value:
        units = get_number_input(currency)
        total += float(units) * currency_value[currency]
    return total


def get_number_input(units):
    while True:
        n = input(f"Please insert {units}:")
        try:
            if int(n) >= 0:
                print(f"Received {n} {units}, or ${float(n) * currency_value[units]}")
                return n
        except ValueError:
            print("Please enter a non-negative whole number, e.g., 0, 1, 2,...")


def check_money(drink, money_inserted):
    if money_inserted < MENU[drink]["cost"]:
        print("Sorry that's not enough money. Money refunded.")
        return False
    return True


def make_coffee(drink):
    ingredients = MENU[drink]["ingredients"]
    for key in resources:
        if key in ingredients:
            resources[key] -= ingredients[key]
    print(f"Here is your {drink}. Enjoy!")


while True:
    choice = input("What would you like? (espresso/latte/cappuccino):")
    if choice == 'off':
        print("Bye!")
        exit()
    elif choice == 'report':
        report()
    elif choice in MENU:
        if check_resources(choice):
            money_taken = take_money()
            print(f"Received ${money_taken}")
            if check_money(choice, money_taken):
                money += MENU[choice]["cost"]
                change = money_taken - MENU[choice]["cost"]
                if change > 0.01:
                    print(f"Here is ${change} dollars in change.")
                make_coffee(choice)
    else:
        print("Sorry I don't understand your instruction")
