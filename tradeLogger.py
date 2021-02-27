import atexit
import time
import sqlite3
import logging
from alice_blue import *
import json
import datetime

from numpy.lib import utils
from src.systemutils import util
import os
from pathlib import Path
from threading import Thread
from sqlalchemy import create_engine, pool
import pandas as pd
from src.systemutils import tel_msgr
from src.broker_tasks import bkr_alice
import talib.abstract as ta
from src.data_scrubber import data_scrub
logging.basicConfig(level=logging.INFO)

date_time_now = datetime.datetime.now()
socket_opened = False
base_path = util.get_project_root()
db_file_path = os.path.join(base_path, "src", "data", "stock_data_db.db")
tel_utl = tel_msgr.TelUtil()


class clprepare_journal(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.symbol_query = "SELECT scripname, order_id, date FROM order_book where date(date)=date('now')"
        self.msql_engine = util.get_sqlengine()
        self.starting_time = int(9) * 60 + int(14)
        self.closing_minutes = int(15) * 60 + int(10)
        self.alice_access_token = util.doGetTokenforToday()
        self.alice = util.getAliceBlueObj()
        self.lite_conn = sqlite3.connect(
            db_file_path, check_same_thread=False, timeout=10, isolation_level="DEFERRED")
        self.c = self.lite_conn.cursor()
        self.lite_conn.execute("PRAGMA journal_mode = WAL")
        self.lite_conn.execute("PRAGMA cache_size=10000")
        self.ds = data_scrub.DS()
        atexit.register(self.cleanup)

    def loadJson(self, filename=""):  # This helps in reading JSON files
        with open(filename, mode="r") as json_file:
            data = json.load(json_file)
            return data

    def cleanup(self):  # Dont leave your footprints dispose whats not needed after job is done
        self.msql_engine.dispose()
        self.lite_conn.close()

    def run_main(self):
        day_wise_positions = self.alice.get_daywise_positions()
        df = pd.read_json(json.dumps(
            day_wise_positions["data"]["positions"]), orient='records')

        df["day_pnl"] = round(df["realised_pnl"].sum(), 3)
        df["trade_day"] = datetime.datetime.now().strftime("%Y-%m-%d")

        alice_get_balance = self.alice.get_balance()
        final_credits = 0.0
        for rec in alice_get_balance["data"]["cash_positions"]:
            if rec["category"] == 'ABFS-COMMON':
                final_credits = rec['net']

        print(final_credits)

        df = df[["trading_symbol", "total_buy_quantity", "product", "exchange", "buy_quantity", "sell_quantity", "net_quantity", "oms_order_id", "realised_pnl", "close_price",
                 "buy_amount", "sell_amount", "day_pnl", "trade_day"]]
        df.reset_index(inplace=True)
        df.drop(columns=["index"], inplace=True)
        df["capital"] = float(final_credits)
        # print(df)
        df.to_sql("trade_journal_alice", con=self.msql_engine,
                  if_exists='append', chunksize=1000, method='multi', index=False)
        if len(df.index) > 0:
            tel_utl.sendMsg('''Total trades for today: {}                               
            <pre>Todays PnL   : {}</pre>
            Latest capital    : {}'''.format(
                len(df), df[1:]["day_pnl"].values[0], final_credits))


clss = clprepare_journal()
all_processes = []
socket_thread = Thread(target=clss.run_main(), name="socket_thread")
all_processes.append(socket_thread)
socket_thread.start()
