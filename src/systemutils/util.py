from pathlib import Path
import os
import sys
import logging
from alice_blue import *
import datetime
import json
from sqlalchemy import create_engine, pool


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


base_path = get_project_root()
date_time_now = datetime.datetime.now()


def loadJson(filename=""):  # This helps in reading JSON files
    with open(filename, mode="r") as json_file:
        data = json.load(json_file)
        return data


def getAliceBlueObj():
    try:
        cred_data = loadJson(os.path.join(
            base_path, "credentials", "env_credential.json"))
        access_token = doGetTokenforToday()
        alice_obj = AliceBlue(username=cred_data["alice"]["username"], password=cred_data["alice"]["password"],
                              access_token=access_token, master_contracts_to_download=cred_data["alice"]["contracts"])
        return alice_obj
    except Exception as e:
        print(e)
        pass


def get_sqlengine():
    system_cred = loadJson(os.path.join(
        base_path, "credentials", "env_credential.json"))
    msql_engine = create_engine("mysql+pymysql://{user}:{pw}@{endpoint}:3306/{db}"
                                .format(endpoint=system_cred["mysql"]["endpoint"],
                                        user=system_cred["mysql"]["username"],
                                        pw=system_cred["mysql"]["password"],
                                        
                                        db=system_cred["mysql"]["dbschema"]))
    return msql_engine


def doGetTokenforToday():
    try:
        base_path = get_project_root()
        # print(base_path)
        system_cred = loadJson(os.path.join(
            base_path, "credentials", "env_credential.json"))
        cred_data = system_cred
        daily_token_file = os.path.join(
            base_path, "credentials", "day_access_token.json")

        if(os.path.exists(daily_token_file)):
            data = loadJson(daily_token_file)
            if "access_token" in data and data["date"] == date_time_now.strftime("%Y-%m-%d") and isinstance(data["access_token"], str):
                return data["access_token"]
            else:
                access_token = AliceBlue.login_and_get_access_token(
                    username=cred_data["alice"]["username"], password=cred_data["alice"]["password"], twoFA=cred_data["alice"]["twoFA"],  api_secret=cred_data["alice"]["api_secret"])
                json_data = {"access_token": access_token, "broker": "ALICE",
                             "date": date_time_now.strftime("%Y-%m-%d")}
                with open(daily_token_file, "w") as outfile:
                    json.dump(json_data, outfile)
                    return access_token
        else:
            access_token = AliceBlue.login_and_get_access_token(
                username=cred_data["alice"]["username"], password=cred_data["alice"]["password"], twoFA=cred_data["alice"]["twoFA"],  api_secret=cred_data["alice"]["api_secret"])
            json_dataa = {"access_token": access_token, "broker": "ALICE",
                          "date": date_time_now.strftime("%Y-%m-%d")}
            with open(daily_token_file, "w") as outfile:
                json.dump(json_dataa, outfile)
                return access_token
    except Exception as e:
        print(e)
        pass


def get_percentage_diff(a, b):
    '''
    Returns percentage difference between the two values
    (ex: a=210 b= 208)
    '''
    result = float((abs(a-b) * 100) / a)
    return round(result, 3)


def add_sub_percent_to_val(val, per):
    '''
    Increments or decrements a value by given percentage
    (ex: val=50, per=3)
    '''
    return round(val+(val*per/100), 3)
