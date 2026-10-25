from tabulate import tabulate
#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
    
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    def get_cost(self):
        return self.cost
    
    def get_quantity(self):
        return self.quantity
    
    def __str__(self):

        return (f"{self.code:<10} {self.product:<25} {self.country:<15} R{self.cost} {self.quantity:>5}")

#=============Shoe list===========

shoe_list = []

#==========Functions outside the class==============




def read_shoes_data(): 
    '''Reads from inventory.txt to populate shoe_list'''

    try:
        with open('inventory.txt', 'r') as inventory:
            lines = inventory.readlines()
            for line in lines[1:]:
                country, code, product, cost, quantity = line.strip().split(',')
                shoe_list.append(Shoe(country, code, product, int(cost), int(quantity)))
    
    except FileNotFoundError:
        print('Error: inventory.txt could not be found.')    



def capture_shoes():
    '''Adds new shoe to shoe_list '''

    country = input('Enter the country: ')
    code = input('Enter the code: ').upper()
    product = input('Enter the product: ')
    while True:
        try:
            cost = int(input('Enter the cost: R'))
            quantity = int(input('Enter the quantity: '))
            break
        except ValueError:
            print('Invalid entry for either cost or quantity')
    shoe_list.append(Shoe(country, code, product, cost, quantity))
    print(f'\n{product} has been added to the inventory')



def view_all():
    '''Prints to view the inventory of shoes'''
    
    if not shoe_list:
        print('Shoe list is empty.')
        return
    
    row = []
    for shoe in shoe_list:
        row.append([shoe.country, shoe.code, shoe.product, f'R{shoe.cost}', shoe.quantity])
    print('\n' + tabulate(row, headers = ['Country', 'Code', 'Product', 'Cost', 'Quantity']))



def re_stock():
    ''' Sorts through shoe_list to find lowest quantity and asks user 
    whether they would like to add to the quantity of lowest quantity product'''

    if not shoe_list:
        print('Shoe list is empty.')
        return
    
    lowest_quantity = min(shoe_list, key=lambda shoe: shoe.quantity)
    print(lowest_quantity)
    user_choice = input(f'\nWould you like to restock {lowest_quantity.product}? (yes/no): ')
    if user_choice.lower() == 'yes':
        while True:
            try:
                new_quantity = int(input('\nPlease enter quantity you want to restock: '))
                lowest_quantity.quantity += new_quantity
                try:
                    with open('inventory.txt', 'w') as inventory:
                        inventory.write('Country,Code,Product,Cost,Quantity\n')
                        for shoe in shoe_list:
                            inventory.write(f'{shoe.country},{shoe.code},{shoe.product},{shoe.cost},'
                                            f'{shoe.quantity}\n')
                        print(f'\n{lowest_quantity.product} quantity has been successfully updated.')
                except FileNotFoundError as error:
                    print(error)
                break

            except ValueError:
                print('You entered an invalid quantity please try again.')
    else:
        print('No changes made.')


def search_shoe():
    '''Returns a shoe that the user searches for by entering the shoe code'''

    user_search_input = input('\nEnter shoe code: ').strip().upper()

    for shoe in shoe_list:
        if user_search_input == shoe.code:
            return shoe
    return None



def value_per_item():
    '''Calculates the total value for each product in shoe_list and prints them in a table'''
    
    if not shoe_list:
        print('Shoe list is empty.')
        return
    
    row = []
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        row.append([shoe.product, f'R{value}'])
    print('\n' + tabulate(row, headers=['Product', 'Value per item']))



def highest_qty():
    '''Looks for the shoe with the highest quantity and prints that it is for sale.'''
    if not shoe_list:
        print('Shoe list is empty')
        return
    
    highest_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)
    print(f'\n{highest_shoe.product} is for sale! {highest_shoe.quantity} in stock.')

#==========Main Menu=============
print(r"""
   ____  _                   ____  _             _
  / ___|| |__   ___   ___   / ___|| |_ ___   ___| | __
  \___ \| '_ \ / _ \ / _ \  \___ \| __/ _ \ / __| |/ /
   ___) | | | | (_) |  __/   ___) | || (_) | (__|   <
  |____/|_| |_|\___/ \___|  |____/ \__\___/ \___|_|\_\

                     _______
                ____/ o  o  \__________
               /    o  o  o            \___
              |_________________________ __)
              \___________________________/

          ~ Inventory Manager: every pair counted ~
""")
read_shoes_data()
while True:
    print('''
Please choose an option:
1. View all shoes
2. Add a new shoe
3. Restock the lowest-stock shoe
4. Search for a shoe by code
5. View the total value of each shoe
6. View the shoe that's for sale
7. Exit
''')
    choice = input('Enter a number (1-7): ')

    if choice == '1':
        view_all()

    elif choice == '2':
        capture_shoes()

    elif choice == '3':
        re_stock()

    elif choice == '4':
        shoe = search_shoe()

        if shoe is None:
            print('No shoe found with that code.')
        else:
            print(f'Shoe found:\n{shoe}')

    elif choice == '5':
        value_per_item()

    elif choice == '6':
        highest_qty()

    elif choice == '7':
        print('\nGoodbye!')
        break
    
    else:
        print('\nInvalid choice. Please enter a number from 1 to 7.')