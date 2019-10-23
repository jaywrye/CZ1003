import menuDB


def storeAvgWaitTime(storename):                                #Function that returns the average wait time per person for that store
    storetype = ""
    avgwaittime = 0
    for n in menuDB.storeType:
        if storename in menuDB.storeType:
            storetype = menuDB.storeType[storename]
            for m in menuDB.storeTypeSpeeds:
                avgwaittime = menuDB.storeTypeSpeeds[storetype]
        return avgwaittime

while True:
    userInputQueue = input("Enter number of people in queue: ")
    userInputStore = input("Enter the store name: ")
    if userInputStore in menuDB.storeType:
        avgwaittime = storeAvgWaitTime(userInputStore)
        totalWaitTime = int(avgwaittime*int(userInputQueue))
        print("Waiting time is:", avgwaittime, "*", userInputQueue, "=", (totalWaitTime), "minutes")
        if totalWaitTime > 60:
            print("Queue is very long, consider going to a different store.")
        break
    else:
        print("Invalid number or store")
        continue