# okex_trade

在okex平台基于网格的自动交易程序。
是基于币币账号交易，交易币种LTC-USDT。

# 配置文件

<code>
{
    "initial_base_price": 230,
    "is_change": -1,
    "percent_down_buy": 0.04,
    "percent_up_sell": 0.045,
    "quantity_buy": 0.02,
    "quantity_sell": 0.02
}
</code>

initial_base_price是基准价格
is_change是更改确认，-1表示不更改，0表示更改。可以运行时更改
percent_down_buy表示每下跌多少买入
percent_up_sell表示每上涨多少卖出
quantity_buy表示买入数量
quantity_sell表示卖出数量

