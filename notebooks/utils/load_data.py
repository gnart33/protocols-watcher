import pandas as pd
import ctc
import os
import requests
import time
from dotenv import load_dotenv
load_dotenv()
from_block = 15767026
ETHERSCAN_TOKEN = os.getenv('ETHERSCAN_TOKEN')

def get_current_block():
    current_timestamp = int(time.time())
    print(ETHERSCAN_TOKEN)
    _url = f"""https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={current_timestamp}&closest=before&apikey={ETHERSCAN_TOKEN}"""
    request = requests.post(_url)
    return int(request.json()['result'])

def load_psdn_ocean_transfers():
    """Load the PSDN Ocean data from a CSV file"""
    psdn_ocean_data_file = 'data/export-token-0x51fa2efd62ee56a493f24ae963eace7d0051929e-psdnocean.csv'
    psdn_ocean_transfers = pd.read_csv(psdn_ocean_data_file)
    # types casting
    psdn_ocean_transfers['DateTime'] = pd.to_datetime(psdn_ocean_transfers['DateTime'])
    psdn_ocean_transfers["Quantity"] = [float(str(i).replace(",", "")) for i in psdn_ocean_transfers["Quantity"]]
    return psdn_ocean_transfers

def load_lp_staking():
    # load data lp staking contract
    lp_staking_contract_data_file = 'data/export-address-token-0x08D3f2cAe4eaCDCbFb0f7FfaD07a6d00FC36Db6E-erc-transfer.csv'
    lp_staking_contract_data = pd.read_csv(lp_staking_contract_data_file)

    # types casting
    lp_staking_contract_data['DateTime'] = pd.to_datetime(lp_staking_contract_data['DateTime'])
    lp_staking_contract_data["TokenValue"] = [float(str(i).replace(",", "")) for i in lp_staking_contract_data["TokenValue"]]
    return lp_staking_contract_data


def load_psdn_ocean_staking():
    # load data psdnOcean staking contract
    psdn_ocean_staking_contract_data_file = 'data/export-address-token-0xEb1CEFa6F175B4c889582DFEea4ee155CCD5D2A5-psdnocean-stake.csv'
    psdn__ocean_staking_contract_data = pd.read_csv(psdn_ocean_staking_contract_data_file)

    # types casting
    psdn__ocean_staking_contract_data['DateTime'] = pd.to_datetime(psdn__ocean_staking_contract_data['DateTime'])
    psdn__ocean_staking_contract_data["TokenValue"] = [float(str(i).replace(",", "")) for i in psdn__ocean_staking_contract_data["TokenValue"]]
    return psdn__ocean_staking_contract_data


def load_psdn_transfers():
    psdn_transfers_file = 'data/export-token-0xa5b947687163fe88c3e6af5b17ae69896f4abccf-psdn-transfers.csv'
    psdn_transfers = pd.read_csv(psdn_transfers_file)

    psdn_transfers['DateTime'] = pd.to_datetime(psdn_transfers['DateTime'])
    psdn_transfers["Quantity"] = [float(str(i).replace(",", "")) for i in psdn_transfers["Quantity"]]
    return psdn_transfers


def logs_table_from_etherscan(contract_address):
    """Logs table of a contract, pulled form etherscan.io"""
    to_block = get_current_block()
    _url = f"""https://api.etherscan.io/api?module=logs&action=getLogs&address={contract_address}&fromBlock={from_block}&toBlock={to_block}&page=1&offset=1000&apikey={ETHERSCAN_TOKEN}"""
    request = requests.post(_url)
    data = request.json()['result']
    df = pd.DataFrame.from_records(data)
    df['blockNumber'] = df[ 'blockNumber'].apply(int, base=16)
    df['timeStamp'] = df[ 'timeStamp'].apply(int, base=16)
    # 
    df['DateTime'] = pd.to_datetime(df['timeStamp'], unit='s')
    return df


