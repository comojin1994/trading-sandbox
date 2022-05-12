import requests, yaml, json
import getmac
from get_hashkey import hashkey


def post_order(order: str, datas):
    '''
    str order: buy, sell
    '''
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "appKey":config['APP_KEY'],
        "appSecret":config['APP_SECRET'],
        "tr_id":"JTTT1002U" if order == 'buy' else "JTTT1006U",
        "tr_cont": "",
        "custtpye": "P",
        "mac_address": f'{getmac.get_mac_address()}',
        "hashkey": hashkey(datas)}

    PATH = "uapi/overseas-stock/v1/trading/order"
    URL = f"{config['URL_BASE']}/{PATH}"

    res = requests.post(URL, headers=headers, data=json.dumps(datas))

    return res.json()


if __name__ == '__main__':
    from pprint import pprint
    import time
    from get_access_token import get_access_token
    
    order = 'buy' # 사자: 'buy', 팔자: 'sell'
    datas = {'CANO': '46491254', 
            'ACNT_PRDT_CD': '01',
            'OVRS_EXCG_CD': 'NASD', # 거래소코드
            'PDNO': 'TQQQ', # 상품번호
            'ORD_QTY': '1', # 주문수량
            'OVRS_ORD_UNPR': '1.00', # 해외주문단가
            'CTAC_TLNO': '01064792776',
            'MGCO_APTM_ODNO': '',
            'SLL_TYPE': '00',
            'ORD_SVR_DVSN_CD': '0',
            'ORD_DVSN': '00'}
    
    
    while True:
        res = post_order(order, datas)
        
        print()
        print(f'RESPONSE      >>> {res["msg1"]}')
        print(f'RESPONSE CODE >>> {res["msg_cd"]}')
        print(f'성공실패여부  >>> {res["rt_cd"]}')
        print()
        
        if res['rt_cd'] != '0':
            
            if res['msg_cd'] == 'EGW00123':
                # TOKEN 만료
                print('Access token: \n')
                print(get_access_token())
            
            elif res['msg_cd'] == 'EGW00201':
                # 초당 거래건수 초과
                time.sleep(1)
                
            elif res['msg_cd'] == 'APBK0952':
                # 주문 가능금액 초과
                break
            
        else:
            print(f'주문시각        >>> {res["output"]["ORD_TMD"]}')
            print(f'주문번호        >>> {res["output"]["ODNO"]}')
            print(f'영업점코드      >>> {res["output"]["KRX_FWDG_ORD_ORGNO"]}')
            print()  
            
            break
