
import random
import datetime
import pymongo

Client = pymongo.MongoClient("mongodb://localhost:27017/")
RoundDB = Client["Round"]
LogOTP = RoundDB['LogOTP']


def otpsend(data):
    dic = {'code':random.randint(10000,99999),'timestamp':datetime.datetime.now().timestamp(),'date':datetime.datetime.now(),'phone':data['phone']}
    print(dic)
    LogOTP.insert_one(dic)
    return {'replay':True}


def OtpVerification(data):
    LastOtp = LogOTP.find_one({'$query':{'phone':data['Phone']},'$orderby':{'timestamp':-1}} )
    if LastOtp == None:
        return {'replay':False}
    elif  str(LastOtp['code']) != str(data['Code']):
        return {'replay':False}
    else:
        if str(data['Code']) == str(LastOtp['code']):
            return {'replay':True}
        else:
            return {'replay':False}