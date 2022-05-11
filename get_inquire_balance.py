import requests, yaml
import getmac


def get_inquire_balance(cano: str,
                        acnt_prdt_cd: str,
                        ovrs_excg_cd: str,
                        tr_crcy_cd: str,
                        ctx_area_fk200: str="",
                        ctx_area_nk200: str=""):
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "appKey":config['APP_KEY'],
        "appSecret":config['APP_SECRET'],
        "tr_id":"JTTT3012R",
        "tr_cont": "",
        "custtpye": "P",
        "mac_address": f'{getmac.get_mac_address()}'}
    params = {"CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "OVRS_EXCG_CD": ovrs_excg_cd,
            "TR_CRCY_CD": tr_crcy_cd,
            "CTX_AREA_FK200": ctx_area_fk200,
            "CTX_AREA_NK200": ctx_area_nk200}

    PATH = "uapi/overseas-stock/v1/trading/inquire-balance"
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
            'tr_crcy_cd': 'USD'}
    
    while True:
        res = get_inquire_balance(**data)
        
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
    
    print() # 해당 종목
    print(f'계좌번호      >>> {res["output1"][0]["cano"]}')
    print(f'계좌상품코드  >>> {res["output1"][0]["acnt_prdt_cd"]}')
    print(f'상품유형코드  >>> {res["output1"][0]["prdt_type_cd"]}')
    print(f'해외상품번호  >>> {res["output1"][0]["ovrs_pdno"]}')
    print(f'해외종목명    >>> {res["output1"][0]["ovrs_item_name"]}')
    print(f'평가손익금액  >>> $ {res["output1"][0]["frcr_evlu_pfls_amt"]}') # 손익 금액
    print(f'평가손익율    >>> {res["output1"][0]["evlu_pfls_rt"]} %') # 손익율
    print(f'매입평균가격  >>> $ {res["output1"][0]["pchs_avg_pric"]}') # 평단가
    print(f'매입금액      >>> $ {res["output1"][0]["frcr_pchs_amt1"]}') # 얼마에 샀는지
    print(f'평가금액      >>> $ {res["output1"][0]["ovrs_stck_evlu_amt"]}') # 총 얼마인지
    print(f'잔고수량      >>> {res["output1"][0]["ovrs_cblc_qty"]}')
    print(f'주문가능수량  >>> {res["output1"][0]["ord_psbl_qty"]}') # 매도 가능한 주문 수량
    print(f'현재가        >>> $ {res["output1"][0]["now_pric2"]}')
    print(f'거래통화코드  >>> {res["output1"][0]["tr_crcy_cd"]}')
    print(f'거래소코드    >>> {res["output1"][0]["ovrs_excg_cd"]}')
    print(f'대출유형코드  >>> {res["output1"][0]["loan_type_cd"]}')
    print(f'대출일자      >>> {res["output1"][0]["loan_dt"]}')
    print(f'만기일자      >>> {res["output1"][0]["expd_dt"]}')
    
    print() # 전체 종목
    print(f'매입금액      >>> $ {res["output2"]["frcr_pchs_amt1"]}') # 얼마에 샀는지
    print(f'실현손익      >>> {res["output2"]["ovrs_rlzt_pfls_amt"]}')
    print(f'실현수익률    >>> {res["output2"]["rlzt_erng_rt"]} %')
    print(f'총손익        >>> $ {res["output2"]["ovrs_tot_pfls"]}')
    print(f'총평가손익    >>> $ {res["output2"]["tot_evlu_pfls_amt"]}')
    print(f'총수익률      >>> {res["output2"]["tot_pftrt"]} %')
    print(f'매수금액합계1 >>> $ {res["output2"]["frcr_buy_amt_smtl1"]}')
    print(f'실현손익금액  >>> $ {res["output2"]["ovrs_rlzt_pfls_amt2"]}')
    print(f'매수금액합계2 >>> $ {res["output2"]["frcr_buy_amt_smtl2"]}')
    
    print(f'성공실패여부  >>> {res["rt_cd"]}')    
    
