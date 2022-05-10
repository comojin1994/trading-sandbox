import requests, json, yaml
    
    
def hashkey(datas):
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    PATH = "uapi/hashkey"
    URL = f"{config['URL_BASE']}/{PATH}"
    headers = {
        'content-Type' : 'application/json',
        'appKey' : config['APP_KEY'],
        'appSecret' : config['APP_SECRET'],
        }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]

    return hashkey


if __name__ == '__main__':
    
    datas = {
        "CANO": '46491254',
        "ACNT_PRDT_CD": "01",
        "OVRS_EXCG_CD": "SHAA",
        "PDNO": "00001",
        "ORD_QTY": "500",
        "OVRS_ORD_UNPR": "52.65",
        "ORD_SVR_DVSN_CD": "0"
    }
    
    
    print('Hashkey: \n')
    print(hashkey(datas))
    
    