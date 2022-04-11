import os
import json
from web3 import Web3
from utils import (
    CHEFV2_ADDRESS,
    ZERO_ADDRESS,
    getMetaUsdcRatio,
    getWnearUsdcRatio,
    init_chef,
    init_chefv2,
    init_rewarder,
    init_tlp,
    getReserveInUsdc,
    getTotalStakedInUSDC,
    getAPR,
    getMCUsdcRatio,
    getAuroraUsdcRatio,
    getCoingeckoPriceRatio,
    getMechaUsdcRatio,
    getGbaUsdcRatio
)


v1_pools = {
    0: "0x00dbf792f23D162Bcf84F9BC979CAc15025D9F8c", #MCOIN-fNear
    1: "0x433FCcF7df0A8b8c31A31C74A6EA917aAB520d70", #fNear-fUSDC
    2: "0xd2D3EB8Ee7341B8a6AF8C499CF3DeC6c0a45fF27", #MCOIN-fUSDC
    # Old chef pools
    # 0: "0xaF00ba46B3e7Fea7E39fF320534677a51B88D39C",
    # 1: "0x43413cAB62F19e2B347dC50504bf21fE0DCE3790",
    # 2: "0x62c1e1dadEbDEDa9FF397a48239D2D0a1E4E71C8",
    # 3: "0x0348fA0B2289beFa36956F3C95135572C2bc61B3",
    # 4: "0xA6335CCdAa874bb9E0cffDdA4e49F3186435B320",
}

v2_pools = {
        # 0: {
        #     "LP": "0x5eeC60F348cB1D661E4A5122CF4638c7DB7A886e",
        #     "Aurora Rewarder": "0x94669d7a170bfe62FAc297061663e0B48C63B9B5"
        #     },
        # 1: {
        #     "LP": "0xd1654a7713617d41A8C9530Fb9B948d00e162194",
        #     "Aurora Rewarder": "0x78EdEeFdF8c3ad827228d07018578E89Cf159Df1"
        #     },
        # 2: {
        #     "LP": "0xdF8CbF89ad9b7dAFdd3e37acEc539eEcC8c47914",
        #     "Aurora Rewarder": "0x89F6628927fdFA2592E016Ba5B14389a4b08D681"
        #     },
        # 3: {
        #     "LP": "0xa9eded3E339b9cd92bB6DEF5c5379d678131fF90",
        #     "Aurora Rewarder": "0x17d1597ec86fD6aecbfE0F32Ab2F2aD9c37E6750"
        #     },
        # 4: {
        #     "LP": "0x61C9E05d1Cdb1b70856c7a2c53fA9c220830633c",
        #     "Aurora Rewarder": ZERO_ADDRESS
        #     },
        # 5: {
        #     "LP": "0x6443532841a5279cb04420E61Cf855cBEb70dc8C",
        #     "Aurora Rewarder": ZERO_ADDRESS
        #     },
        # 6: {
        #     "LP": "0x7be4a49AA41B34db70e539d4Ae43c7fBDf839DfA",
        #     "Aurora Rewarder": ZERO_ADDRESS
        #     },
        # 7: {
        #     "LP": "0x3dC236Ea01459F57EFc737A12BA3Bb5F3BFfD071",
        #     "Aurora Rewarder": ZERO_ADDRESS
        #     },
        # 8: {
        #     "LP": "0x48887cEEA1b8AD328d5254BeF774Be91B90FaA09",
        #     "Aurora Rewarder": "0x42b950FB4dd822ef04C4388450726EFbF1C3CF63"
        #     },
        # 9: {
        #     "LP": "0xd62f9ec4C4d323A0C111d5e78b77eA33A2AA862f",
        #     "Aurora Rewarder": "0x9847F7e33CCbC0542b05d15c5cf3aE2Ae092C057"
        #     },
        # 10: {
        #     "LP": "0xdDAdf88b007B95fEb42DDbd110034C9a8e9746F2",
        #     "Aurora Rewarder": "0xbbE41F699B0fB747cd4bA21067F6b27e0698Bc30"
        #     },
        # 11: {
        #     "LP": "0x5913f644A10d98c79F2e0b609988640187256373",
        #     "Aurora Rewarder": "0x7B9e31BbEdbfdc99e3CC8b879b9a3B1e379Ce530"
        #     },
        # 12: {
        #     "LP": "0x47924Ae4968832984F4091EEC537dfF5c38948a4",
        #     "Aurora Rewarder": "0xf267212F1D8888e0eD20BbB0c7C87A089cDe6E88"
        #     },
        # 13: {
        #     "LP": "0xb419ff9221039Bdca7bb92A131DD9CF7DEb9b8e5",
        #     "Aurora Rewarder": "0xb84293D04137c9061afe34118Dac9931df153826"
        #     },
        # 14: {
        #     "LP": "0xFBc4C42159A5575a772BebA7E3BF91DB508E127a",
        #     "Aurora Rewarder": "0x028Fbc4BB5787e340524EF41d95875Ac2C382101"
        #     },
        # 15: {
        #     "LP": "0x7B273238C6DD0453C160f305df35c350a123E505",
        #     "Aurora Rewarder": "0xDAc58A615E2A1a94D7fb726a96C273c057997D50"
        #     }
    }

