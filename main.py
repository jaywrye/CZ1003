import datetime
import menuDB

day = datetime.datetime.today().weekday()                                         # Get current day of the week: Monday = 0, Tuesday = 1, Wednesday = 2 ... Sunday = 6
todaysMenu = {}                                                                   # Empty dictionary to store menu

for n in menuDB.storeList:                                                        # Print out all the stores from storeList
    print(n)

while True:                                                                       # Endless loop until user enters correct store name
    userInputStore = input("Enter the store name: ")
    try:
        menuDB.storeList.index(userInputStore)
        break;
    except:
        print("No such store")
        continue;

for n in menuDB.menu:
    if (n[0] == userInputStore and (n[1] == 7 or n[1] == day)):                  # n is a tuple, n[0] is the store name, n[1] is the day of the week; If n[1] has 7, it means it is available everyday
        todaysMenu.update({n[2] : menuDB.menu[(userInputStore, n[1], n[2])]})  # adds the name of the food item that is available today as the key and the price of that food item as the value into the todaysMenu to create a new dict
        print(n[2])                                                            # print out the food items available today

while True:
    userInputFood = input("Enter the food name: ")   
    if userInputFood in todaysMenu:
        print("Price: ${:.2f}".format(todaysMenu[userInputFood]))
        break;
    else:
        print("No such food in today's menu")
        continue;
