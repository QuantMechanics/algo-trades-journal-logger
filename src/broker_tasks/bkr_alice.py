from src.systemutils import util
import logging
from alice_blue import *
import time
import json
logging.basicConfig(level=logging.INFO)


def place_order(scrip, aliceobj: any):
    resp = aliceobj.place_order(transaction_type=TransactionType.Buy,
                                instrument=aliceobj.get_instrument_by_symbol(
                                    'NSE', scrip),
                                quantity=5,
                                order_type=OrderType.Market,
                                product_type=ProductType.Intraday,
                                is_amo=False)
    return resp['data']['oms_order_id']


def place_cover_order(_scrip, aliceobj: any, _quantity: 1, _stoploss: 0, _trailing_stop_loss: 0, _trigger_price: 0):
    resp = aliceobj.place_order(transaction_type=TransactionType.Buy,
                                instrument=aliceobj.get_instrument_by_symbol(
                                    'NSE', _scrip),
                                quantity=_quantity,
                                order_type=OrderType.Market,
                                product_type=ProductType.CoverOrder,
                                price=0.0,
                                # trigger_price Here the trigger_price is taken as stop loss (provide stop loss in actual amount)
                                trigger_price=_stoploss,
                                stop_loss=None,
                                square_off=None,
                                trailing_sl=_trailing_stop_loss,
                                is_amo=False)
    print(resp)
    return resp['data']['oms_order_id']
