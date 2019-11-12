import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *   
import datetime
import time
from tkinter import messagebox
from functions import *

import os
#import openpyxl
#from openpyxl import load_workbook
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry

#basic layout of page
root = tk.Tk() #initialise window
root.title("Home") #create window
root.config(bg = 'white') #change background color
root.minsize(800, 500) #set size of window 


#declarations
day = datetime.datetime.today().weekday()
storemenuDict = {}
storesOpenList = []

#declare variables
opentime = 0
closetime = 0
time1 = ''
userInputFood = StringVar()
pplwaiting = StringVar()
menuDict = {}
storeOpen = {}
storeOpenDict = {}
DayDict = {}
dayofweek = datetime.datetime.today().weekday()
now = datetime.datetime.now()
current = datetime.datetime.now().time()
currentdate = now.strftime("%d %b %Y")
currentime = now.strftime("%I:%M:%S %p")

# Position Axis
w = 300
h = 200
x = 50
y = 100
root.geometry("%dx%d+%d+%d" % (w, h, x, y))


def usercustom():
    storesOpenList = []
    global ddl, convertedtime2

    # get user input date
    userdate = cal.get_date()
    
    # get user input time
    userhour = hourcombo.get()
    if userhour.isdigit():
            userhour = hourcombo.get()
    else:
        messagebox.showinfo("Error", "Please enter numbers only.")

    usermin = mincombo.get()
    if usermin.isdigit():
            usermin = hourcombo.get()
    else:
        messagebox.showinfo("Error", "Please enter numbers only.")

    usertime = userhour + ":" + usermin
    convertedtime = datetime.datetime.strptime(usertime, "%H:%M")
    convertedtime2 = convertedtime.time()

    #returns list of open stalls based on user defined date and time
    for n in storeOpenDict:
        if dayofweek in storeOpenDict[n]:
            try: 
                if(convertedtime2 >= storeOpenDict[n][dayofweek][0]) and (convertedtime2 <= storeOpenDict[n][dayofweek][1]):
                    storesOpenList.append(n)
                    print(storesOpenList)
            except:
                break

    ddl = StringVar(window2)
    try:
        ddl.set(storesOpenList[0]) #set first item as default value
        ddlLabel = Label(window2, text = "Please choose a restaurant: ", font = h3, bg = "white")
        ddlLabel.place(x = 10, y = 110)
        ddlist = OptionMenu(window2, ddl, storesOpenList[0], *storesOpenList)
        ddlist.config(bg = "white", width = 20, relief = FLAT, font = h4)
        ddlist.place(x = 250, y = 110)

        #gobtn
        load = Image.open('images/gobtn.png')
        render = ImageTk.PhotoImage(load)
        img = Button(window2, image = render, relief = FLAT, borderwidth = 0, command = customshopmenu)
        img.image = render
        img.place(x = 450, y = 107) 
    except:
        messagebox.showerror("Error", "Sorry, no stores are available at your chosen time/date.")
        window2.destroy()
        
def customshopmenu():
    global fooditems, price
    chosenshop = ddl.get()
    titleLabel = ""

    titleLabel = Label(window2, text = chosenshop + "'s Menu", bg = "white", font = h2)
    titleLabel.place(x = 10, y = 150)

    storemenudicttime = storemenutime(chosenshop, convertedtime2, day, menuDict, storeOpenDict)

    allprices = [v for v in storemenudicttime.values()]
    fooditems = Label(window2, text = '\n'.join(storemenudicttime), font = h3, bg = "white", justify = LEFT)
    fooditems.place(x = 10, y = 200)
    price = Label(window2, text = '\n'.join(map(str, allprices)), font = h3, bg = "white")
    price.place(x = 350, y = 200)

def menubtn(ImgLocation, store):
    global storename 
    storename = store

    opentime, closetime = storeopeningtime(store, day, storeOpenDict)

    menupop = tk.Toplevel(root)
    menupop.minsize(450, 700)
    menupop.config(bg = "white")
    menupop.title(store)

    #banner image
    load = Image.open(ImgLocation)
    render = ImageTk.PhotoImage(load)
    img = Label(menupop, image = render)
    img.image = render
    img.place(x = 0, y = 1)

    oplabel = Label(menupop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 10, y = 180)
    ophours = Label(menupop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 180)

    Label(menupop, text = "No. of people: ", font = h3, bg = "white").place(x = 10, y = 215)
    Entry(menupop, textvariable = pplwaiting).place(x = 130, y = 220)

    #go button
    load = Image.open('images/gobtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(menupop, image = render, relief = FLAT, borderwidth = 0, command = lambda : userWaitingTime(store, pplwaiting, storeInfo))
    img.image = render
    img.place(x = 270, y = 215)

    menulabel = Label(menupop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 200, y = 270)

    storemenudicttime = storemenutime(store, current, day, menuDict, storeOpenDict)

    allprices = [v for v in storemenudicttime.values()]
    fooditems = Label(menupop, text = '\n'.join(storemenudicttime), font = h3, bg = "white", justify = LEFT)
    fooditems.place(x = 30, y = 290)
    price = Label(menupop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white")
    price.place(x = 350, y = 290)

def allstores():
    window = tk.Toplevel(root)
    window.config(bg = "white")
    window.title("All Stores")
    window.minsize(600, 450) #set size of window 

    titlelabel = Label(window, text = "All Stores", font = h1, bg = "white")
    titlelabel.place(x = 255, y = 20)

    load = Image.open('images/miniwokbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/miniwok.png', 'Mini Wok'))
    img.image = render
    img.place(x = 30, y = 90)

    load = Image.open('images/ytfbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/ytf.png', 'Yong Tau Foo'))
    img.image = render
    img.place(x = 210, y = 90)

    load = Image.open('images/chickenricebtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/chickenrice.png', 'Chicken Rice'))
    img.image = render
    img.place(x = 390, y = 90)

    load = Image.open('images/noodlesbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/noodles.png', 'Noodles'))
    img.image = render
    img.place(x = 30, y = 150)

    load = Image.open('images/mixedricebtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/mixedrice.png', 'Mixed Rice'))
    img.image = render
    img.place(x = 210, y = 150)

    load = Image.open('images/westernbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/western.png', 'Western'))
    img.image = render
    img.place(x = 390, y = 150)

    load = Image.open('images/drinksbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/drinks.png', 'Drinks'))
    img.image = render
    img.place(x = 30, y = 210)

    load = Image.open('images/soupbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/soup.png', 'Soup Delight'))
    img.image = render
    img.place(x = 210, y = 210)

    load = Image.open('images/malaybtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/malay.png', 'Malay BBQ'))
    img.image = render
    img.place(x = 390, y = 210)

    load = Image.open('images/vegetarianbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/vegetarian.png', 'Vegetarian'))
    img.image = render
    img.place(x = 30, y = 270)

    load = Image.open('images/saladbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/salad.png', 'Salad'))
    img.image = render
    img.place(x = 210, y = 270)

    load = Image.open('images/pastabtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/pasta.png', 'Pasta'))
    img.image = render
    img.place(x = 390, y = 270)

    load = Image.open('images/ljsbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/ljs.png', 'Long John Silver'))
    img.image = render
    img.place(x = 30, y = 330)

    load = Image.open('images/macbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/mcdonalds.png', 'McDonalds'))
    img.image = render
    img.place(x = 210, y = 330)

