import requests, yaml
import getmac


def get_daily_price(excd: str,
                    symb: str,
                    gubn: str,
                    bymd: str,
                    modp: str,
                    keyb: str=''):
    
    '''
    입력된 날짜(BYMD) 기준 100개의 데이터 반환
    '''
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "appKey":config['APP_KEY'],
        "appSecret":config['APP_SECRET'],
        "tr_id":"HHDFS76240000 ",
        "tr_cont": "",
        "custtpye": "P",
        "mac_address": f'{getmac.get_mac_address()}'}
    params = {"AUTH":"",
        "EXCD": excd, 
        "SYMB": symb,
        'GUBN': gubn,
        'BYMD': bymd,
        'MODP': modp,
        'KEYB': keyb}

    PATH = "uapi/overseas-price/v1/quotations/dailyprice"
    URL = f"{config['URL_BASE']}/{PATH}"

    res = requests.get(URL, headers=headers, params=params)

    return res.json()


if __name__ == '__main__':
    from pprint import pprint
    
    res = get_daily_price(excd='NAS',
                        symb='TQQQ',
                        gubn='0',
                        bymd='20220511',
                        modp='0')
    
    print(f'RESPONSE      >>> {res["msg1"]}')
    print(f'RESPONSE CODE >>> {res["msg_cd"]}')
    print(f'종목코드      >>> {res["output1"]["rsym"]}')
    for i in range(5):
        # 가장 최근의 5개 기록만 출력
        print()
        print(f'날짜          >>> {res["output2"][i]["xymd"]}')
        print(f'종가          >>> {res["output2"][i]["clos"]}')
        print(f'대비기호      >>> {res["output2"][i]["sign"]}')
        print(f'대비          >>> {res["output2"][i]["diff"]}')
        print(f'등락율        >>> {res["output2"][i]["rate"]}')
        print(f'시가          >>> {res["output2"][i]["open"]}')
        print(f'고가          >>> {res["output2"][i]["high"]}')
        print(f'저가          >>> {res["output2"][i]["low"]}')
        print(f'거래량        >>> {res["output2"][i]["tvol"]}')
        print(f'거래대금      >>> {res["output2"][i]["tamt"]}')
        print(f'매수호가      >>> {res["output2"][i]["pbid"]}')
        print(f'매수호가잔량  >>> {res["output2"][i]["vbid"]}')
        print(f'매도호가      >>> {res["output2"][i]["pask"]}')
        print(f'매도호가잔량  >>> {res["output2"][i]["vask"]}')
        print()
    print(f'성공실패여부  >>> {res["rt_cd"]}')
    
