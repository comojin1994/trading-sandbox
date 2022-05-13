import requests, yaml
import getmac


def get_inquire_nccs(cano: str,
                    acnt_prdt_cd: str,
                    ovrs_excg_cd: str,
                    sort_sqn: str,
                    ctx_area_fk200: str="",
                    ctx_area_nk200: str=""):
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "appKey":config['APP_KEY'],
        "appSecret":config['APP_SECRET'],
        "tr_id":"JTTT3018R",
        "tr_cont": "",
        "custtpye": "P",
        "mac_address": f'{getmac.get_mac_address()}'}
    params = {"CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "SORT_SQN": sort_sqn,
            "CTX_AREA_NK200": ctx_area_nk200,
            "CTX_AREA_FK200": ctx_area_fk200}

    PATH = "uapi/overseas-stock/v1/trading/inquire-nccs"
    URL = f"{config['URL_BASE']}/{PATH}"

    res = requests.get(URL, headers=headers, params=params)

    return res.json()


if __name__ == '__main__':
    from pprint import pprint
    import time
    from get_access_token import get_access_token
    
    data = {'cano': '46491254',
            'acnt_prdt_cd': '01',
            'ovrs_excg_cd': 'NASD',
            'sort_sqn': 'DS'}
    
    while True:
        res = get_inquire_nccs(**data)
        
        if res['rt_cd'] != '0':
            print()
            print(f'RESPONSE      >>> {res["msg1"]}')
            print(f'RESPONSE CODE >>> {res["msg_cd"]}')
            print(f'성공실패여부  >>> {res["rt_cd"]}')
            print()
            
            if res['msg_cd'] == 'EGW00123':
                # TOKEN 만료
                print('Access token: \n')
                print(get_access_token())
            
            elif res['msg_cd'] == 'EGW00201':
                # 초당 거래건수 초과
                time.sleep(1)
            
        else: break

    
    print(f'RESPONSE      >>> {res["msg1"]}')
    print(f'RESPONSE CODE >>> {res["msg_cd"]}')
    
    print()
    for i in range(len(res['output'])):
        print(f'주문일자        >>> {res["output"][i]["ord_dt"]}')
        print(f'주문시각        >>> {res["output"][i]["ord_tmd"]}')
        print(f'거래시장        >>> {res["output"][i]["tr_mket_name"]}')
        print(f'거래동화코드    >>> {res["output"][i]["tr_crcy_cd"]}')
        print(f'국가코드        >>> {res["output"][i]["natn_cd"]}')
        print(f'국가명          >>> {res["output"][i]["natn_kor_name"]}')
        print(f'지점번호        >>> {res["output"][i]["ord_gno_brno"]}')
        print(f'주문번호        >>> {res["output"][i]["odno"]}') # 접수한 주문의 일련번호
        print(f'원주문번호      >>> {res["output"][i]["orgn_odno"]}') # 정정 또는 취소 대상 주문의 일련번호
        print(f'상품번호        >>> {res["output"][i]["pdno"]}')
        print(f'상품명          >>> {res["output"][i]["prdt_name"]}')
        print(f'매수매도코드    >>> {res["output"][i]["sll_buy_dvsn_cd"]}')
        print(f'매수매도명      >>> {res["output"][i]["sll_buy_dvsn_cd_name"]}')
        print(f'정정취소구분    >>> {res["output"][i]["rvse_cncl_dvsn"]}')
        print(f'정정취소구분명  >>> {res["output"][i]["rvse_cncl_dvsn_name"]}')
        print(f'거부사유        >>> {res["output"][i]["rjct_rson"]}')
        print(f'거부사유명      >>> {res["output"][i]["rjct_rson_name"]}')
        
        print()
        print(f'주문수량        >>> {res["output"][i]["ft_ord_qty"]}')
        print(f'주문단가        >>> $ {res["output"][i]["ft_ord_unpr3"]}')
        print(f'체결수량        >>> {res["output"][i]["ft_ccld_qty"]}')
        print(f'체결단가        >>> $ {res["output"][i]["ft_ccld_unpr3"]}')
        print(f'체결금액        >>> $ {res["output"][i]["ft_ccld_amt3"]}')
        print(f'미체결수량      >>> {res["output"][i]["nccs_qty"]}')
        
        print()
        print(f'거래소코드      >>> {res["output"][i]["ovrs_excg_cd"]}')
        print(f'처리상태        >>> {res["output"][i]["prcs_stat_name"]}')
        
        print()
        print(f'대출유형코드    >>> {res["output"][i]["loan_type_cd"]}')
        print(f'대출일자        >>> {res["output"][i]["loan_dt"]}')
        print()

    
    print(f'성공실패여부  >>> {res["rt_cd"]}')    
    
