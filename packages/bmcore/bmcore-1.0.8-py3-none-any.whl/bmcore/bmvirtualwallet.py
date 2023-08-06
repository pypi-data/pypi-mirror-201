from bmcore.bmenv import *
from pycardano import *
import json
import os


class VirtualWallet:

    def __init__(self, env: BMEnvironment, skey_json, vkey_json) -> None:
        self.skey = PaymentSigningKey.from_json(skey_json)
        self.vkey = PaymentVerificationKey.from_json(vkey_json)
        self.address = Address(self.vkey.hash(), network=env.network)
        self.chain_context = env.chain_context

    def getChangeAddress(self):
        return self.address.to_primitive().hex()

    def getUtxos(self):
        address = str(self.address)
        try:
            return [utxo.to_cbor() for utxo in self.chain_context.utxos(address)]
        except:
            return []

    def signTx(self, tx_cbor):
        tx = Transaction.from_cbor(tx_cbor).transaction_body.hash()
        sig = self.skey.sign(tx)
        set = TransactionWitnessSet(
            vkey_witnesses=[VerificationKeyWitness(self.vkey, sig)]
        ).to_cbor()
        return set

    def submitTx(self, signed_tx):
        self.chain_context.submit_tx(signed_tx)

    @staticmethod
    def init_from_path(env: BMEnvironment, path: str):
        contents = {}
        with open(path, "r") as f:
            contents = json.loads(f.read())
        return VirtualWallet(env, contents["skey"], contents["vkey"])

    @staticmethod
    def create_virtual_wallet() -> None:
        name = input("* Name for the virtual wallet: ")
        key_pair = PaymentKeyPair.generate()
        skey = key_pair.signing_key
        vkey = key_pair.verification_key
        file = f"virtual_wallets/{name}.json"
        if os.path.exists(file):
            raise Exception(
                f"A virtual wallet file with the name '{name}.json' already exists.")
        if not os.path.exists('virtual_wallets/'):
            os.makedirs('virtual_wallets/')
        with open(file, "w") as outfile:
            data = {
                "skey": skey.to_json(),
                "vkey": vkey.to_json()
            }
            outfile.write(json.dumps(data))


if __name__ == "__main__":
    VirtualWallet.create_virtual_wallet()
