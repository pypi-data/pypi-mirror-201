from eulith_web3.erc20 import TokenSymbol, EulithERC20
from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.gmx import GMXClient
from eulith_web3.signing import construct_signing_middleware
from eulith_web3.kms import KmsSigner
from eulith_web3.contract_bindings.pendle.i_p_action_add_remove_liq import IPActionAddRemoveLiq, ApproxParams, TokenInput
import boto3

PENDLE_ROUTER = '0x0000000001e4ef00d069e71d6ba041b0a16f7ea0'
GLP_MARKET = '0x7D49E5Adc0EAAD9C027857767638613253eF125f'

if __name__ == '__main__':
    aws_credentials_profile_name = 'default'
    key_name = 'LUCAS_TEST_KEY'
    formatted_key_name = f'alias/{key_name}'

    session = boto3.Session(profile_name=aws_credentials_profile_name)
    client = session.client('kms')

    wallet = KmsSigner(client, formatted_key_name)

    print(wallet.address)

    ew3 = EulithWeb3(eulith_url="https://arb-main.eulithrpc.com/v0",
                     eulith_refresh_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJzdWIiOiJsdWNhcyIsImV4cCI6MTcxMjM0OTY2MSwic291cmNlX2hhc2giOiIqIiwic2NvcGUiOiJBUElSZWZyZXNoIn0.QAyFERJw-Z0P0JKsbWBsIVtXHh1om2FfINlcUq-eKEIdAXPzty4B4U30Cjz4ETnYN0kqH1SWFWzCTqTZ6wH5Kxs",
                     signing_middle_ware=construct_signing_middleware(wallet))

    wallet_checksum = ew3.to_checksum_address(wallet.address)

    weth = ew3.v0.get_erc_token(TokenSymbol.WETH)
    usdc = ew3.v0.get_erc_token(TokenSymbol.USDC)
    glp = ew3.v0.get_erc_token(TokenSymbol.GLP)

