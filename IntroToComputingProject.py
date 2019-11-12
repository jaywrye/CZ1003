import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *   
import datetime
import time
from tkinter import messagebox
from functions import *
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry

#basic layout of page
root = tk.Tk() 
root.title("Home")
root.config(bg = 'white') 
root.minsize(800, 500) 

#declarations
storemenuDict = {}
storesOpenList = []
opentime = 0
closetime = 0
time1 = ''
menuDict = {}
storeOpen = {}
storeOpenDict = {}
#DayDict = {}
now = datetime.datetime.now()
current = datetime.datetime.now().time()
currentdate = now.strftime("%d %b %Y")
currentime = now.strftime("%I:%M:%S %p")
day = datetime.datetime.today().weekday()
userInputFood = StringVar()
pplwaiting = StringVar()

# Position Axis
w = 300
h = 200
x = 50
y = 100
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

#creates page for user to define their own dates and time
def custom():
    global window2, cal, hourcombo, mincombo
    window2 = tk.Toplevel(root)
    window2.config(bg = "white")
    window2.title("Customisation")
    window2.minsize(600, 500) #set size of window 

    titleLabel = Label(window2, text = "Customisation", font = h1, bg = "white")
    titleLabel.place(x = 10, y = 20)

    #calendar
    calendarLabel = Label(window2, text = 'Choose date', font = h3, bg = "white")
    calendarLabel.place(x = 10, y = 60)
    cal = DateEntry(window2, background='darkblue', foreground='white')
    cal.place(x = 130, y = 65)

    #time
    timelabel = Label(window2, text = "Choose time", font = h3, bg = "white")
    timelabel.place(x = 240, y = 60)

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

#gets user-defined values and display list of stalls open based on that
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

    #pass and convert user-defined time into time format
    usertime = userhour + ":" + usermin
    convertedtime = datetime.datetime.strptime(usertime, "%H:%M")
    convertedtime2 = convertedtime.time()

    #returns list of open stalls based on user defined date and time
    for n in storeOpenDict:
        if day in storeOpenDict[n]:
            try: 
                if(convertedtime2 >= storeOpenDict[n][day][0]) and (convertedtime2 <= storeOpenDict[n][day][1]):
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
        
