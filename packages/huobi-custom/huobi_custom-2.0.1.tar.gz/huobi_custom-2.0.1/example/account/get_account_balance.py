from huobi.client.account import AccountClient
from huobi.constant import *
from huobi.utils import LogInfo



api_key ='88fbec25-de8461a1-ntmuw4rrsr-bb051'
api_secret ='bde897ae-beb99d2d-cfa29656-1a0a6'



account_client = AccountClient(api_key=api_key,
                               secret_key=api_secret)
LogInfo.output("====== (SDK encapsulated api) not recommend for low performance and frequence limitation ======")
account_balance_list = account_client.get_account_balance()
if account_balance_list and len(account_balance_list):
    for account_obj in account_balance_list:
        account_obj.print_object()
        print()