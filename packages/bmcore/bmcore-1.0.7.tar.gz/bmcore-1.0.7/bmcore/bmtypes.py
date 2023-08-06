from bmcore.bmenv import *
from pycardano import *
from typing import Union
import builtins


class BMConstants:

    MINTING_SESSION_TTL_MINUTES = 10


class BMProject:

    def __init__(self, json) -> None:
        self.project_id = json["project_id"]
        self.skey = PaymentSigningKey.from_json(json["skey"])
        self.vkey = PaymentVerificationKey.from_json(json["vkey"])
        self.policy = ScriptAll([
            ScriptPubkey(self.vkey.hash()),
            InvalidHereAfter(json["validity_period"])
        ])
        self.policy_id = json["policy_id"]
        assert (self.policy.hash().payload.hex() == json["policy_id"])

    def __hash__(self):
        return builtins.hash(self.project_id)

    @staticmethod
    def create(srenv: BMEnvironment, name, validity_period_years):

        key_pair = PaymentKeyPair.generate()
        skey = key_pair.signing_key
        vkey = key_pair.verification_key
        validity_period_seconds = validity_period_years * \
            (365 + 1) * 24 * 60 * 60
        validity_period = srenv.chain_context.last_block_slot + validity_period_seconds
        policy_id = ScriptAll([
            ScriptPubkey(vkey.hash()),
            InvalidHereAfter(validity_period)
        ]).hash().payload.hex()

        return {
            "network": srenv.network.to_primitive(),
            "project_id": name,
            "skey": skey.to_json(),
            "vkey": vkey.to_json(),
            "validity_period": validity_period,
            "policy_id": policy_id
        }


class BMCIP30ChangeAddress:

    def __init__(self, raw_value) -> None:
        self.value = Address.from_primitive(
            bytes(bytearray.fromhex(raw_value)))
        self.humanReadable = str(self.value)


class BMUTxOSet:

    def __init__(self, raw_value_array) -> None:
        self.value = [UTxO.from_cbor(raw_value)
                      for raw_value in raw_value_array]


class BMHRAddress:

    def __init__(self, raw_value) -> None:
        self.value = Address.from_primitive(raw_value)


class BMAssetPattern:

    """
    NOTE: An asset pattern looks like this:
    asset_pattern = {
        "d5e6bf0500378d4f0da4e8dde6becec7621cd8cbf5cbb9b87013d4cc": {
            "SpaceBud7667": 1,
            "SpaceBud1099": 1
        },
        "b771be5a82843c7f50de45b6cb0860bc3ee1fc1646d1382571020505": {
            "moon": 999_0000
        }
    }
    """

    def __init__(self, raw_value) -> None:
        self.raw_value = raw_value
        self.asset_count = 0
        self.primitive = self._asset_pattern_to_primitive(raw_value)

    def _asset_pattern_to_primitive(self, asset_map):
        map_with_encoded_keys = {}
        for (policy_id, token_map) in asset_map.items():
            encoded_token_map = {}
            for (asset_name, amount) in token_map.items():
                self.asset_count += 1
                encoded_token_map[asset_name.encode('utf-8')] = amount
                map_with_encoded_keys[bytes.fromhex(
                    policy_id)] = encoded_token_map
        return map_with_encoded_keys


class BMHRMultiAsset:

    def __init__(self, lovelace: int, asset_pattern: BMAssetPattern = None) -> None:

        if (type(lovelace) != int):
            raise TypeError(
                f"lovelace should be of type 'int' and not {type(lovelace)}")

        if (asset_pattern is None):
            self.value = Value(lovelace)
        else:
            self.value = Value.from_primitive([
                lovelace,
                asset_pattern.primitive
            ])


class BMPaymentRecipient:

    def __init__(self, address: Union[BMCIP30ChangeAddress, BMHRAddress], invoice: BMHRMultiAsset) -> None:
        self.address = address.value
        self.invoice_value = invoice.value


class BMMintable:

    def __init__(self, project: BMProject, asset_name, metadata, count) -> None:
        self.project = project
        self.asset_name_bytes = str.encode(asset_name, 'utf-8')
        self.asset_name = asset_name
        self.metadata = metadata
        self.count = count

    @staticmethod
    def to_multi_asset(mintables, exclude_burned=False):
        _map = {}
        for mintable in mintables:
            if (exclude_burned and mintable.count <= 0):
                continue
            policy_id_payload = mintable.project.policy.hash().payload
            try:
                _map[policy_id_payload][mintable.asset_name_bytes] = mintable.count
            except:
                _map[policy_id_payload] = {}
                _map[policy_id_payload][mintable.asset_name_bytes] = mintable.count

        if (_map == {}):
            return None

        return MultiAsset.from_primitive(_map)

    @staticmethod
    def to_aux_data(mintables, tag=721):
        _metadata = {
            tag: {}
        }
        for mintable in mintables:
            # TODO: This is not really optimized for single policy projects because
            # you keep on calling .hex() for all the same values. Maybe add a flag here.
            if (mintable.count <= 0):
                continue
            policy_id_hash = mintable.project.policy_id
            try:
                _metadata[tag][policy_id_hash][mintable.asset_name] = mintable.metadata
            except:
                _metadata[tag][policy_id_hash] = {}
                _metadata[tag][policy_id_hash][mintable.asset_name] = mintable.metadata

        if (_metadata[tag] == {}):
            return None

        return AuxiliaryData(
            AlonzoMetadata(metadata=Metadata(_metadata))
        )


class BMMintingRecipient:

    def __init__(self, address: Union[BMCIP30ChangeAddress, BMHRAddress], mintables) -> None:
        self.address = address.value
        self.mintables = mintables
