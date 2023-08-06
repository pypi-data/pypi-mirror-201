from datetime import datetime

def getDateString():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def printLog(msg):
    print(f'[{getDateString()}] {msg}')