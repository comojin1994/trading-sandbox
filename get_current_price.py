import requests, yaml
import getmac


def get_current_price(excd: str, symb: str):
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "appKey":config['APP_KEY'],
        "appSecret":config['APP_SECRET'],
        "tr_id":"HHDFS00000300",
        "tr_cont": "",
        "custtpye": "P",
        "mac_address": f'{getmac.get_mac_address()}'}
    params = {"AUTH":"",
        "EXCD": excd, 
        "SYMB": symb}

    PATH = "uapi/overseas-price/v1/quotations/price"
    URL = f"{config['URL_BASE']}/{PATH}"

    res = requests.get(URL, headers=headers, params=params)

    return res.json()


if __name__ == '__main__':
    from pprint import pprint
    
    res = get_current_price(excd='NAS', symb='TQQQ')
    
    print(f'RESPONSE      >>> {res["msg1"]}')
    print(f'RESPONSE CODE >>> {res["msg_cd"]}')
    print(f'종목코드      >>> {res["output"]["rsym"]}')
    print(f'현재가        >>> {res["output"]["last"]}')
    print(f'등락율        >>> {res["output"]["rate"]}')
    print(f'대비기호      >>> {res["output"]["sign"]}')
    print(f'대비          >>> {res["output"]["diff"]}')
    print(f'거래량        >>> {res["output"]["tvol"]}')
    print(f'거래대금      >>> {res["output"]["tamt"]}')
    print(f'전일종가      >>> {res["output"]["base"]}')
    print(f'전일거래량    >>> {res["output"]["pvol"]}')
    print(f'성공실패여부  >>> {res["rt_cd"]}')
    
