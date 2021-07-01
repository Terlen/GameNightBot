from json import dump, load
import datetime

fileName = 'nextChoice'

def nextGameNight(gameDay=3):
    today = datetime.date.today()
    daysAhead = gameDay - today.weekday()
    if daysAhead <= 0:
        daysAhead += 7
    return (today + datetime.timedelta(daysAhead)).strftime("%m/%d/%Y")

def saveNextChoice(User, Date=nextGameNight()):
    with open(fileName, 'w') as file:
        nextChoice = [User, Date]
        dump(nextChoice, file)

def loadNextChoice():
    with open(fileName) as file:
        return load(file)

