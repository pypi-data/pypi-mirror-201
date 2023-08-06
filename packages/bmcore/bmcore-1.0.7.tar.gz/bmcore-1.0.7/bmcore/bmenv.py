import os
from dotenv import load_dotenv
from pycardano import *


class BMEnvironment():

    def _warn(self, msg):
        print(f"\033[33m{msg}\033[0m")

    def __init__(self, path=".env", network=None) -> None:
        load_dotenv(path)

        if (network is not None):
            self._warn(
                f"NETWORK override detected, setting NETWORK to {network}")
            self.network = Network.from_primitive(network)
        else:
            self._warn(f"Loading NETWORK VAR from .env")
            self.network = Network.MAINNET if int(
                os.getenv("NETWORK")) == 1 else Network.TESTNET

        if (self.network is Network.MAINNET):
            self.chain_context = BlockFrostChainContext(
                project_id=os.getenv("BLOCKFROST_MAINNET_API_KEY"),
                network=self.network,
                base_url=os.getenv("BLOCKFROST_MAINNET_BASE_URL")
            )
        else:
            self.chain_context = BlockFrostChainContext(
                project_id=os.getenv("BLOCKFROST_TESTNET_API_KEY"),
                network=self.network,
                base_url=os.getenv("BLOCKFROST_TESTNET_BASE_URL")
            )

        self.db_connection_string = os.getenv("DB_CONNECTION_STRING")

        self._warn("Env loaded!")
