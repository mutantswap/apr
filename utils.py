import json
import os
from eth_account import Account
from retry import retry
import requests
from urllib import parse

# TODO: Change address to mainnet
FACTORY_ADDRESS = "0xB934cF2B1eBFbC742B403568Db1Ef1B8EAD3fC56"
MCMAKER_ADDRESS = "0x5B2B3f681939F55021D78f2e22cCba1342f1821F"
MCBAR_ADDRESS = "0x2cf8D731898AF2976e23089fc33FbA7F740c3B4c"
CHEF_ADDRESS = "0x339E5B27Fd074dF8090e2E3d65b27B8628c274a3"
CHEFV2_ADDRESS = "0xd616ab1aa6f629cE23476BA6133F47dC58Ddbfa9"
MC_ADDRESS = "0x46B9C67951B9356A7b64F3d3460512c77F570d6D"
WNEAR_ADDRESS = "0xcCdE08a3A0C3Defd5b29323AAc5187581eb36B78"
AURORA_ADDRESS = "0x8BEc47865aDe3B172A928df8f990Bc7f2A3b9f79"
USDC_ADDRESS = "0x99635152E74e0412E8288B955f1E0C9D9ba5A033"
USDT_ADDRESS = "0x4988a896b1227218e4A686fdE5EabdcAbd91571f"
WETH_ADDRESS = "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB"
WBTC_ADDRESS = "0xF4eB217Ba2454613b15dBdea6e5f22276410e89e"
ATLUNA_ADDRESS = "0xC4bdd27c33ec7daa6fcfd8532ddB524Bf4038096"
ATUST_ADDRESS = "0x5ce9F0B6AFb36135b5ddBF11705cEB65E634A9dC"
ASHIBAM_ADDRESS = "0x48687fB162A735a3FedD47a98Fcbf58Be3ed4538"
FLX_ADDRESS = "0xea62791aa682d455614eaA2A12Ba3d9A2fD197af"
EMPYR_ADDRESS = "0xE9F226a228Eb58d408FdB94c3ED5A18AF6968fE1"
AVAX_ADDRESS = "0x80A16016cC4A2E6a2CACA8a4a498b1699fF0f844"
BNB_ADDRESS = "0x2bF9b864cdc97b08B6D79ad4663e71B8aB65c45c"
MATIC_ADDRESS = "0x6aB6d61428fde76768D7b45D8BFeec19c6eF91A8"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
MECHA_ADDRESS = "0xa33C3B53694419824722C10D99ad7cB16Ea62754"
META_ADDRESS = "0xc21Ff01229e982d7c8b8691163B0A3Cb8F357453"
XNL_ADDRESS = "0x7cA1C28663b76CFDe424A9494555B94846205585"
GBA_ADDRESS = "0xc2ac78FFdDf39e5cD6D83bbD70c1D67517C467eF"

### MSLP addresses
WNEAR_USDC = "0xA6335CCdAa874bb9E0cffDdA4e49F3186435B320"
WETH_USDC = "0x2F41AF687164062f118297cA10751F4b55478ae1"
WNEAR_MC = "0x0348fA0B2289beFa36956F3C95135572C2bc61B3"
MC_AURORA = "0xd1654a7713617d41A8C9530Fb9B948d00e162194"
MECHA_WNEAR = "0xd62f9ec4C4d323A0C111d5e78b77eA33A2AA862f"
META_WNEAR = "0xa8CAaf35c0136033294dD286A14051fBf37aed07"
GBA_USDT = "0x7B273238C6DD0453C160f305df35c350a123E505"

def init_chef(w3):
    with open('abi/chef.json') as json_file:
        return w3.eth.contract(
            address=CHEF_ADDRESS,
            abi=json.load(json_file)
        )

def init_chefv2(w3):
    with open('abi/chefv2.json') as json_file:
        return w3.eth.contract(
            address=CHEFV2_ADDRESS,
            abi=json.load(json_file)
        )

def init_rewarder(w3, rewarderAddress):
    with open('abi/complexrewarder.json') as json_file:
        return w3.eth.contract(
            address=rewarderAddress,
            abi=json.load(json_file)
        )

def init_tlp(w3, lpAddress):
    with open('abi/tlp.json') as json_file:
        return w3.eth.contract(
            address=lpAddress,
            abi=json.load(json_file)
        )

def init_tri_maker(w3):
    with open('abi/triMaker.json') as json_file:
        return w3.eth.contract(
            address=MCMAKER_ADDRESS,
            abi=json.load(json_file)
        )

def init_erc20(w3, erc20_address):
    with open('abi/erc20.json') as json_file:
        return w3.eth.contract(
            address=erc20_address,
            abi=json.load(json_file)
        )


