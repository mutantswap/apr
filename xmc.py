import json
import os
from eth_account import Account
from web3 import Web3
from utils import (
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    ASHIBAM_ADDRESS,
    AVAX_ADDRESS,
    BNB_ADDRESS,
    EMPYR_ADDRESS,
    FLX_ADDRESS,
    MATIC_ADDRESS,
    convertFeesForPair,
    init_mc_maker,
    init_erc20,
    MCBAR_ADDRESS,
    MCOIN_ADDRESS,
    WNEAR_ADDRESS,
    WETH_ADDRESS,
    AURORA_ADDRESS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    WBTC_ADDRESS
)
from time import time, sleep
Account.enable_unaudited_hdwallet_features()

web3_url = os.getenv("AURORA_W3_URL", "https://testnet.aurora.dev/") #TODO change to mainnet
w3 = Web3(Web3.HTTPProvider(web3_url))
temp_mnemonic = "test test test test test test test test test test test junk"
acct = Account.from_mnemonic(mnemonic=temp_mnemonic)

mc_maker = init_mc_maker(w3)
mcoin = init_erc20(w3, MCOIN_ADDRESS)

pairs = [
    # (ATLUNA_ADDRESS, WNEAR_ADDRESS),
    # (ATUST_ADDRESS, WNEAR_ADDRESS),
    # (USDC_ADDRESS, WNEAR_ADDRESS),
    # (USDT_ADDRESS, WNEAR_ADDRESS),
    # (WBTC_ADDRESS, WNEAR_ADDRESS),
    # (MCOIN_ADDRESS, WNEAR_ADDRESS),
    (MCOIN_ADDRESS, USDC_ADDRESS),
    # (MCOIN_ADDRESS, USDT_ADDRESS),
    # (AURORA_ADDRESS, MCOIN_ADDRESS),
    # (WETH_ADDRESS, MCOIN_ADDRESS),
    # (WETH_ADDRESS, WNEAR_ADDRESS),
    # (WETH_ADDRESS, USDC_ADDRESS),
    # (WETH_ADDRESS, USDT_ADDRESS),
    # (AURORA_ADDRESS, WETH_ADDRESS),
    # (ASHIBAM_ADDRESS, WETH_ADDRESS),
    # (USDC_ADDRESS, USDT_ADDRESS),
    # (FLX_ADDRESS, WNEAR_ADDRESS),
    # (AVAX_ADDRESS, WNEAR_ADDRESS),
    # (BNB_ADDRESS, WNEAR_ADDRESS),
    # (MATIC_ADDRESS, WNEAR_ADDRESS),
    # (EMPYR_ADDRESS, USDC_ADDRESS),
    ]


mcoin_amount = 0
initial_mcBar_balance = mcoin.functions.balanceOf(MCBAR_ADDRESS).call()
current_time = time()

with open('xmc.json') as json_file:
    xmc_data = json.load(json_file)

for pair in pairs:
    mcoin_amount += convertFeesForPair(mc_maker, pair, w3, acct)
    print(mcoin_amount)

print(current_time, initial_mcBar_balance, mcoin_amount)


if xmc_data["timestamp"] != 0:
    timedelta = current_time - xmc_data["timestamp"]
    pr = mcoin_amount/initial_mcBar_balance
    apr = pr*(3600*24*365)*100/timedelta
    xmc_data["apr"] = apr

xmc_data["mcBarMcoin"] = initial_mcBar_balance
xmc_data["mintedMcoin"] = mcoin_amount
xmc_data["timestamp"] = current_time

with open('xmc.json', 'w', encoding='utf-8') as f:
    json.dump(xmc_data, f, ensure_ascii=False, indent=4)
