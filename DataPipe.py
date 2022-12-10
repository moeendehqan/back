import pandas as pd
import pymongo
import requests
import General
import datetime
import time
import winreg as reg
Client = pymongo.MongoClient("mongodb://localhost:27017/")


RoundDB = Client["Round"]
TseCL = RoundDB['tse']
TseLive = RoundDB['Live']

def addToReg():
    key = reg.OpenKey(reg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" ,0 , reg.KEY_ALL_ACCESS) # Open The Key
    reg.SetValueEx(key ,"any_name" , 0 , reg.REG_SZ , __file__)
    reg.CloseKey(key)




token = '6e437430f8f55f9ba41f7a2cfea64d90'

def LastUpdateFunc():
    LastUpDate = TseCL.find_one({'$query':{},'$orderby':{'dateInt':-1}})
    if len(LastUpDate)==0: LastUpDate = 0
    else: LastUpDate = LastUpDate['dateInt']
    return LastUpDate

def GetOpeningMarket():
    LastUpDate = LastUpdateFunc()
    url =f'http://sourcearena.ir/api/?token={token}&market=bourse&days=500'
    df = pd.DataFrame(requests.get(url).json())
    df['date'] = [General.DateToStd(x) for x in df['date']]
    df['dateInt'] = [General.DateToInt(x) for x in df['date']]
    df = df[df['dateInt']>LastUpDate]
    df = df.drop_duplicates()
    opening = df[df['state']!='closed']
    closed = df[df['state']=='closed']
    opening = opening['date'].to_list()
    closed = closed['date'].to_list()
    return {'closed':closed, 'opening':opening}

def UpdateTseHistori():
    dateList = GetOpeningMarket()
    if len(dateList['closed'])>0:
        print('Pipe Historcal')
        for date in dateList['closed']:
            url =f'https://sourcearena.ir/api/?token={token}&all&time={date}&type=2'
            df = pd.DataFrame(requests.get(url).json())
            df['date'] = date
            df['dateInt'] = [General.DateToInt(x) for x in df['date']]
            df = df.to_dict(orient='records')
            TseCL.delete_many({'dateInt':date})
            TseCL.insert_many(df)
    if len(dateList['opening'])>0:
        print('Pipe Live')
        date = dateList['opening']
        timestump = datetime.datetime.now()
        url =f'https://sourcearena.ir/api/?token={token}&all&time={date}&type=2'
        df = pd.DataFrame(requests.get(url).json())
        df['date'] = date
        df['timestump'] = timestump.timestamp()
        df['dateInt'] = [General.DateToInt(x) for x in df['date']]
        df = df.to_dict(orient='records')
        TseLive.insert_many(df)
        TseCL.delete_many({'dateInt':date})
        TseCL.insert_many(df)


def LoopUpdateTse():
    while True:
        time.sleep(60)
        now =datetime.datetime.now()
        print(now)
        start = now.replace(hour=8,minute=44)
        end = now.replace(hour=13,minute=0)
        if now>start and now<end:
            UpdateTseHistori()


addToReg()
LoopUpdateTse()