def custom():
    global window2, cal, hourcombo, mincombo
    window2 = tk.Toplevel(root)
    window2.config(bg = "white")
    window2.title("Customisation")
    window2.minsize(600, 500) #set size of window 

    Label(window2, text = "Customisation", font = h1, bg = "white").place(x = 10, y = 20)
    style = ttk.Style()
    style.configure("TButton", font = ("Century Gothic", 12, 'bold'), foreground = "#3366CC", background = 'white', width = "15")
    #calendar
    Label(window2, text = 'Choose date', font = h3, bg = "white").place(x = 10, y = 60)
    cal = DateEntry(window2, background='darkblue', foreground='white')
    cal.place(x = 130, y = 65)

    #time
    Label(window2, text = "Choose time", font = h3, bg = "white").place(x = 240, y = 60)

    hour_list = []
    for hour in range(0, 24):
        if hour < 10:
            hour = '0' + str(hour)
        hour_list.append(str(hour))
    hourcombo = ttk.Combobox(window2, values=hour_list, width=5,)
    hourcombo.set(10)
    hourcombo.place(x = 350, y = 65)

    minute_list = []
    for minute in range(0,60):
        if minute < 10:
            minute = '0' + str(minute)
        minute_list.append(str(minute))
    mincombo = ttk.Combobox(window2, text = "00", values=minute_list, width=5)
    mincombo.set(00)
    mincombo.place(x = 420, y = 65)

    load = Image.open('images/gobtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window2, image = render, relief = FLAT, borderwidth = 0, command = usercustom)
    img.image = render
    img.place(x = 480, y = 58)

def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')

    if time2 != time1:
        time1 = time2
        clock.config(text = time2)

    clock.after(10, tick)

# Font Styling
h1 = ("Century Gothic", 14, "bold")
h2 =  ("Century Gothic", 12, "bold")
h3Italic = ("Century Gothic", 11, "italic")
h3 =  ("Century Gothic", 11)
h3Bold = ("Century Gothic", 11, "bold")
h4 = ("Century Gothic", 9)

menuDict, storeOpenDict = excelConversion("North Spine Canteen Details.xlsx")
storeInfo = excelConversionInfo("North Spine Canteen Details.xlsx")
# Main Frames
left_frame = Frame(root, width = 220, height = 150)
left_frame.grid(row = 0, column = 0, pady = 20, padx = 40)

left_frame2 = Frame(root, width = 220, height = 150)


# Frame in Left Frame + Content
Label(left_frame, text = "Hello! Today is...", font = h1).place(x = 35, y = 20)

# Left frame content
Label(left_frame, text = currentdate, font = h3Italic).place(x = 60, y = 70)
clock = Label(left_frame, font = h3Italic)
clock.place(x = 68, y = 100)

# Right frame content
Label(text = "WELCOME TO NTU'S CANTEEN MASTER", font = h2, bg = "white").place(x = 300, y = 30)
Label(text = "I want to...", font = h3, bg = "white").place(x = 300, y = 80)

#today's stores button
load = Image.open('images/btn2.png')
render = ImageTk.PhotoImage(load)
img = Button(image = render, relief = FLAT, command = allstores, borderwidth = 0)
img.image = render
img.place(x = 300, y = 120)

#customise button
load = Image.open('images/btn12.png')
render = ImageTk.PhotoImage(load)
img = Button(image = render, relief = FLAT, command = custom, borderwidth = 0)
img.image = render
img.place(x = 450, y = 120)

#exit button
load = Image.open('images/exitbtn.png')
render = ImageTk.PhotoImage(load)
img = Button(image = render, relief = FLAT, command = root.destroy, borderwidth = 0)
img.image = render
img.place(x = 600, y = 120)

# About Canteen Master
Label(text = "ABOUT  US", font = h2, bg = "white").place(x = 430, y = 200)
load = Image.open('images/btn 4.png')
render = ImageTk.PhotoImage(load)
img = Label(image = render, relief = FLAT, bg = "white")
img.image = render
img.place(x = 280, y = 230)

tick()
root.mainloop() #display window until user closes it