#based on the stall list provided, it will display the menu for the store that the user chooses
def customshopmenu():
    global fooditems, price
    chosenshop = ddl.get()

    custommenupop = tk.Toplevel(root)
    custommenupop.minsize(450, 500)
    custommenupop.config(bg = "white")
    custommenupop.title("Menu")

    titleLabel = Label(custommenupop, text = chosenshop + "'s Menu", bg = "white", font = h2)
    titleLabel.place(x = 10, y = 10)

    #retrieve menu of the stall based on user inputs
    storemenudicttime = storemenutime(chosenshop, convertedtime2, day, menuDict, storeOpenDict)

    #display retrieved information on window
    allprices = [v for v in storemenudicttime.values()]
    fooditems = Label(custommenupop, text = '\n'.join(storemenudicttime), font = h3, bg = "white", justify = LEFT)
    fooditems.place(x = 10, y = 50)
    price = Label(custommenupop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white")
    price.place(x = 350, y = 50)

#displays the menu based on the store the user selects
def menubtn(ImgLocation, store):
    global storename 
    storename = store

    #gets opening and closing time of the store
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

    #display operational hours
    oplabel = Label(menupop, text = "Operating hours: ", font = h3Bold, bg = "white")
    oplabel.place(x = 10, y = 180)
    ophours = Label(menupop, text = (str(opentime) + " to " + str(closetime)), font = h3, bg = "white")
    ophours.place(x = 150, y = 180)

    #display text entry for user to enter number of people queuing
    pplwaitingLabel = Label(menupop, text = "No. of people: ", font = h3, bg = "white")
    pplwaitingLabel.place(x = 10, y = 215)
    pplwaitingEntry = Entry(menupop, textvariable = pplwaiting)
    pplwaitingEntry.place(x = 130, y = 220)

    #go button
    load = Image.open('images/gobtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(menupop, image = render, relief = FLAT, borderwidth = 0, command = lambda : userWaitingTime(store, pplwaiting, storeInfo))
    img.image = render
    img.place(x = 270, y = 215)

    menulabel = Label(menupop, text = "Menu", font = h2, bg = "white")
    menulabel.place(x = 200, y = 270)

    #gets the menu based on stall selected
    storemenudicttime = storemenutime(store, current, day, menuDict, storeOpenDict)

    #displays information
    allprices = [v for v in storemenudicttime.values()]
    fooditems = Label(menupop, text = '\n'.join(storemenudicttime), font = h3, bg = "white", justify = LEFT)
    fooditems.place(x = 30, y = 290)
    price = Label(menupop, text = '\n'.join(map(str, allprices)), font = h3, bg = "white")
    price.place(x = 350, y = 290)

#displays the button for the user to view the menu
def allstores():
    window = tk.Toplevel(root)
    window.config(bg = "white")
    window.title("All Stores")
    window.minsize(600, 450) #set size of window 

    titlelabel = Label(window, text = "All Stores", font = h1, bg = "white")
    titlelabel.place(x = 255, y = 20)

    #mini wok
    load = Image.open('images/miniwokbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/miniwok.png', 'Mini Wok'))
    img.image = render
    img.place(x = 30, y = 90)

    #yong tau foo
    load = Image.open('images/ytfbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/ytf.png', 'Yong Tau Foo'))
    img.image = render
    img.place(x = 210, y = 90)

    #chicken rice
    load = Image.open('images/chickenricebtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/chickenrice.png', 'Chicken Rice'))
    img.image = render
    img.place(x = 390, y = 90)

    #noodles
    load = Image.open('images/noodlesbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/noodles.png', 'Noodles'))
    img.image = render
    img.place(x = 30, y = 150)

    #mixed rice
    load = Image.open('images/mixedricebtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/mixedrice.png', 'Mixed Rice'))
    img.image = render
    img.place(x = 210, y = 150)

    #western
    load = Image.open('images/westernbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/western.png', 'Western'))
    img.image = render
    img.place(x = 390, y = 150)
    
    #drinks
    load = Image.open('images/drinksbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/drinks.png', 'Drinks'))
    img.image = render
    img.place(x = 30, y = 210)

    #soup delight
    load = Image.open('images/soupbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/soup.png', 'Soup Delight'))
    img.image = render
    img.place(x = 210, y = 210)

    #malay
    load = Image.open('images/malaybtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/malay.png', 'Malay BBQ'))
    img.image = render
    img.place(x = 390, y = 210)

    #vegetarian
    load = Image.open('images/vegetarianbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/vegetarian.png', 'Vegetarian'))
    img.image = render
    img.place(x = 30, y = 270)

    #salad
    load = Image.open('images/saladbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/salad.png', 'Salad'))
    img.image = render
    img.place(x = 210, y = 270)

    #pasta
    load = Image.open('images/pastabtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/pasta.png', 'Pasta'))
    img.image = render
    img.place(x = 390, y = 270)

    #long john silver   
    load = Image.open('images/ljsbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/ljs.png', 'Long John Silver'))
    img.image = render
    img.place(x = 30, y = 330)

    #mac
    load = Image.open('images/macbtn.png')
    render = ImageTk.PhotoImage(load)
    img = Button(window, image = render, borderwidth = 0, relief = FLAT, command = lambda: menubtn('images/mcdonalds.png', 'McDonalds'))
    img.image = render
    img.place(x = 210, y = 330)

#display time
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

menuDict, storeOpenDict = excelConversion("North Spine Canteen Details (New).xlsx")
storeInfo = excelConversionInfo("North Spine Canteen Details (New).xlsx")
# Main Frames
left_frame = Frame(root, width = 220, height = 150)
left_frame.grid(row = 0, column = 0, pady = 190, padx = 40)
left_frame2 = Frame(root, width = 220, height = 150)

#logo
load = Image.open('images/logo.PNG')
render = ImageTk.PhotoImage(load)
img = Label(image = render, relief = FLAT, bg = "white")
img.image = render
img.place(x = 50, y = 50)

# Frame in Left Frame + Content
helloLabel = Label(left_frame, text = "Hello! Today is...", font = h1)
helloLabel.place(x = 35, y = 30)

# Left frame content
dateLabel = Label(left_frame, text = currentdate, font = h3Italic)
dateLabel.place(x = 60, y = 70)
clock = Label(left_frame, font = h3Italic)
clock.place(x = 78, y = 100)

# Right frame content
welcomeLabel = Label(text = "WELCOME TO NTU'S CANTEEN MASTER", font = h2, bg = "white")
welcomeLabel.place(x = 300, y = 30)
welcomeLabel2 = Label(text = "I want to...", font = h3, bg = "white")
welcomeLabel2.place(x = 300, y = 80)

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
