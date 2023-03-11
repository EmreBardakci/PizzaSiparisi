import csv
import datetime
import os.path
# Menu.txt dosyasindan menü bilgilerini okuyarak, pizza tabanlari ve soslari listeler halinde döndüren fonksiyon
def read_menu():
    with open('Menu.txt', 'r') as f:
        menu_text = f.read()
    menu_lines = menu_text.split('\n')
    pizza_bases = []
    pizza_toppings = []
    in_pizza_bases = False
    in_pizza_toppings = False
    for line in menu_lines:
        if line.startswith(
'* Lütfen Bir Pizza Tabani Seçiniz:'
):
            in_pizza_bases = True
            continue
        elif line.startswith(
'* ve seçeceğiniz sos:'
):
            in_pizza_bases = False
            in_pizza_toppings = True
            continue
        elif line.startswith('*'):
            in_pizza_toppings = False
            continue
        if in_pizza_bases and line:
            pizza_bases.append(line.strip())
        elif in_pizza_toppings and line:
            pizza_toppings.append(line.strip())
    return pizza_bases, pizza_toppings

# Pizza sinifi
class Pizza:
    def __init__(self, description, cost):
        self._description = description
        self._cost = cost

    def get_description(self):
        return self._description
    
    def get_cost(self):
        return self._cost

# Klasik pizza sinifi
class KlasikPizza(Pizza):
    def __init__(self):
        super().__init__("Klasik pizza", 50)

# Margarita pizza sinifi
class MargaritaPizza(Pizza):
    def __init__(self):
        super().__init__("Margarita pizza", 60)

# Türk pizza sinifi
class TurkPizza(Pizza):
    def __init__(self):
        super().__init__("Türk pizza", 70)

# Sade pizza sinifi 
class SadePizza(Pizza):
    def __init__(self):
        super().__init__("Sade pizza", 80)        

# Decorator sinifi
class ToppingDecorator(Pizza):
    def __init__(self, pizza, topping):
        self._pizza = pizza
        self._topping = topping

    def get_description(self):
        return self._pizza.get_description() + ", " + self._topping.get_description()

    def get_cost(self):
        return self._pizza.get_cost() + self._topping.get_cost()

# Zeytin topping sinifi
class ZeytinTopping(Pizza):
    def __init__(self):
        super().__init__("Zeytin", 2)
        
# Mantar topping sinifi
class MantarTopping(Pizza):
    def __init__(self):
        super().__init__("Mantarlar", 3)
    
# Keçi peyniri topping sinifi
class KeciPeyniriTopping(Pizza):
    def __init__(self):
        super().__init__("Keçi peyniri", 4)
        
# Et topping sinifi
class EtTopping(Pizza):
    def __init__(self):
        super().__init__("Et", 5)

# Soğan topping sinifi
class SoganTopping(Pizza):
    def __init__(self):
        super().__init__("Soğan", 1)
        
# Mısır topping sinifi
class MisirTopping(Pizza):
    def __init__(self):
        super().__init__("Misir",6)

def save_order_to_database(username, tc, card_number, order_description, card_password):
    order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(order_time, order_description)
    fields = [username, tc, card_number, order_description, order_time, card_password]
    with open('Orders_Database.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        


def main():
    
    with open("Menu.txt", "r", encoding="utf-8") as menu_file:
        menu = menu_file.read()
    print(menu)

     
   # Pizza ve sos seçenekleri için kullanıcı girişi alma
    while True:
        try:
            pizza_choice = int(input("Please select a pizza: "))
            if pizza_choice < 1 or pizza_choice > 4:
                raise ValueError
            sauce_choice = int(input("Please select a sauce: "))
            if sauce_choice < 11 or sauce_choice > 16:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please try again.")

     
    #Pizza ve sosun toplam maliyetini hesaplama
    pizza = None
    sauce = None
    if pizza_choice == 1:
        pizza = KlasikPizza()
    elif pizza_choice == 2:
        pizza = MargaritaPizza()
    elif pizza_choice == 3:
        pizza = TurkPizza()
    elif pizza_choice == 4:
        pizza = SadePizza()
    if sauce_choice == 11:
        sauce = ZeytinTopping()
    elif sauce_choice == 12:
        sauce = MantarTopping()
    elif sauce_choice == 13:
        sauce = KeciPeyniriTopping()
    elif sauce_choice == 14:
        sauce = EtTopping()
    elif sauce_choice == 15:
        sauce = SoganTopping()
    elif sauce_choice == 16:
        sauce = MisirTopping()
    sauceCost = sauce.get_cost()
    pizzaCost = pizza.get_cost()
    total_cost = sauceCost + pizzaCost

    #Sipariş için kullanıcı bilgilerini alma 
    name = input("Please enter your name: ")
    tc_id = input("Please enter your TC identification number: ")
    cc_number = input("Please enter your credit card number: ")
    cc_cvv = input("Please enter your credit card CVV: ")
    order_discr = f"{pizza.get_description()} and {sauce.get_description()}"
    # Write order to Orders_Database.csv file
    save_order_to_database(name,tc_id,cc_number,order_discr,cc_cvv)

    
    #Baskı emri onayı ve toplam maliyet 
    print("Your order has been placed successfully!")
    print(f"Total cost: {total_cost:.2f} TL")

if __name__ == "__main__":
    if os.path.exists("/Orders_Database.csv"):
        
        fields = ['Username', 'TC', 'Card_Number', 'Order_Description', 'Order_Time', 'Card_Password']

        with open('Orders_Database.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
        main()
        
    else:
        main()