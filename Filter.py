import pandas as pd
import pymongo

import Login
Client = pymongo.MongoClient("mongodb://localhost:27017/")


RoundDB = Client["Round"]
TseCL = RoundDB['tse']
TseLive = RoundDB['tse']

def get(data):
    user = Login.authentication(data)
    if user['credit']>0:
        LastUpDate = TseCL.find_one({'$query':{},'$orderby':{'dateInt':-1}})['date']
        df = pd.DataFrame(TseCL.find({'date':LastUpDate}))
        df = df.drop_duplicates()
        print(df)
        return {'replay':True}
    else:
        return Login.ErrorUser()