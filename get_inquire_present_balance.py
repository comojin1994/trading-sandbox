import requests, yaml
import getmac


def get_inquire_present_balance(cano: str,
                                acnt_prdt_cd: str,
                                wcrc_frcr_dvsn_cd: str,
                                natn_cd: str,
                                tr_mket_cd: str,
                                inqr_dvsn_cd: str):
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "appKey":config['APP_KEY'],
        "appSecret":config['APP_SECRET'],
        "tr_id":"CTRP6504R",
        "tr_cont": "",
        "custtpye": "P",
        "mac_address": f'{getmac.get_mac_address()}'}
    params = {"CANO": cano,
            "ACNT_PRDT_CD": acnt_prdt_cd,
            "WCRC_FRCR_DVSN_CD": wcrc_frcr_dvsn_cd,
            "NATN_CD": natn_cd,
            "TR_MKET_CD": tr_mket_cd,
            "INQR_DVSN_CD": inqr_dvsn_cd}

    PATH = "uapi/overseas-stock/v1/trading/inquire-present-balance"
    URL = f"{config['URL_BASE']}/{PATH}"

    res = requests.get(URL, headers=headers, params=params)

    return res.json()


if __name__ == '__main__':
    from pprint import pprint
    import time
    from get_access_token import get_access_token
    
    data = {'cano': '46491254',
            'acnt_prdt_cd': '01',
            'wcrc_frcr_dvsn_cd': '02',
            'natn_cd': '000',
            'tr_mket_cd': '01',
            'inqr_dvsn_cd': '00'}
    
    while True:
        res = get_inquire_present_balance(**data)
        
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

    
    print(f'RESPONSE         >>> {res["msg1"]}')
    print(f'RESPONSE CODE    >>> {res["msg_cd"]}')
    print()
    
    print('종목별 상세')
    for i in range(len(res['output1'])):
        print('='*15, f'    {i}    ', '='*15)
        print(f'거래시장           >>> {res["output1"][i]["tr_mket_name"]}')
        print(f'국가               >>> {res["output1"][i]["natn_kor_name"]}')
        print(f'해외거래소코드     >>> {res["output1"][i]["ovrs_excg_cd"]}')
        print(f'종목연동거래소코드 >>> {res["output1"][i]["item_lnkg_excg_cd"]}')
        print(f'상품명             >>> {res["output1"][i]["prdt_name"]}')
        print(f'상품번호           >>> {res["output1"][i]["pdno"]}') # 종목코드
        print(f'표준상품번호       >>> {res["output1"][i]["std_pdno"]}')
        print(f'상품유형코드       >>> {res["output1"][i]["prdt_type_cd"]}')
        print(f'유가증권구분명     >>> {res["output1"][i]["scts_dvsn_name"]}') # 현금, 미니스탁 등등...
        print(f'매수동화코드       >>> $ {res["output1"][i]["buy_crcy_cd"]}')
        print(f'기준환율           >>> $ {res["output1"][i]["bass_exrt"]}')
        print(f'현재가             >>> $ {res["output1"][i]["ovrs_now_pric1"]}')
        print(f'평균단가           >>> $ {res["output1"][i]["avg_unpr3"]}')
        print(f'잔고수량           >>> {res["output1"][i]["cblc_qty13"]}')
        print(f'당일매수체결수량   >>> {res["output1"][i]["thdt_buy_ccld_qty1"]}')
        print(f'당일매수체결금액   >>> $ {res["output1"][i]["thdt_buy_ccld_frcr_amt"]}')
        print(f'당일매도체결수량   >>> {res["output1"][i]["thdt_sll_ccld_qty1"]}')
        print(f'당일매도체결금액   >>> $ {res["output1"][i]["thdt_sll_ccld_frcr_amt"]}')
        print(f'체결수량합계       >>> {res["output1"][i]["ccld_qty_smtl1"]}') # 총 가지고 있는 주식의 수
        print(f'주문가능수량       >>> {res["output1"][i]["ord_psbl_qty1"]}')
        print(f'외화매입금액       >>> $ {res["output1"][i]["frcr_pchs_amt"]}') # 산 가격
        print(f'외화평가금액       >>> $ {res["output1"][i]["frcr_evlu_amt2"]}') # 현재 가격
        print(f'평가손익금액       >>> $ {res["output1"][i]["evlu_pfls_amt2"]}')
        print(f'평가손익율         >>> {res["output1"][i]["evlu_pfls_rt1"]} %')
        print(f'매입잔액원화       >>> ₩ {res["output1"][i]["pchs_rmnd_wcrc_amt"]}')
        print(f'단위금액           >>> {res["output1"][i]["unit_amt"]}')
        print(f'대출잔액           >>> {res["output1"][i]["loan_rmnd"]}')
        print(f'대출일자           >>> {res["output1"][i]["loan_dt"]}')
        print(f'대출만기일자       >>> {res["output1"][i]["loan_expd_dt"]}')
        print()
    
    print('통화별 상세')
    for i in range(len(res['output2'])):
        print()
        print(f'통화코드           >>> {res["output2"][i]["crcy_cd"]}')
        print(f'통화코드명         >>> {res["output2"][i]["crcy_cd_name"]}')
        print(f'외화매수급액합계   >>> $ {res["output2"][i]["frcr_buy_amt_smtl"]}')
        print(f'외화매도급액합계   >>> $ {res["output2"][i]["frcr_sll_amt_smtl"]}')
        print(f'외화예수금액       >>> $ {res["output2"][i]["frcr_dncl_amt_2"]}')
        print(f'최초고시환율       >>> $ {res["output2"][i]["frst_bltn_exrt"]}')
        print(f'외화매수증거금액   >>> $ {res["output2"][i]["frcr_buy_mgn_amt"]}')
        print(f'외화기타증거금     >>> $ {res["output2"][i]["frcr_etc_mgna"]}')
        print(f'외화출금가능금액   >>> $ {res["output2"][i]["frcr_drwg_psbl_amt_1"]}')
        print(f'외화평가금액       >>> $ {res["output2"][i]["frcr_evlu_amt2"]}') # 외화 출금가능 금액을 원화로 표현
        print(f'익일외화출금가능액 >>> $ {res["output2"][i]["nxdy_frcr_drwg_psbl_amt"]}')
        print(f'현지보관동화여부   >>> {res["output2"][i]["acpl_cstd_crcy_yn"]}')
        print()    

    print('계좌 종합')
    print()
    print(f'매입금액합계       >>> ₩ {res["output3"]["pchs_amt_smtl"]}')
    print(f'평가금액합계       >>> ₩ {res["output3"]["evlu_amt_smtl"]}')
    print(f'평가손익금액합계   >>> ₩ {res["output3"]["evlu_pfls_amt_smtl"]}')
    print(f'예수금             >>> ₩ {res["output3"]["dncl_amt"]}')
    print(f'CMA평가금액        >>> ₩ {res["output3"]["cma_evlu_amt"]}')
    print(f'총예수금액         >>> ₩ {res["output3"]["tot_dncl_amt"]}')
    print(f'기타증거금         >>> ₩ {res["output3"]["etc_mgna"]}')
    print(f'인출가능총금액     >>> ₩ {res["output3"]["wdrw_psbl_tot_amt"]}')
    print(f'외화평가총액       >>> ₩ {res["output3"]["frcr_evlu_tota"]}')
    print(f'평가수익율         >>> {res["output3"]["evlu_erng_rt1"]} %') # ?
    print(f'매입금액합계       >>> ₩ {res["output3"]["pchs_amt_smtl_amt"]}')
    print(f'평가금액합계       >>> ₩ {res["output3"]["evlu_amt_smtl_amt"]}')
    print(f'총평가손익금액     >>> ₩ {res["output3"]["tot_evlu_pfls_amt"]}')
    print(f'총자산금액         >>> ₩ {res["output3"]["tot_asst_amt"]}')
    print(f'매수증거금액       >>> ₩ {res["output3"]["buy_mgn_amt"]}')
    print(f'증거금총액         >>> ₩ {res["output3"]["mgna_tota"]}')
    print(f'외화사용가능금액   >>> ₩ {res["output3"]["frcr_use_psbl_amt"]}')
    print(f'미결제매수금액합계 >>> ₩ {res["output3"]["ustl_buy_amt_smtl"]}')
    print(f'미결제매도금액합계 >>> ₩ {res["output3"]["ustl_sll_amt_smtl"]}')
    print(f'총외화잔고합계     >>> ₩ {res["output3"]["tot_frcr_cblc_smtl"]}')
    print(f'총대출금액         >>> ₩ {res["output3"]["tot_loan_amt"]}')
    
    print()
    print(f'성공실패여부       >>> {res["rt_cd"]}')

