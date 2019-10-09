import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *   
import datetime
from tkinter import messagebox
import menuDB

from tkcalendar import Calendar, DateEntry

#basic layout of page
root = tk.Tk() #initialise window
root.title("Home") #create window
root.config(bg = 'white') #change background color
root.minsize(800, 500) #set size of window 

# Font Styling
h1 = ("Century Gothic", 14, "bold")
h2 =  ("Century Gothic", 12, "bold")
h3Italic = ("Century Gothic", 11, "italic")
h3 =  ("Century Gothic", 11)

#C O N T E N T

#label = tk.Label(root, text = "Welcome to Canteen Waiter!", font = ("Arial ", 16, "bold"), height=3, bg="white")

# Main Frames
left_frame = Frame(root, width = 220, height = 150)
left_frame.grid(row = 0, column = 0, pady = 20, padx = 40)

left_frame2 = Frame(root, width = 220, height = 150)
left_frame2.grid(row = 1, column = 0, pady = 23, padx = 30)
#right_frame = Frame(root, width = 850, height = 600)
#right_frame.grid(row = 0, column = 1, padx = 10, pady = 5)

# Position Axis
w = 300
h = 200
x = 50
y = 100
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

# Frame in Left Frame + Content
#tool_bar = Frame(left_frame, width = 220, height = 150)
#tool_bar.grid(row = 1, column = 0, pady = 1)
Label(left_frame, text = "Hello! Today is...", font = h1).place(x = 35, y = 20)
Label(left_frame2, text = "Customisation", font = h1).place(x = 38, y = 20)


# Left frame content
now = datetime.datetime.now()
currentdate = now.strftime("%d %b %Y")
currentime = now.strftime("%I:%M %p")
Label(left_frame, text = currentdate, font = h3Italic).place(x = 60, y = 70)
Label(left_frame, text = currentime, font = h3Italic).place(x = 68, y = 100)

#calendar
Label(left_frame2, text = 'Choose date', font = ("Century Gothic", 10)).place(x = 10, y = 60)
cal = DateEntry(left_frame2, background='darkblue', foreground='white')
cal.place(x = 110, y = 60)

#time
Label(left_frame2, text = "Choose time", font = ("Century Gothic", 10)).place(x = 10, y = 100)




#def availablestores():
#    storesopen = ['Macdonalds', 'KFC', 'Starbucks', 'Pizza Hut']
#    messagebox.showinfo("Today's Stores", "\n".join(storesopen))

#def allstores():
#    allstores = ['Macdonalds', 'KFC', 'Starbucks', 'Subway', 'Pizza Hut', 'Long John Silver', 'The Sandwich Guys', 'Each a cup', 'Umi Sushi', 'Paik Bibim', 'The Soup Spoon', 'Boost']
#    messagebox.showinfo("Stores Available", "\n".join(allstores))

day = datetime.datetime.today().weekday()
todaysMenu = {}

def userInput():
    global userInputStore
    storename = userInputStore.get()
    print (userInputStore)

def todaystores():
    window = tk.Toplevel(root)
    window.config(bg = "white")
    window.title("Today's Stores")
    window.minsize(600, 500) #set size of window 
    Label(window, text = "The stores opened today are:", font = h1, bg = "white").place(x = 10, y = 70)
    #storesopen = ['Macdonalds', 'KFC', 'Starbucks', 'Pizza Hut']
    #Label(window, text = "\n ".join(storesopen), font = h3, bg = "white").place(x = 50, y = 70)

    for n in menuDB.storeList:
        Label(window, text = n, font = h3, bg = "white").place(x = 50, y = 110)

    Label(window, text = "Please enter the name of the store: ", font = h3, bg = "white").place(x = 10, y = 30)
    #userInputStore = Entry(window).place(x = 280, y = 35)

    #go = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\btn4.png")
    #Button(window, image = go, bg = "white", relief = FLAT, command = userInput).place(x = 400, y = 30)

    
def allstores():
    window2 = tk.Toplevel(root)
    window2.config(bg = "white")
    window2.title("All Stores")
    window2.minsize(600, 500) #set size of window 
    Label(window2, text = "Here is a list of all the available stores in North Spine:", font = h1, bg = "white").place(x = 10, y = 30)
    #allstores = ['Macdonalds', 'KFC', 'Starbucks', 'Subway', 'Pizza Hut', 'Long John Silver', 'The Sandwich Guys', 'Each a cup', 'Umi Sushi', 'Paik Bibim', 'The Soup Spoon', 'Boost']
    #Label(window2, text = "\n".join(allstores), font = h3, bg = "white").place(x = 50, y = 70)
    Label(window2, text = "\n".join(menuDB.storeList), font = h3, bg = "white").place(x = 180, y = 70)

# Right frame content
#logobtn = PhotoImage(file = r"D:\NTU\CZ1003 Intro to Computational Thinking\Proj\logo.PNG")
#Button(image = logobtn, bg = "white", relief = FLAT).place(x = 300 y = 30)
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

root.mainloop() #display window until user closes it