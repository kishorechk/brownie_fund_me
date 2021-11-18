from brownie import network, accounts, exceptions
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrane_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrane_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrane_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    bad_actor = accounts.add()
    fund_me = deploy_fund_me()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
