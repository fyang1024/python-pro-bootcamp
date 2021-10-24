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

coins = {
    "quarters": 0.25,
    "dimes": 0.10,
    "nickles": 0.05,
    "pennies": 0.01
}

revenue = 0


def report():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${revenue}")


def is_resources_sufficient(available_res, required_res):
    for key in available_res:
        if key in required_res and available_res[key] < required_res[key]:
            print(f"Sorry there is not enough {key}.")
            return False
    return True


def take_payment():
    print("Please insert coins.")
    total = 0
    for coin in coins:
        units = get_number_input(coin)
        total += float(units) * coins[coin]
    return total


def get_number_input(coin):
    """Ask user to input non-negative whole number"""
    while True:
        n = input(f"How many {coin}?:")
        try:
            if int(n) >= 0:
                print(f"Received {n} {coin}, or ${float(n) * coins[coin]}")
                return n
        except ValueError:
            print("Please enter a non-negative whole number, e.g., 0, 1, 2,...")


def is_payment_sufficient(cost, payment):
    """check if the payment is sufficient for the drink ordered."""
    if payment < cost:
        print("Sorry that's not enough money. Money refunded.")
        return False
    return True


def make_coffee(drink, ingredients):
    for key in resources:
        if key in ingredients:
            resources[key] -= ingredients[key]
    print(f"Here is your {drink}. Enjoy!")


is_on = True

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino):")
    if choice == 'off':
        print("Bye!")
        is_on = False
    elif choice == 'report':
        report()
    elif choice in MENU:
        ingredients = MENU[choice]["ingredients"]
        if is_resources_sufficient(resources, ingredients):
            payment = take_payment()
            print(f"Received ${payment}")
            cost = MENU[choice]["cost"]
            if is_payment_sufficient(cost, payment):
                revenue += cost
                change = round(payment - cost, 2)
                if change > 0.01:
                    print(f"Here is ${change} dollars in change.")
                make_coffee(choice, ingredients)
    else:
        print("Sorry I don't understand your instruction")