def getReserveInUsdc(w3, tlp, triUsdcRatio):
    t0 = tlp.functions.token0().call()
    t1 = tlp.functions.token1().call()
    reserves = tlp.functions.getReserves().call()
    if (t0 == USDC_ADDRESS or t1 == USDC_ADDRESS):
        if t0 == USDC_ADDRESS:
            return reserves[0]*2
        else:
            return reserves[1]*2
    elif (t0 == WNEAR_ADDRESS or t1 == WNEAR_ADDRESS):
        wnearUsdcPair = init_tlp(w3, WNEAR_USDC)
        reservesWnearUsdc = wnearUsdcPair.functions.getReserves().call()
        t0WnearUsdc = wnearUsdcPair.functions.token0().call()
        if t0 == WNEAR_ADDRESS:
            reserveInWnear = reserves[0]*2
        else:
            reserveInWnear = reserves[1]*2
        if t0WnearUsdc == WNEAR_ADDRESS:
            wnearReserveInWNearUsdcPair = reservesWnearUsdc[0]
            usdcReserveInWNearUsdcPair = reservesWnearUsdc[1]
        else:
            wnearReserveInWNearUsdcPair = reservesWnearUsdc[1]
            usdcReserveInWNearUsdcPair = reservesWnearUsdc[0]
        return reserveInWnear*usdcReserveInWNearUsdcPair/wnearReserveInWNearUsdcPair
    elif (t0 == WETH_ADDRESS or t1 == WETH_ADDRESS):
        wethUsdcPair = init_tlp(w3, WETH_USDC)
        reservesWethUsdc = wethUsdcPair.functions.getReserves().call()
        t0WethUsdc = wethUsdcPair.functions.token0().call()
        if t0 == WETH_ADDRESS:
            reserveInWeth = reserves[0]*2
        else:
            reserveInWeth = reserves[1]*2
        if t0WethUsdc == WETH_ADDRESS:
            wethReserveInWethUsdcPair = reservesWethUsdc[0]
            usdcReserveInWethUsdcPair = reservesWethUsdc[1]
        else:
            wethReserveInWethUsdcPair = reservesWethUsdc[1]
            usdcReserveInWethUsdcPair = reservesWethUsdc[0]
        return reserveInWeth*usdcReserveInWethUsdcPair/wethReserveInWethUsdcPair
    elif (t0 == MC_ADDRESS or t1 == MC_ADDRESS ):
        if t0 == MC_ADDRESS:
            reserveInTri = reserves[0]*2
        else:
            reserveInTri = reserves[1]*2
        return reserveInTri/triUsdcRatio
    elif (t0 == MCBAR_ADDRESS or t1 == MCBAR_ADDRESS ):
        if t0 == MCBAR_ADDRESS:
            reserveInXTri = reserves[0]*2
        else:
            reserveInXTri = reserves[1]*2
        return reserveInXTri*getTriXTriRatio(w3)/triUsdcRatio
    # TODO FIX ME -- TEMPORARY COPY CODE TO UNBLOCK
    elif (t0 == XNL_ADDRESS or t1 == XNL_ADDRESS ):
        if t0 == XNL_ADDRESS:
            reserveInTri = reserves[0]*2
        else:
            reserveInTri = reserves[1]*2
        return reserveInTri/triUsdcRatio
    elif (t0 == USDT_ADDRESS or t1 == USDT_ADDRESS):
        if t0 == USDT_ADDRESS:
            return reserves[0]*2
        else:
            return reserves[1]*2


def getTotalStakedInUSDC(totalStaked, totalAvailable, reserveInUSDC):
    if totalAvailable == 0:
        return 0
    else:
        return totalStaked*reserveInUSDC/totalAvailable


def getWnearUsdcRatio(w3):
    usdcWnearPair = init_tlp(w3, WNEAR_USDC)
    t1 = usdcWnearPair.functions.token1().call()
    t0 = usdcWnearPair.functions.token0().call()
    reserves = usdcWnearPair.functions.getReserves().call()

    if t0 == WNEAR_ADDRESS:
        wnearUsdcRatio = reserves[0]/reserves[1]
    else:
        wnearUsdcRatio = reserves[1]/reserves[0]
    return wnearUsdcRatio

def getGbaUsdcRatio(w3):
    gbaUSDTPair = init_tlp(w3, GBA_USDT)
    t1 = gbaUSDTPair.functions.token1().call()
    t0 = gbaUSDTPair.functions.token0().call()
    reserves = gbaUSDTPair.functions.getReserves().call()

    if t0 == GBA_ADDRESS:
        gbaUsdcRatio = reserves[0]/reserves[1]
    else:
        gbaUsdcRatio = reserves[1]/reserves[0]
    return gbaUsdcRatio

def getMCUsdcRatio(w3, wnearUsdcRatio):
    mcWnearPair = init_tlp(w3, WNEAR_MC)
    t1 = mcWnearPair.functions.token1().call()
    t0 = mcWnearPair.functions.token0().call()
    reserves = mcWnearPair.functions.getReserves().call()
    if t0 == WNEAR_ADDRESS:
        mcWnearRatio = reserves[1]/reserves[0]
    else:
        mcWnearRatio = reserves[0]/reserves[1]
    return mcWnearRatio * wnearUsdcRatio

