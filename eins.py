import urllib.request
import json
import sqlite3
import argparse
from datetime import datetime, timedelta
import logging
from ics import Calendar, Event

muellsorten = {
    "gelber": "Gelber Sack",
    "rest": "Restmüll",
    "bio": "Biomüll",
    "papier": "Papier",
    "christ": "Christbaum",
}

def main(offset=None, duration=None):
    (date, hasChanged) = isModified()
    if (hasChanged):
        print("Es gibt Neuigkeiten")
        updateCalendar(offset, duration)
        updateModifcationDate(date)

def updateCalendar(offset=None, duration=None):
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
                        e.begin =  calcDateTimeBegin(pickup) if (offset==None) else calcDateTimeBegin(pickup, offset) 
                        if(duration == None): 
                            e.make_all_day() 
                        else: 
                            e.duration = timedelta(hours=duration) 
                        c.events.add(e)

        calfile = open("pickups" + location['shorthand'] + ".ics", 'w')
        calfile.writelines(c.serialize_iter())
        calfile.close()

def calcDateTimeBegin(pickup, offset=0):
    print(offset)
    return  datetime(int(pickup['year']),  int(pickup['month']),  int(pickup['day']))+timedelta(hours=offset)

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

def parseUserArguments():
    parser = argparse.ArgumentParser(description="Create garbage collection plan ;-)")

    parser.add_argument('--offset', type=int, default=None, help='The offset for the event beginning based on 00:00 a.m. local time')
    parser.add_argument('--duration', type=int, default=None, help='The event duration')

    return parser.parse_args()

def checkDurationValidValue(duration):
    if (duration is not None):
        if(duration <= 0):
            print("Event duration must not be less or equal to 0, ... exit")
            exit(1)

def noArugmentIsGivenByUser(args):
    return (args.offset is None) and (args.duration is None)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    args = parseUserArguments()

    if noArugmentIsGivenByUser(args):
        main()
    else:
        checkDurationValidValue(args.duration)
        main(args.offset, args.duration)

        

