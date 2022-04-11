import os
from web3 import Web3
from utils import (
    ATLUNA_ADDRESS,
    ATUST_ADDRESS,
    ASHIBAM_ADDRESS,
    convertFeesForPair,
    getAccount,
    getFundedAccount,
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

pairs = [
    (ATLUNA_ADDRESS, WNEAR_ADDRESS),
    (ATUST_ADDRESS, WNEAR_ADDRESS),
    (USDC_ADDRESS, WNEAR_ADDRESS),
    (USDT_ADDRESS, WNEAR_ADDRESS),
    (WBTC_ADDRESS, WNEAR_ADDRESS),
    (MCOIN_ADDRESS, WNEAR_ADDRESS),
    (MCOIN_ADDRESS, USDC_ADDRESS),
    (MCOIN_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, MCOIN_ADDRESS),
    (WETH_ADDRESS, MCOIN_ADDRESS),
    (WETH_ADDRESS, WNEAR_ADDRESS),
    (WETH_ADDRESS, USDC_ADDRESS),
    (WETH_ADDRESS, USDT_ADDRESS),
    (AURORA_ADDRESS, WETH_ADDRESS),
    (ASHIBAM_ADDRESS, WETH_ADDRESS),
    (USDC_ADDRESS, USDT_ADDRESS),
    ]

TAG = "[GCC_XMC_BASE] "

def xmc_base(timestamp):
    web3_url = os.getenv("AURORA_W3_URL", "https://testnet.aurora.dev/") #TODO change to mainnet
    w3 = Web3(Web3.HTTPProvider(web3_url))
    try:
        # 2/8/22 - Total cost of a complete run is 0.00016Ξ
        acct = getFundedAccount()
    except:
        temp_mnemonic = "test test test test test test test test test test test junk"
        acct = getAccount(temp_mnemonic)

    print('xmc acct balance: ' + str(w3.eth.get_balance(acct.address)/1e18) + 'Ξ')

    mc_maker = init_mc_maker(w3)
    mcoin = init_erc20(w3, MCOIN_ADDRESS)

    mcoin_amount = 0
    initial_mcBar_balance = mcoin.functions.balanceOf(MCBAR_ADDRESS).call()
    current_time = time()

    xmc_data = {}

    for pair in pairs:
        sleep(5)
        mcoin_amount += convertFeesForPair(mc_maker, pair, w3, acct)
        print(TAG, 'mcoin_amount: ',  mcoin_amount)

    print(TAG, current_time, initial_mcBar_balance, mcoin_amount)


    if timestamp != 0 and timestamp != None:
        timedelta = current_time - timestamp
        pr = mcoin_amount/initial_mcBar_balance
        apr = pr*(3600*24*365)*100/timedelta
        xmc_data["apr"] = apr

    xmc_data["mcBarMcoin"] = initial_mcBar_balance
    xmc_data["mintedMcoin"] = mcoin_amount
    xmc_data["timestamp"] = current_time

    return xmc_data
