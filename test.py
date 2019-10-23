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
    storename = userInputStore.get()
    window = tk.Toplevel(root)
    window.title(storename + "'s Menu") #create window
    window.config(bg = 'white') #change background color
    window.minsize(700, 600) #set size of window 

    Label(window, text = storename + "'s Menu", font = h1, bg = "white").place(x = 120, y = 20)

    #for n in menuDB.menu:
    #   if storename in n:                  # n is a tuple, n[0] is the store name, n[1] is the day of the week; If n[1] has 7, it means it is available everyday
    #        storemenudict.update({n[2] : menuDB.menu[n]})
            #todayList = storemenudict.values()
            #todaykeys = storemenudict.keys()
            #keys, values = zip(*storemenudict.items())
    #        todayKeys = [k for k in storemenudict.keys()]
    #        todayValues = [v for v in storemenudict.values()]
    #        Label(window, text = todayKeys, font = h3, bg = "white").place(x = 10, y = 100)
    #        Label(window, text = todayValues,  font = h3, bg = "white").place(x = 10, y = 200)

    storemenuDict = {}
    for n in menuDict:
        if storename in n: 
            storemenuDict.update({n[1] : menuDict[n]})
            allprices = [v for v in storemenuDict.values()]
            Label(window, text = '\n'.join(storemenuDict), font = h3, bg = "white").place(x = 10, y = 100)
            Label(window, text = '\n'.join(map(str, allprices)), font = h3, bg = "white").place(x = 400, y = 100)

print(menuDict)
userInputStore = StringVar()

def todaystores():
    window = tk.Toplevel(root)
    window.config(bg = "white")
    window.title("Today's Stores")
    window.minsize(600, 600) #set size of window 
    Label(window, text = "The stores opened today are:", font = h1, bg = "white").place(x = 10, y = 70)

    for n in storeOpenDict:
       if day in storeOpenDict[n]:
            storesOpenList.append(n)
            Label(window, text = '\n'.join(storesOpenList), font = h3, bg = "white").place(x = 20, y = 100)

    #list of all stores open today. if stall is duplicated, remove.
    #for n in menuDB.storeOpen:
    #    if day in menuDB.storeOpen[n][0]:
    #        todayStores_dup.append(n)
    #        for i in todayStores_dup:
    #            if i not in todayStores:
    #                todayStores.append(i)
    #        Label(window, text = ', '.join(todayStores), font = h3, bg = "white").place(x = 50, y = 110)

    Label(window, text = "Please enter the name of the store: ", font = h3, bg = "white").place(x = 10, y = 30)
    Entry(window, textvariable = userInputStore).place(x = 280, y = 35)
    #go = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn 1.png")
    Button(window, text = "Go!", bg = "silver", relief = FLAT, command = userInput, width = 4, height = 1).place(x = 430, y = 30)
    #Label(window, text = todaysMenu, font = h1, bg = "white").place(x = 10, y = 100)

def allstores():
    window2 = tk.Toplevel(root)
    window2.config(bg = "white")
    window2.title("All Stores")
    window2.minsize(600, 500) #set size of window 
    Label(window2, text = "Here is a list of all the available stores in North Spine:", font = h1, bg = "white").place(x = 10, y = 30)
    style = ttk.Style()
    style.configure("TButton", font = ("Century Gothic", 12, 'bold'), foreground = "#3366CC", background = 'white', width = "15")
    ttk.Button(window2, text = "CAI PNG", style = "TButton", command = caipngbtn).place(x = 30, y = 90)
    ttk.Button(window2, text = "TZE CHAR", style = "TButton", command = tzecharbtn).place(x = 210, y = 90)
    ttk.Button(window2, text = "CHICKEN RICE", style = "TButton", command = chickricebtn).place(x = 390, y = 90)
    ttk.Button(window2, text = "KOREAN FOOD", style = "TButton", command = koreanbtn).place(x = 30, y = 150)
    ttk.Button(window2, text = "JAPANESE FOOD", style = "TButton", command = japbtn).place(x = 210, y = 150)
    ttk.Button(window2, text = "NOODLES", style = "TButton", command = noodlesbtn).place(x = 390, y = 150)

