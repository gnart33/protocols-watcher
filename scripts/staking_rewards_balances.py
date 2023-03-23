from brownie import interface
import pandas as pd

staking_reward_contract_address = "0x2Ae08F2cBB9A9e2d4609c487Ecb1B6308718D5e8"


def main():
    stakers = get_stakers()
    print(f"Total stakers: {len(stakers)}")
    stakers_balance = []
    for staker in stakers:
        print(staker)
        stakers_balance.append(query_staking_rewards_balances(staker)/1e18)
    df = pd.DataFrame(
    {'staker': stakers,
     'balance': stakers_balance
    })
    df.to_csv("staking_rewards_balances.csv")


def query_staking_rewards_balances(address):
    staking_rewards_contract = interface.IStakingRewards(staking_reward_contract_address)
    return staking_rewards_contract.balanceOf(address)

def get_stakers():
    csv_file = "/Users/nvtrang/code/h2o/protocol-liquidity/data/export-address-token-0x2ae08f2cbb9a9e2d4609c487ecb1b6308718d5e8.csv"
    staker_tnx = pd.read_csv(csv_file, index_col=0)
    stakers = staker_tnx.loc[(staker_tnx["TokenSymbol"] == "xPSDN-ETH1") & (staker_tnx["To"] == "0x2ae08f2cbb9a9e2d4609c487ecb1b6308718d5e8")]
    stakers_list = list(stakers["From"].unique())
    return stakers_list

