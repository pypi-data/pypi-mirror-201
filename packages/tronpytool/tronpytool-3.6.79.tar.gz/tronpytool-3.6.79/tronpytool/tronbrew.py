from . import Paths

from .compile.basetest import CoreDeploy, WrapContract, SolcWrap, message_exit
from .payment import PrintNetworkName


# https://chatanalytics.app/demo

class TronBrew(CoreDeploy):

    def __init__(self, root_path: str, factory_path: str, network: str = "mainnet"):
        self.ROOT = root_path
        self.FACTORY = factory_path
        _workSpace = WrapContract(network).setDefaultKeys()
        _tron = _workSpace.getClientTron()
        PrintNetworkName(_tron)
        self.master_wallet = _tron.default_address
        self.wrapper = _workSpace
        super().__init__(_tron)
        self.connecting()

    def connecting(self, history: any = False):
        self.is_deploy = False
        self.sol_wrap = SolcWrap(self.ROOT)
        self.pathfinder = Paths(self.ROOT)
        if history is False:
            self.pathfinder.setDefaultPath()
        else:
            self.pathfinder.SetUseHistory(history)
        self.pathfinder.Network(self.tron.network_name)
        if self.FACTORY == "" or self.FACTORY == "{}":
            message_exit("Factory folder is not pointed / not valid. Please check for details")

        self.pathfinder.setFactory(self.FACTORY)
        self.ready_io(True)
