import sms
import datetime
import pymongo
import Cryption
import ast


Client = pymongo.MongoClient("mongodb://localhost:27017/")
RoundDB = Client["Round"]
UserDb = RoundDB['user']

def verification(data):
    if sms.OtpVerification(data)['replay']:
        UserDict = UserDb.find_one({'phone':data['Phone']},{'_id':0})
        now = datetime.datetime.now()
        if UserDict == None:
            next_month = now + datetime.timedelta(days=30)
            UserDict = {'phone':data['Phone'],'startDate':now.timestamp(),'endDate':next_month.timestamp()}
            EncryptUser = (Cryption.encrypt(str(UserDict))).decode()
            UserDb.insert_one(UserDict)
            return {'replay':True,'Cookie':EncryptUser}
        else:
            EncryptUser = (Cryption.encrypt(str(UserDict))).decode()
            print(EncryptUser)
            return {'replay':True,'Cookie':EncryptUser}
    else:
        return {'replay':False,'msg':'کد صحیح نیست'}

def authentication(data):
    Signature = str.encode(data['cookie'])
    Signature = ast.literal_eval(Cryption.decrypt(Signature))['phone']
    UserDict = UserDb.find_one({'phone':Signature},{'_id':0})
    if UserDict == None:
        return {'replay':False}
    now = datetime.datetime.now()
    endDate = datetime.datetime.fromtimestamp(UserDict['endDate'])
    credit = (endDate - now).days
    if credit<0:credit=0
    return {'replay':True,'credit':credit,'phone':Signature}

def ErrorUser():
    return {'replay':False,'msg':'خطا، کاربر فاقد اعتبار است'}