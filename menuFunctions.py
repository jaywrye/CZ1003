import menuDB

def storesopen(dayofweek):                                                     # Function that returns a list of stores open on the chosen day
    storesopenList = []                                                        # dayofweek is an int ranging from 0-6  with 0 being Monday and 6 being Sunday
    for n in menuDB.storeOpen:
        if dayofweek in menuDB.storeOpen[n][0]:
            storesopenList.append(n)
    return storesopenList

def storeopeningtime(storename):                                       # Function that returns opening time and closing time based on storename, returns 0 if no such store found
    opentime = 0
    closetime = 0
    for n in menuDB.storeOpen:
        if storename in menuDB.storeOpen:
            opentime = menuDB.storeOpen[n][1][0]
            closetime = menuDB.storeOpen[n][1][1]
        return opentime, closetime

def storemenu(storename):                                                      # Function that returns dictionary of ALL items on their menu {"Name of food item" : price of food}
    storemenuDict = {}                                                         # storename is a string
    for n in menuDB.menu:
        if storename in n:
            storemenuDict.update({n[2] : menuDB.menu[n]})
    return storemenuDict

def storemenuDay(storename, dayofweek):                                       # Function that returns dictionary of menu items on the chosen day {"Name of food item" : price of food}
    storemenuDict = {}                                                        # storename is a string, dayofweek is an int ranging from 0-7  with 0 being Monday and 6 being Sunday and 7 is everyday
    for n in menuDB.menu:
        if storename in n:
            if dayofweek in n:
                storemenuDict.update({n[2] : menuDB.menu[n]})
            if 7 in n:
                storemenuDict.update({n[2] : menuDB.menu[n]})
    return storemenuDict

def storemenuOnlyDay(storename, dayofweek):                                 # Function that returns dictionary of menu items available only on the chosen day {"Name of food item" : price of food}
    storemenuDict = {}                                                      # storename is a string, dayofweek is an int ranging from 0-6  with 0 being Monday and 6 being Sunday
    for n in menuDB.menu:
        if storename in n:
            if dayofweek in n:
                storemenuDict.update({n[2] : menuDB.menu[n]})
    return storemenuDict

def searchfood(foodname):                                                   # Function that returns price for chosen food, if not found return 0
    for n in menuDB.menu:                                                   # foodname is a string
        if foodname in n:
            return menuDB.menu[n]
        else:
            return 0

def dictSplit(storemenuDict):                                   # Function that splits a dictionary into 2 lists, one that has food name another that has price
    storenameList = []
    storepriceList = []
    for storename in storemenuDict:
        storenameList.append(storename)
        storepriceList.append(storemenuDict[storename])
    return storenameList, storepriceList
