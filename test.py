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


api_key = "b79b1ec8-154d-4a89-a5a6-1acd1f4f79cd"
secret_key = "E6DE443863A5429D2E059D18CD588178"
passphrase = "170283"
swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)

# result = swapAPI.get_settings('ETH-USDT-SWAP')

# result = result = swapAPI.set_leverage(instrument_id='ETH-USDT-SWAP', leverage='3', side='3')

# print(result)
