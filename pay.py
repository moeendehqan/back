import requests
import json


token= '2Dgl_X9rJC6vcWPUxkxQj7_rtjz5B904MOJX71Rxdd4'


def CreatePay(phone):
    url = 'https://api.payping.ir/v2/pay'
    headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json'}
    data = {"amount":1000, "payerIdentity":phone, "payerName":"کاربر", "description":"اشتراک یکساله", "returnUrl":"http://localhost:3000/", "clientRefId":"556212"}
    pp = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(pp.json())


CreatePay('09011010958')