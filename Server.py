from flask import Flask ,request
from flask_cors import CORS
import pymongo
import warnings
import public
import sms
import Login
import Filter
warnings.filterwarnings("ignore")

client = pymongo.MongoClient()
farasahmDb = client['farasahm']
userCl = farasahmDb['user']

app = Flask(__name__)
CORS(app)

@app.route('/public/randomtse',methods = ['POST', 'GET'])
def stocks_sediment():
    return public.RandomTse()

@app.route('/sms/otpsend',methods = ['POST', 'GET'])
def sms_otpsend():
    data = request.get_json()
    return sms.otpsend(data)

@app.route('/Login/verification',methods = ['POST', 'GET'])
def Login_verification():
    data = request.get_json()
    return Login.verification(data)

@app.route('/login/authentication',methods = ['POST', 'GET'])
def Login_authentication():
    data = request.get_json()
    return Login.authentication(data)

@app.route('/filter/get',methods = ['POST', 'GET'])
def filter_get():
    data = request.get_json()
    return Filter.get(data)

if __name__ == '__main__':
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
    app.run(host='0.0.0.0', debug=True)