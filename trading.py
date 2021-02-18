#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import okex.information_api as information
import time
import logging
import datetime


def beijing(sec, what):
    beijing_time = datetime.datetime.now() + datetime.timedelta(hours=13)
    return beijing_time.timetuple()

logging.Formatter.converter = beijing
logging.basicConfig(filename='trading.log', format='%(asctime)s %(message)s', datefmt='%m %d %Y %I:%M:%S', level=logging.INFO)

class grid_trading():
    def __init__(self, initial_base_price=0, percent_up_sell=0, percent_down_buy=0, quantity_sell=0, quantity_buy=0):
        self.api_key = "b79b1ec8-154d-4a89-a5a6-1acd1f4f79cd"
        self.secret_key = "E6DE443863A5429D2E059D18CD588178"
        self.passphrase = "170283"
        self.spotAPI = spot.SpotAPI(self.api_key, self.secret_key, self.passphrase, False)

        self.initial_base_price = initial_base_price
        self.percent_up_sell = percent_up_sell
        self.percent_down_buy = percent_down_buy
        self.quantity_sell = quantity_sell
        self.quantity_buy = quantity_buy

        self.buy_price = initial_base_price * (1 - percent_down_buy)
        self.sell_price = initial_base_price * (1 + percent_up_sell)
        self.buy_trade_fee = self.quantity_buy * 0.0015
        self.sell_trade_fee = self.quantity_sell * 0.001

        self.total_amount = self.get_account_amount()
        self.total_position = self.get_account_position()
        # self.initial_amount = ''

    def get_current_price(self):
        last = self.spotAPI.get_specific_ticker('ETH-USDT')['last']
        return float(last)

    def get_account_amount(self):
        balance_ustd = self.spotAPI.get_coin_account_info('USDT')['balance']
        return float(balance_ustd)
    
    def get_account_position(self):
        balance_eth = self.spotAPI.get_coin_account_info('ETH')['balance']
        return float(balance_eth)

    def place_order(self, order_side, order_size, order_price):
        result = self.spotAPI.take_order(instrument_id='ETH-USDT', side=order_side, client_oid='', type='', size=order_size, price=order_price, order_type='0', notional='')
        return result
    
    def trading(self):
        current_price = self.get_current_price()
        if current_price < self.buy_price:
            if self.total_amount < current_price * self.quantity_buy:
                logging.info('账户余额不足')
                return False
            logging.info('buy price: %s', self.buy_price)
            logging.info('buy number: %s', self.quantity_buy)
        
            self.place_order(order_side='buy', order_size=self.quantity_buy, order_price=self.buy_price)
            self.total_amount -= self.buy_price * self.quantity_buy
            self.total_position += self.quantity_buy - self.buy_trade_fee
            
            self.initial_base_price = self.buy_price
            self.buy_price = self.initial_base_price * (1 - self.percent_down_buy)
            self.sell_price = self.initial_base_price * (1 + self.percent_up_sell)

        elif current_price > self.sell_price:
            if self.total_position < self.quantity_sell:
                logging.info('没有仓位')
                return False
            logging.info('sell price: %s', self.sell_price)
            logging.info('sell number: %s', self.quantity_sell)

            self.place_order(order_side='sell', order_size=self.quantity_sell, order_price=self.sell_price)
            self.total_amount += self.sell_price * self.quantity_sell
            self.total_position -= self.quantity_sell + self.sell_trade_fee

            self.initial_base_price = self.sell_price
            self.buy_price = self.initial_base_price * (1 - self.percent_down_buy)
            self.sell_price = self.initial_base_price * (1 + self.percent_up_sell)

def start():
    initial_base_price = 1800
    percent_down_buy = 0.01
    percent_up_sell = 0.02
    quantity_buy = 0.001
    quantity_sell = 0.001

    ex = grid_trading(initial_base_price, percent_up_sell, percent_down_buy, quantity_sell, quantity_buy)
    cnt = 0
    while True:
        ex.trading()        
        current_price = ex.get_current_price()
        time.sleep(1)
        if cnt % 5 == 0:
            logging.info(' USDT: %s ETH: %s 当前价格: %s 网格买入价格: %s 网格卖出价格: %s。' % (str(ex.total_amount), str(ex.total_position), str(current_price), str(ex.buy_price), str(ex.sell_price)))


if __name__ == '__main__':
    start()