def getAuroraUsdcRatio(w3, triUsdcRatio):
    triAuroraPair = init_tlp(w3, MC_AURORA)
    t1 = triAuroraPair.functions.token1().call()
    t0 = triAuroraPair.functions.token0().call()
    reserves = triAuroraPair.functions.getReserves().call()
    if t0 == MC_ADDRESS:
        triAuroraRatio = reserves[1]/reserves[0]
    else:
        triAuroraRatio = reserves[0]/reserves[1]
    return triAuroraRatio * triUsdcRatio

def getMechaUsdcRatio(w3, wnearUsdcRatio):
    mechaWnearPair = init_tlp(w3, MECHA_WNEAR)
    t1 = mechaWnearPair.functions.token1().call()
    t0 = mechaWnearPair.functions.token0().call()
    reserves = mechaWnearPair.functions.getReserves().call()

    if t0 == MECHA_ADDRESS:
        mechaWnearRatio = reserves[0]/reserves[1]
    else:
        mechaWnearRatio = reserves[1]/reserves[0]

    return mechaWnearRatio * wnearUsdcRatio

def getMetaUsdcRatio(w3, wnearUsdcRatio):
    metaWnearPair = init_tlp(w3, META_WNEAR)
    t1 = metaWnearPair.functions.token1().call()
    t0 = metaWnearPair.functions.token0().call()
    reserves = metaWnearPair.functions.getReserves().call()

    if t0 == META_ADDRESS:
        metaWnearPair = reserves[0]/reserves[1]
    else:
        metaWnearPair = reserves[1]/reserves[0]

    return metaWnearPair * wnearUsdcRatio

def getTriXTriRatio(w3):
    xtri = init_erc20(w3, MCBAR_ADDRESS)
    tri = init_erc20(w3, MC_ADDRESS)
    xtri_supply = xtri.functions.totalSupply().call()
    tri_locked = tri.functions.balanceOf(MCBAR_ADDRESS).call()
    return tri_locked/xtri_supply


def getCoingeckoPriceRatio(asset):
    try:
        coingecko_api_key = os.getenv("COINGECKO_API_KEY")
        coingecko_query_params = {"ids": asset, "vs_currencies": "usd"}

        if coingecko_api_key:
            coingecko_query_params["x_cg_pro_api_key"] = coingecko_api_key
            coingecko_api_endpoint_root = "https://pro-api.coingecko.com/api/v3/simple/price"
        else:
            coingecko_api_endpoint_root = "https://api.coingecko.com/api/v3/simple/price"

        coingecko_encoded_query_params = parse.urlencode(coingecko_query_params, doseq=False)
        coingecko_api_endpoint = f"{coingecko_api_endpoint_root}?{coingecko_encoded_query_params}"

        response = requests.get(coingecko_api_endpoint)
        usd_price = (response.json()[asset]['usd'])
        return 1/usd_price
    except requests.exceptions.RequestException as e:
        print(f"Coingecko API Call Error: {e}")
        return 0




def getAPR(triUsdRatio, totalRewardRate, totalStakedInUSDC):
    if totalStakedInUSDC == 0:
        return 0
    else:
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return totalYearlyRewards*100*10**6/(totalStakedInUSDC*triUsdRatio)

@retry((ValueError), delay=10, tries=5)
def convertFeesForPair(tri_maker, pair, w3, acct):
    tri_amount = 0
    try:
        transaction = {
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.getTransactionCount(acct.address),
        }
        convert_tranasction = tri_maker.functions.convert(pair[0], pair[1]).buildTransaction(transaction)
        signed = w3.eth.account.sign_transaction(convert_tranasction, acct.key)
        signed_txn = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hash = signed_txn.hex()
        receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=1200)
        for l in receipt['logs']:
            if (l['topics'][0].hex() == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef' and l['topics'][2].hex() == "0x000000000000000000000000802119e4e253d5c19aa06a5d567c5a41596d6803"):
                tri_amount += int(l['data'], 16)
    except ValueError as e:
        if str(e).find('INSUFFICIENT_LIQUIDITY_BURNED') == -1:
            raise e
    return tri_amount

def getAccount(mnemonic):
    # Needed to use `from_mnemonic`
    Account.enable_unaudited_hdwallet_features()

    return Account.from_mnemonic(mnemonic=mnemonic)

def getFundedAccount():
    mnemonic = os.getenv("AURORA_FUNDED_MNEMONIC")
    if (mnemonic is None):
        raise ValueError('[utils::getFundedAccount] env var AURORA_FUNDED_MNEMONIC is None')

    acct = getAccount(mnemonic)

    print('[utils::getFundedAccount] Using funded account: ' + acct.address)

    return acct
