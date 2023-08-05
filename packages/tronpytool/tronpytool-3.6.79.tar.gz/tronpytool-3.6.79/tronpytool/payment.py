#!/usr/bin/env python
# --------------------------------------------------------------------
# Copyright (c) fInvention.c. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------
from dataclasses import dataclass

from tronpytool.common.trc20 import TokenLv

from .compile.basetest import CoreDeploy, WrapContract

from .constants import Bolors


@dataclass
class Key:
    private_key: str
    wallet_address: str
    token: str
    precision: int
    network: str


def PrintNetworkName(tron):
    print(f"You are now using network {Bolors.WARNING}{str(tron.network_name).upper()}{Bolors.RESET}")


class Payment(CoreDeploy):
    """Deploy wrap contract in the deployment"""

    def __init__(self, key_set: Key):
        _workSpace = WrapContract(key_set.network).setMasterKey(key_set.wallet_address, key_set.private_key)
        _tron = _workSpace.getClientTron()
        PrintNetworkName(_tron)
        self.master_wallet = key_set.wallet_address
        self.wrapper = _workSpace
        super().__init__(_tron)
        self.usdt = TokenLv(_tron, self.token_usd_address)
        self.usdt.CallDebug(False).CallContractFee(self.limit_fees)
        self.approved = 0
        self.onedollar = 10 ** self.precision

    @property
    def token_usd_address(self) -> str:
        return "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

    @property
    def precision(self) -> int:
        return 6

    @property
    def limit_fees(self) -> int:
        return 20000000

    def scan_for_usdt_approval_zero(self, receiver_contract: str, user: str) -> bool:
        self.approved = self.usdt.allowance(receiver_contract, user)
        return self.approved > 0

    def scan_for_usdt_approval(self, receiver_contract: str, user: str) -> bool:
        self.approved = self.usdt.allowance(receiver_contract, user)
        return self.approved > self.onedollar

    def move_fund(self, user: str):
        """
        pleaes make override from this operation
        """
        pass

    def transferUsdt(self, amount: int, to_user: str) -> bool:
        """
        this is the await operation
        """
        return self.usdt.transfer(to_user, amount)
