# NOTE Need to install below using python -m pip install -U requests_html
import requests_html
import pandas as pd
import time
import os
from pathlib import Path
_currpath = Path(__file__).parent


def GetAliceBlueBrokerages():
    # # Alice Blue
    session = requests_html.HTMLSession()
    r = session.get('https://aliceblueonline.com/margin-calculator/equity/')
    r.html.render(sleep=5)
    items = r.html.find("table#employee_data", first=True)
    session.close()

    rows_list = []
    for item in items.find("tr"):
        data = [td.text for td in item.find("th,td")]
        rows_list.append({"symbol": data[1], "MIS_margin_X_times": data[2],
                          "CNC_margin_X_times": data[3]})
    # print(rows_list)
    df_AliceB = pd.DataFrame(rows_list)
    df_AliceB["MIS_margin_X_times"] = df_AliceB["MIS_margin_X_times"].str.replace(
        '[\D]', '').replace('', 0)
    df_AliceB["CNC_margin_X_times"] = df_AliceB["CNC_margin_X_times"].str.replace(
        '[\D]', '').replace('', 0)
    df_AliceB.to_csv(os.path.join(_currpath, "brokerage_aliceblue_equity.csv"))
    print("Fetched brokerages for Aliceblue")
    return df_AliceB
    # # END: Alice Blue


def GetZerodhaBrokerages():
    # # Zerodha
    session = requests_html.HTMLSession()
    r = session.get('https://zerodha.com/margin-calculator/Equity/')
    r.html.render(sleep=5)
    items = r.html.find("table#table", first=True)
    session.close()

    rows_list = []
    for item in items.find("tr"):
        data = [td.text for td in item.find("th,td")]
        if len(data) > 4:
            rows_list.append({"symbol": data[0], "MIS_leverage_percent": data[1],
                              "MIS_margin_X_times": data[2], "CO_leverage_percent": data[3],
                              "CO_margin_X_times": data[4]})
    df_zerodha = pd.DataFrame(rows_list)
    df_zerodha["MIS_leverage_percent"] = df_zerodha["MIS_leverage_percent"].str.replace(
        '%', '')
    df_zerodha["MIS_margin_X_times"] = df_zerodha["MIS_margin_X_times"].str.replace(
        'x', '')
    df_zerodha["CO_leverage_percent"] = df_zerodha["CO_leverage_percent"].str.replace(
        '%', '')
    df_zerodha["CO_margin_X_times"] = df_zerodha["CO_margin_X_times"].str.replace(
        'x', '')
    # print(df_zerodha)
    df_zerodha.to_csv(os.path.join(_currpath, "brokerage_zerodha_equity.csv"))
    # #END : Zerodha
    return df_zerodha


def GetSymbolLev_Aliceblue(symbol, bkr="Aliceblue"):
    _currpath = Path(__file__).parent
    if bkr == "Aliceblue":
        pdtest = pd.read_csv(
            os.path.join(_currpath, "brokerage_aliceblue_equity.csv"))
        _filter = pdtest.loc[pdtest['symbol'].isin([symbol])]
        return _filter["MIS_margin_X_times"].values[0] if len(_filter) > 0 else 0


GetAliceBlueBrokerages()

# print(GetSymbolLev_Aliceblue("3MINDIA", bkr="Aliceblue"))
