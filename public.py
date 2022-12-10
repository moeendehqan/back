import pymongo
import pandas as pd

import General
import random
Client = pymongo.MongoClient("mongodb://localhost:27017/")
RoundDB = Client["Round"]
TseCL = RoundDB['tse']

def LastUpdateFunc():
    LastUpDate = TseCL.find_one({'$query':{},'$orderby':{'dateInt':-1}})
    if len(LastUpDate)==0: LastUpDate = 0
    else: LastUpDate = LastUpDate['dateInt']
    return LastUpDate

def RandomTse():
    LastUpDate = General.IntToDate(LastUpdateFunc())
    df = pd.DataFrame(TseCL.find({'date':LastUpDate}))
    df = df[df['state']=='مجاز']
    marketList =['بازار اول فرابورس','بازار اول (تابلوی اصلی) بورس','بازار اول فرابورس','بازار اول (تابلوی فرعی) بورس','بازار دوم بورس','شرکتهای کوچک و متوسط فرابورس','بازار دوم فرابورس','بازار پایه زرد فرابورس']
    df['InListMarket'] = [x in marketList for x in df['market']]
    df = df[df['InListMarket'] == True]
    df['trade_value'] = [int(x) for x in df['trade_value'].fillna(0)]
    df = df[df['trade_value']>=df['trade_value'].mean()]
    df = df.reset_index()
    df = df[['name','final_price','final_price_change_percent']].to_dict(orient='records')
    ListTse = []
    while len(ListTse)<3:
        randomTseOne = df[random.randint(0,len(df))]
        randomTseOne['final_price_change_percent'] = randomTseOne['final_price_change_percent'].replace('%','')
        if randomTseOne not in ListTse:
            ListTse.append(randomTseOne)
    return {'repaly':True,'df':ListTse}
