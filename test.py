import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *   
import datetime
import time
from tkinter import messagebox

import menuDB
import os
from openpyxl import load_workbook

from tkcalendar import Calendar, DateEntry

#basic layout of page
root = tk.Tk() #initialise window
root.title("Home") #create window
root.config(bg = 'white') #change background color
root.minsize(800, 500) #set size of window 

#declarations
day = datetime.datetime.today().weekday()
storemenuDict = {}

#todayStores_dup = []
#todayStores = [] 
#todayValues = []
#todayKeys = []
storesOpenList = []

#declare variables
stall = ""
opentime = 0
closetime = 0
time1 = ''
xlsxFileLocation = r'D:\NTU\CZ1003 Intro to Computational Thinking\Proj\North Spine Canteen Details.xlsx'

wb = load_workbook(xlsxFileLocation) #load excel
openinghours = wb['opening hours']
food = wb['food']
storeinfo = wb['store information']
menu = {}
menuDict = {}
storeOpen = {}
storeOpenDict = {}

def excelConversion():                                         #Parses through the excel and generates 2 dictionaries: menu, storeOpen
    wb = load_workbook(xlsxFileLocation)

    openinghours = wb['opening hours']                                          #opening hours sheet
    food = wb['food']                                                           #food sheet
    storeinfo = wb['store information']                                         #store information sheet
    menu = {}
    storeOpen = {}

    for row in range(2, food.max_row):                                          #parses information in food sheet and converts to dictionary
        key = (food.cell(row, 1).value, food.cell(row, 2).value)
        menu.update({key : food.cell(row, 3).value})

    DayDict = {}
    PreviousStore = openinghours.cell(2, 1).value

    for row in range(2, openinghours.max_row):                                   #iterates through the rows of opening hours sheet
        if (openinghours.cell(row, 1).value != PreviousStore):                   #if the name of the store changes, update dictionary with store name and the days that the store is open
            storeOpen.update({PreviousStore : DayDict})
            PreviousStore = openinghours.cell(row, 1).value
            DayDict = {}                                                         #Clear dictionary

        if ((openinghours.cell(row, 2).value) == 'Weekdays'):           #Update DayDict with key as the day of the week(0 = Monday ... 6 = Sunday) and the value as a tuple with (opening hours, closing hours)
            for n in range(0, 5):
                DayDict.update({n : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Weekends'):
            for n in range(5, 7):
                DayDict.update({n : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Monday'):
            DayDict.update({1 : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Tuesday'):
            DayDict.update({1 : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Wednesday'):
            DayDict.update({2 : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Thursday'):
            DayDict.update({3 : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Friday'):
            DayDict.update({4 : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Saturday'):
            DayDict.update({5 : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

        if ((openinghours.cell(row, 2).value) == 'Sunday'):
            DayDict.update({6 : (openinghours.cell(row, 3).value, openinghours.cell(row, 4).value)})

    return menu, storeOpen      #format of menu dictionary --> {(Store Name, Food Name) : Price} | format of storeOpen dictionary --> {Store Name : {Day of week, (Opening Time, Closing Time)}}

def userInput():
    global userInputStore
    foodname = userInputStore.get()
    #storename = userInputStore.get()
    window = tk.Toplevel(root)
    window.title("Price") #create window
    window.config(bg = 'white') #change background color
    window.minsize(300, 30) #set size of window 

    storemenuDict = {}
    for n in menuDict:
        if foodname.lower() == n[1].lower() or foodname == n[1]:
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(window, text = "The price of " + '\n'.join(storemenuDict) + " is: ", font = h3, bg = "white").place(x = 60, y = 50)
            Label(window, text = "$" + '\n'.join(map(str, allprices)), font = h1, bg = "white").place(x = 120, y = 80)
            print(storemenuDict)

    #storemenuDict = {}
    #for n in menuDict:
    #    if storename.lower() == n[0].lower(): 
    #        storemenuDict.update({n[1] : menuDict[n]})
    #        allprices = [v for v in storemenuDict.values()]
    #        Label(window, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 70)
    #        Label(window, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 370, y = 70)
userInputStore = StringVar()

def allstores():
    window = tk.Toplevel(root)
    window.config(bg = "white")
    window.title("All Stores")
    window.minsize(600, 450) #set size of window 
    #Label(window, text = "The stores opened today are:", font = h1, bg = "white").place(x = 10, y = 70)

    #for n in storeOpenDict:
    #   if day in storeOpenDict[n]:
    #        storesOpenList.append(n)
    #        todayLabel = Label(window, text = '\n'.join(storesOpenList), font = h3, bg = "white")
    #        todayLabel.place(x = 20, y = 100)
            #Button(window, text = storesOpenList).pack(fill = 'both')

    style = ttk.Style()
    style.configure("TButton", font = ("Century Gothic", 12, 'bold'), foreground = "#3366CC", background = 'white', width = "17")
    ttk.Button(window, text = "MINI WOK", style = "TButton", command = miniwokbtn).place(x = 30, y = 90)
    ttk.Button(window, text = "YONG TAU FOO", style = "TButton", command = yongtaufoobtn).place(x = 210, y = 90)
    ttk.Button(window, text = "CHICKEN RICE", style = "TButton", command = chickricebtn).place(x = 390, y = 90)
    ttk.Button(window, text = "NOODLES", style = "TButton", command = noodlesbtn).place(x = 30, y = 150)
    ttk.Button(window, text = "MIXED RICE", style = "TButton", command = mixedricebtn).place(x = 210, y = 150)
    ttk.Button(window, text = "WESTERN", style = "TButton", command = westernbtn).place(x = 390, y = 150)
    ttk.Button(window, text = "DRINKS", style = "TButton", command = drinksbtn).place(x = 30, y = 210)
    ttk.Button(window, text = "SOUP DELIGHT", style = "TButton", command = soupbtn).place(x = 210, y = 210)
    ttk.Button(window, text = "MALAY BBQ", style = "TButton", command = malaybtn).place(x = 390, y = 210)
    ttk.Button(window, text = "VEGETARIAN", style = "TButton", command = vegetarianbtn).place(x = 30, y = 270)
    ttk.Button(window, text = "SALAD", style = "TButton", command = saladbtn).place(x = 210, y = 270)
    ttk.Button(window, text = "PASTA", style = "TButton", command = pastabtn).place(x = 390, y = 270)
    ttk.Button(window, text = "LONG JOHN SILVER", style = "TButton", command = longjohnbtn).place(x = 30, y = 330)
    ttk.Button(window, text = "MCDONALDS", style = "TButton", command = macbtn).place(x = 210, y = 330)

    Label(window, text = "Please search for a food: ", font = h3, bg = "white").place(x = 30, y = 30)
    Entry(window, textvariable = userInputStore).place(x = 240, y = 35)
    #go = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn 1.png")
    Button(window, text = "Go!", bg = "silver", relief = FLAT, command = userInput, width = 4, height = 1).place(x = 380, y = 30)
    #Label(window, text = todaysMenu, font = h1, bg = "white").place(x = 10, y = 100)

def custom():
    window2 = tk.Toplevel(root)
    window2.config(bg = "white")
    window2.title("All Stores")
    window2.minsize(600, 500) #set size of window 
    Label(window2, text = "Here is a list of all the available stores in North Spine:", font = h1, bg = "white").place(x = 10, y = 30)
    style = ttk.Style()
    style.configure("TButton", font = ("Century Gothic", 12, 'bold'), foreground = "#3366CC", background = 'white', width = "15")


def miniwokbtn():
    store = "Mini Wok"

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    miniwokpop = tk.Tk()
    miniwokpop.minsize(400, 500)
    miniwokpop.config(bg = "white")
    miniwokpop.title(store)
    oplabel = Label(miniwokpop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(miniwokpop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(miniwokpop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(miniwokpop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(miniwokpop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(miniwokpop, text = "Okay", command = miniwokpop.destroy)
    okbtn.place(x = 155, y = 450)

def yongtaufoobtn():
    store = "Yong Tau Foo"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    yongtaufoopop = tk.Tk()
    yongtaufoopop.minsize(400, 400)
    yongtaufoopop.config(bg = "white")
    yongtaufoopop.title(store)
    oplabel = Label(yongtaufoopop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(yongtaufoopop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(yongtaufoopop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 140, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(yongtaufoopop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(yongtaufoopop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(yongtaufoopop, text = "Okay", command = yongtaufoopop.destroy)
    okbtn.place(x = 155, y = 350)

def chickricebtn():
    store = "Chicken Rice"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    chickricepop = tk.Tk()
    chickricepop.minsize(400, 350)
    chickricepop.config(bg = "white")
    chickricepop.title(store)
    oplabel = Label(chickricepop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(chickricepop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(chickricepop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(chickricepop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(chickricepop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(chickricepop, text = "Okay", command = chickricepop.destroy)
    okbtn.place(x = 155, y = 300)

def noodlesbtn():
    store = "Noodles"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    noodlespop = tk.Tk()
    noodlespop.minsize(400, 420)
    noodlespop.config(bg = "white")
    noodlespop.title(store)
    oplabel = Label(noodlespop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(noodlespop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(noodlespop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(noodlespop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(noodlespop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 280, y = 100)

    okbtn = Button(noodlespop, text = "Okay", command = noodlespop.destroy)
    okbtn.place(x = 155, y = 370)

def mixedricebtn():
    store = "Mixed Rice"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    mixedricepop = tk.Tk()
    mixedricepop.minsize(320, 300)
    mixedricepop.config(bg = "white")
    mixedricepop.title(store)
    oplabel = Label(mixedricepop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(mixedricepop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(mixedricepop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 125, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(mixedricepop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(mixedricepop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 200, y = 100)

    okbtn = Button(mixedricepop, text = "Okay", command = mixedricepop.destroy)
    okbtn.place(x = 125, y = 240)

def westernbtn():
    store = "Western"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    westernpop = tk.Tk()
    westernpop.minsize(400, 370)
    westernpop.config(bg = "white")
    westernpop.title(store)
    oplabel = Label(westernpop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(westernpop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(westernpop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(westernpop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(westernpop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(westernpop, text = "Okay", command = westernpop.destroy)
    okbtn.place(x = 155, y = 270)

def drinksbtn():
    store = "Drinks"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    drinkspop = tk.Tk()
    drinkspop.minsize(400, 550)
    drinkspop.title(store)
    drinkspop.config(bg = "white")
    oplabel = Label(drinkspop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(drinkspop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(drinkspop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(drinkspop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(drinkspop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(drinkspop, text = "Okay", command = drinkspop.destroy)
    okbtn.place(x = 155, y = 500)

def soupbtn():
    store = "Soup Delight"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    souppop = tk.Tk()
    souppop.minsize(400, 400)
    souppop.title(store)
    souppop.config(bg = "white")
    oplabel = Label(souppop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(souppop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(souppop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(souppop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(souppop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(souppop, text = "Okay", command = souppop.destroy)
    okbtn.place(x = 155, y = 350)


def malaybtn():
    store = "Malay BBQ"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    malaypop = tk.Tk()
    malaypop.minsize(400, 360)
    malaypop.title(store)
    malaypop.config(bg = "white")
    oplabel = Label(malaypop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(malaypop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(malaypop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(malaypop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(malaypop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(malaypop, text = "Okay", command = malaypop.destroy)
    okbtn.place(x = 155, y = 300)

def vegetarianbtn():
    store = "Vegetarian"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    vegetarianpop = tk.Tk()
    vegetarianpop.minsize(400, 330)
    vegetarianpop.title(store)
    vegetarianpop.config(bg = "white")
    oplabel = Label(vegetarianpop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(vegetarianpop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(vegetarianpop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(vegetarianpop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(vegetarianpop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(vegetarianpop, text = "Okay", command = vegetarianpop.destroy)
    okbtn.place(x = 155, y = 270)

def saladbtn():
    store = "Salad"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    saladpop = tk.Tk()
    saladpop.minsize(400, 400)
    saladpop.title(store)
    saladpop.config(bg = "white")
    oplabel = Label(saladpop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(saladpop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(saladpop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(saladpop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(saladpop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(saladpop, text = "Okay", command = saladpop.destroy)
    okbtn.place(x = 155, y = 350)

def pastabtn():
    store = "Pasta"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    pastapop = tk.Tk()
    pastapop.minsize(400, 550)
    pastapop.config(bg = "white")
    pastapop.title(store)
    oplabel = Label(pastapop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(pastapop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(pastapop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(pastapop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(pastapop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(pastapop, text = "Okay", command = pastapop.destroy)
    okbtn.place(x = 155, y = 500)

def longjohnbtn():
    store = "Long John Silver"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    ljspop = tk.Tk()
    ljspop.minsize(450, 470)
    ljspop.title(store)
    ljspop.config(bg = "white")
    oplabel = Label(ljspop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(ljspop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(ljspop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(ljspop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(ljspop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 350, y = 100)

    okbtn = Button(ljspop, text = "Okay", command = ljspop.destroy)
    okbtn.place(x = 155, y = 400)
    
def pizzabtn():
    store = "Pizza Hut"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    pizzapop = tk.Tk()
    pizzapop.minsize(500, 500)
    pizzapop.title(store)
    pizzapop.config(bg = "white")
    oplabel = Label(pizzapop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(pizzapop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(pizzapop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(pizzapop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(pizzapop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(pizzapop, text = "Okay", command = pizzapop.destroy)
    okbtn.place(x = 155, y = 450)
    
def macbtn():
    store = "McDonalds"
    storemenuDict = {}

    opentime = storeOpenDict[store][day][0]
    closetime = storeOpenDict[store][day][1]

    macpop = tk.Tk()
    macpop.minsize(400, 440)
    macpop.title(store)
    macpop.config(bg = "white")
    oplabel = Label(macpop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 15, y = 20)
    ophours = Label(macpop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 20)
    menulabel = Label(macpop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 155, y = 60)

    for n in menuDict:
        if store in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(macpop, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(macpop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 300, y = 100)

    okbtn = Button(macpop, text = "Okay", command = macpop.destroy)
    okbtn.place(x = 155, y = 400)

def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')

    if time2 != time1:
        time1 = time2
        clock.config(text = time2)

    clock.after(10, tick)

#parse all info in food worksheet and put into dictionary
for row in range(2, food.max_row):
    key = (food.cell(row, 1).value, food.cell(row, 2).value)
    menu.update({key : food.cell(row, 3).value})

# Font Styling
h1 = ("Century Gothic", 14, "bold")
h2 =  ("Century Gothic", 12, "bold")
h3Italic = ("Century Gothic", 11, "italic")
h3 =  ("Century Gothic", 11)
h3Bold = ("Century Gothic", 11, "bold")

menuDict, storeOpenDict = excelConversion()
# Main Frames
left_frame = Frame(root, width = 220, height = 150)
left_frame.grid(row = 0, column = 0, pady = 20, padx = 40)

left_frame2 = Frame(root, width = 220, height = 150)
left_frame2.grid(row = 1, column = 0, pady = 23, padx = 30)

# Position Axis
w = 300
h = 200
x = 50
y = 100
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

# Frame in Left Frame + Content
Label(left_frame, text = "Hello! Today is...", font = h1).place(x = 35, y = 20)
Label(left_frame2, text = "Customisation", font = h1).place(x = 38, y = 20)

# Left frame content
now = datetime.datetime.now()
currentdate = now.strftime("%d %b %Y")
currentime = now.strftime("%I:%M:%S %p")

Label(left_frame, text = currentdate, font = h3Italic).place(x = 60, y = 70)
clock = Label(left_frame, font = h3Italic)
clock.place(x = 68, y = 100)

#calendar
Label(left_frame2, text = 'Choose date', font = ("Century Gothic", 10)).place(x = 10, y = 60)
cal = DateEntry(left_frame2, background='darkblue', foreground='white')
cal.place(x = 110, y = 60)

#time
Label(left_frame2, text = "Choose time", font = ("Century Gothic", 10)).place(x = 10, y = 100)

# Right frame content
Label(text = "WELCOME TO NTU'S CANTEEN MASTER", font = h2, bg = "white").place(x = 300, y = 30)
Label(text = "I want to...", font = h3, bg = "white").place(x = 300, y = 80)

todaybtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn2.png")
Button(image = todaybtn, bg = "white", relief = FLAT, command = allstores).place(x = 300, y = 120)
#todaybtn.grid(row = 0, column = 0 )
allbtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn12.png")
Button(image = allbtn, bg = "white", relief = FLAT, command = custom).place(x = 450, y = 120)
#allbtn.pack(side = LEFT)
exitbtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn3.png")
Button(image = exitbtn, bg = "white", relief = FLAT, command = root.destroy).place(x = 600, y = 120)

# About Canteen Master
Label(text = "ABOUT  US", font = h2, bg = "white").place(x = 430, y = 200)
abtusbtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn 4.png")
Button(image = abtusbtn, bg = "white", relief = FLAT).place(x = 280, y = 230)

tick()
root.mainloop() #display window until user closes it