def caipngbtn():
    store = "Cai Png"

    for stall, hours in menuDB.storeOpen.items():
        if stall == store:
            opentime = menuDB.storeOpen[stall][1][0]
            closetime = menuDB.storeOpen[stall][1][1]

    caipngpop = tk.Tk()
    caipngpop.minsize(200, 100)
    caipngpop.title("Operating Hours")
    label = Label(caipngpop, text = ( str(opentime) + " to " + str(closetime)), font = h3)
    label.pack(side = "top", fill = "x", pady = 10)
    okbtn = Button(caipngpop, text = "Okay", command = caipngpop.destroy)
    okbtn.pack()

def tzecharbtn():
    store = "Tze Char"

    for stall, hours in menuDB.storeOpen.items():
        if stall == store:
            opentime = menuDB.storeOpen[stall][1][0]
            closetime = menuDB.storeOpen[stall][1][1]

    tzecharpop = tk.Tk()
    tzecharpop.minsize(200, 100)
    tzecharpop.title("Operating Hours")
    label = Label(tzecharpop, text = (str(opentime) + " to " + str(closetime)), font = h3)
    label.pack(side = "top", fill = "x", pady = 10)
    okbtn = Button(tzecharpop, text = "Okay", command = tzecharpop.destroy)
    okbtn.pack()

def chickricebtn():
    store = "Chicken Rice"

    for stall, hours in menuDB.storeOpen.items():
        if stall == store:
            opentime = menuDB.storeOpen[stall][1][0]
            closetime = menuDB.storeOpen[stall][1][1]

    chickricepop = tk.Tk()
    chickricepop.minsize(200, 100)
    chickricepop.title("Operating Hours")
    label = Label(chickricepop, text = (str(opentime) + " to " + str(closetime)), font = h3)
    label.pack(side = "top", fill = "x", pady = 10)
    okbtn = Button(chickricepop, text = "Okay", command = chickricepop.destroy)
    okbtn.pack()

def koreanbtn():
    store = "Korean"

    for stall, hours in menuDB.storeOpen.items():
        if stall == store:
            opentime = menuDB.storeOpen[stall][1][0]
            closetime = menuDB.storeOpen[stall][1][1]

    koreanpop = tk.Tk()
    koreanpop.minsize(200, 100)
    koreanpop.title("Operating Hours")
    label = Label(koreanpop, text = (str(opentime) + " to " + str(closetime)), font = h3)
    label.pack(side = "top", fill = "x", pady = 10)
    okbtn = Button(koreanpop, text = "Okay", command = koreanpop.destroy)
    okbtn.pack()

def japbtn():
    store = "Cai Png"

    for stall, hours in menuDB.storeOpen.items():
        if stall == store:
            opentime = menuDB.storeOpen[stall][1][0]
            closetime = menuDB.storeOpen[stall][1][1]

    jappop = tk.Tk()
    jappop.minsize(200, 100)
    jappop.title("Operating Hours")
    label = Label(jappop, text = (str(opentime) + " to " + str(closetime)), font = h3)
    label.pack(side = "top", fill = "x", pady = 10)
    okbtn = Button(jappop, text = "Okay", command = jappop.destroy)
    okbtn.pack()

def noodlesbtn():
    store = "Cai Png"

    for stall, hours in menuDB.storeOpen.items():
        if stall == store:
            opentime = menuDB.storeOpen[stall][1][0]
            closetime = menuDB.storeOpen[stall][1][1]

    noodlespop = tk.Tk()
    noodlespop.minsize(200, 100)
    noodlespop.title("Operating Hours")
    label = Label(noodlespop, text = (str(opentime) + " to " + str(closetime)), font = h3)
    label.pack(side = "top", fill = "x", pady = 10)
    okbtn = Button(noodlespop, text = "Okay", command = noodlespop.destroy)
    okbtn.pack()

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

todaybtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn 1.png")
Button(image = todaybtn, bg = "white", relief = FLAT, command = todaystores).place(x = 300, y = 120)
#todaybtn.grid(row = 0, column = 0 )
allbtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn2.png")
Button(image = allbtn, bg = "white", relief = FLAT, command = allstores).place(x = 450, y = 120)
#allbtn.pack(side = LEFT)
exitbtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn3.png")
Button(image = exitbtn, bg = "white", relief = FLAT, command = root.destroy).place(x = 600, y = 120)

# About Canteen Master
Label(text = "ABOUT  US", font = h2, bg = "white").place(x = 430, y = 200)
abtusbtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn 4.png")
Button(image = abtusbtn, bg = "white", relief = FLAT).place(x = 280, y = 230)

tick()
root.mainloop() #display window until user closes it