web3_url = os.getenv("AURORA_W3_URL", "https://testnet.aurora.dev/")
w3 = Web3(Web3.HTTPProvider(web3_url))

def apr_base():
    print("Starting APR BASE")
    data = []
    ## chef calls
    decimals = 18
    chef = init_chef(w3)
    totalAllocPoint = chef.functions.totalAllocPoint().call()

    mcPerBlock = chef.functions.mcPerBlock().call()
    wnearUsdcRatio = getWnearUsdcRatio(w3)
    mcUsdcRatio = getMCUsdcRatio(w3, wnearUsdcRatio)
    # auroraUsdcRatio = getAuroraUsdcRatio(w3, mcUsdcRatio)
    # mechaUsdcRatio = getMechaUsdcRatio(w3, wnearUsdcRatio)
    # metaUsdcRatio = getMetaUsdcRatio(w3, wnearUsdcRatio)
    # lunaUsdcRatio = getCoingeckoPriceRatio("terra-luna")
    # flxUsdcRatio = getCoingeckoPriceRatio("flux-token")
    # solaceUsdcRatio = getCoingeckoPriceRatio("solace")
    # chronicleUsdcRatio = getCoingeckoPriceRatio("chronicle")
    # gbaUsdcRatio = getGbaUsdcRatio(w3)
    print(f"Near USDC Ratio: {wnearUsdcRatio/10**18}")
    print(f"MC USDC Ratio: {mcUsdcRatio/10**18}")
    # print(f"Aurora USDC Ratio: {auroraUsdcRatio/10**12}")
    # print(f"LUNA USDC Ratio: {lunaUsdcRatio}")
    # print(f"FLX USDC Ratio: {flxUsdcRatio}")
    # print(f"MECHA USDC Ratio: {mechaUsdcRatio/10**12}")
    # print(f"Solace USDC Ratio: {solaceUsdcRatio}")
    # print(f"Meta USDC Ratio: {metaUsdcRatio/10**18}")
    # print(f"Chronicle USDC Ratio: {chronicleUsdcRatio}")
    # print(f"GBA USDC Ratio: {gbaUsdcRatio/10**12}")

    for id, address in v1_pools.items():
        # if id < 3:
        #     data.append(
        #         {
        #             "id": id,
        #             "poolId": id,
        #             "lpAddress": address,
        #             "totalSupply": 0,
        #             "totalStaked": 0,
        #             "totalStakedInUSD": 0,
        #             "totalRewardRate": 0,
        #             "allocPoint": 0,
        #             "apr": 0,
        #             "apr2": 0,
        #             "chefVersion": "v1",
        #         }
        #     )
        #     continue
        print("V1 Reached here", address)
        tlp = init_tlp(w3, address)
        poolInfo = chef.functions.poolInfo(id).call()
        assert poolInfo[0].lower() == address.lower()
        allocPoint = poolInfo[1]
        print("V1 allocPoint", allocPoint)
        reserveInUSDC = getReserveInUsdc(w3, tlp, mcUsdcRatio)
        print("V1 reserveInUSDC", reserveInUSDC)
        totalSupply = tlp.functions.totalSupply().call()
        print("V1 totalSupply", totalSupply)
        totalStaked = tlp.functions.balanceOf(chef.address).call()
        print("V1 totalStaked", totalStaked)
        totalStakedInUSDC = getTotalStakedInUSDC(totalStaked, totalSupply, reserveInUSDC)
        print("V1 totalStakedInUSDC", totalStakedInUSDC)
        print("V1 mcPerBlock", mcPerBlock)
        print("V1 allocPoint", allocPoint)
        print("V1 totalAllocPoint", totalAllocPoint)
        totalSecondRewardRate = (
            mcPerBlock * allocPoint / (totalAllocPoint * 10 ** decimals)
        )  # TODO: update to return base 10 values
        print("V1 totalSecondRewardRate", totalSecondRewardRate)
        totalWeeklyRewardRate = (
            3600 * 24 * 7 * totalSecondRewardRate
        )  # TODO: update to return base 10 values
        print("V1 totalWeeklyRewardRate", totalWeeklyRewardRate)

        # Chef V1
        data.append(
            {
                "id": id,
                "poolId": id,
                "lpAddress": address,
                "totalSupply": totalSupply,
                "totalStaked": totalStaked,
                "totalStakedInUSD": totalStakedInUSDC / 10 ** 6,
                "totalRewardRate": totalWeeklyRewardRate,
                # "totalWeeklyRewardRate": totalWeeklyRewardRate,
                "allocPoint": allocPoint,
                "apr": getAPR(mcUsdcRatio/10**12, totalSecondRewardRate, totalStakedInUSDC),
                "apr2": 0,
                "chefVersion": "v1",
            }
        )

    #Get alloc point of dummy LP pool in Chef V1
    dummyLPPoolId = 0
    dummyLPToken = "0x00dbf792f23D162Bcf84F9BC979CAc15025D9F8c"
    dummyLpPoolInfo = chef.functions.poolInfo(dummyLPPoolId).call()
    assert dummyLpPoolInfo[0].lower() == dummyLPToken.lower()
    dummyLpAllocPoint = dummyLpPoolInfo[1]


    # get totalSecondRewardRate for dummy LP in Chef V1
    dummyLpTotalSecondRewardRate = (mcPerBlock * dummyLpAllocPoint / (totalAllocPoint * 10 ** decimals))

    #Chef V2 calls
    chefv2 = init_chefv2(w3)
    totalAllocPointV2 = chefv2.functions.totalAllocPoint().call()



    for id, addresses in v2_pools.items():
        print(f"V2 Reached here {id}: {addresses['LP']}")
        tlp = init_tlp(w3, addresses["LP"])
        poolInfo = chefv2.functions.poolInfo(id).call()
        allocPoint = poolInfo[2]

        # Rewarder logic
        rewardsPerBlock = 0
        if addresses["Aurora Rewarder"] != ZERO_ADDRESS:
            rewarder = init_rewarder(w3, addresses["Aurora Rewarder"])
            rewardsPerBlock = rewarder.functions.tokenPerBlock().call()
            rewardDecimals = 18
            print(f"Double rewards per block: {rewardsPerBlock}")
            # if id == 0 or id == 1:
            #     doubleRewardUsdcRatio = auroraUsdcRatio/10**12
            # elif id == 2 or id == 3:
            #     doubleRewardUsdcRatio = lunaUsdcRatio
            # elif id == 8:
            #     doubleRewardUsdcRatio = flxUsdcRatio
            # elif id == 9:
            #     doubleRewardUsdcRatio = mechaUsdcRatio/10**12
            # elif id == 10:
            #     doubleRewardUsdcRatio = solaceUsdcRatio
            # elif id == 11 or id == 12:
            #     rewardDecimals = 24
            #     doubleRewardUsdcRatio = metaUsdcRatio/10**18
            # elif id == 13 or id == 14:
            #     doubleRewardUsdcRatio = chronicleUsdcRatio
            # elif id == 15:
            #     doubleRewardUsdcRatio = gbaUsdcRatio/10**12




        #LP staked amts logic
        reserveInUSDC = getReserveInUsdc(w3, tlp, mcUsdcRatio)
        totalSupply = tlp.functions.totalSupply().call()
        totalStaked = tlp.functions.balanceOf(CHEFV2_ADDRESS).call()
        totalStakedInUSDC = getTotalStakedInUSDC(totalStaked, totalSupply, reserveInUSDC)
        totalSecondRewardRate = (
            dummyLpTotalSecondRewardRate * allocPoint / (totalAllocPointV2)
        )  # Taking MCOIN allocation to dummy LP in chef v1 as mco per block for chef V2
        totalWeeklyRewardRate = (
            3600 * 24 * 7 * totalSecondRewardRate
        )  # TODO: update to return base 10 values
        data.append(
                {
                    "id": len(v1_pools) + id,
                    "poolId": id,
                    "lpAddress": addresses["LP"],
                    "totalSupply": totalSupply,
                    "totalStaked": totalStaked,
                    "totalStakedInUSD": totalStakedInUSDC / 10 ** 6,
                    "totalRewardRate": totalWeeklyRewardRate,
                    "allocPoint": allocPoint,
                    "apr": getAPR(mcUsdcRatio/10**12, totalSecondRewardRate, totalStakedInUSDC),
                    "apr2": getAPR(doubleRewardUsdcRatio, rewardsPerBlock/(10**rewardDecimals), totalStakedInUSDC),
                    "chefVersion": "v2",
                }
        )

    return data


if __name__ == "__main__":
    apr_base()
