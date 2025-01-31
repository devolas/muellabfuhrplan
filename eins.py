import urllib.request
import json
import sqlite3
from datetime import datetime,date
import logging
from ics import Calendar, Event

muellsorten = {
    "gelber": "Gelber Sack",
    "rest": "Restmüll",
    "bio": "Biomüll",
    "papier": "Papier",
    "christ": "Christbaum",
}

def main():
    (date, hasChanged) = isModified()
    if (hasChanged):
        print("Es gibt Neuigkeiten")
        updateCalendar()
        updateModifcationDate(date)

def updateCalendar():
    calendarfile = "pickups.ics"

    pickups = getPickups()

    for location in getPickupLocations():
        c = Calendar()

        for pickup in pickups:
            for muellkurz, muelllang in muellsorten.items():
                print(pickup['year'] + ' ' + pickup['month'] + ' ' + pickup['day'] + " in " + location['shorthand'])
                if muellkurz in pickup.keys():
                    print(pickup[muellkurz].split(', '))
                    if location['shorthand'] in pickup[muellkurz].split(', '):
                        print("habe " + muellkurz + "gefunden")
                        e = Event()
                        e.name = muelllang + " in " + location['name']
                        print(type(e))
                        e.begin = pickup['year'] + '-' + pickup['month'] + '-' + pickup['day'] # + "00:00:00") 
                        e.make_all_day()
                        c.events.add(e)

        calfile = open("pickups" + location['shorthand'] + ".ics", 'w')
        calfile.writelines(c.serialize_iter())
        calfile.close()        

def isModified():
    lastOnlineDate = getLastModified()
    if (lastOnlineDate > getLocalModificationDate()):
        return (lastOnlineDate, True)
    else:
        return (lastOnlineDate, False)

def updateModifcationDate(date):
    filename = "lastmodified.txt"
    import os
    f = open(filename, mode='w')
    f.write(str(date))
    f.close()

def getLocalModificationDate():
    try:
        return datetime.fromisoformat((open("lastmodified.txt")).read())
    except:
        return datetime(1970,1,1)

def getLastModified():
    url = "https://www.mzvhegau.de/wp-json/flexia/v1/pickups/modified"
    rawdate = getFreshData(url)['last_modified']
    date = datetime.fromisoformat(rawdate)
    return date

def getPickupLocations():
    url = "https://www.mzvhegau.de/wp-json/flexia/v2/pickups"
    return getFreshData(url)

def getPickups():
    url = "https://www.mzvhegau.de/wp-json/flexia/v1/pickups"
    return getFreshData(url)

def getFreshData(url):
    urlfile = urllib.request.urlopen(
        urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }))
    jsondata = json.loads(urlfile.read())
    return jsondata

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
