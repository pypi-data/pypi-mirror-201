from bmcore.bmenv import *
from bmcore.bmtypes import *
from pycardano import *
from typing import List, Set


class BMMint:

    def __init__(self, environment: BMEnvironment) -> None:
        self.env = environment
        self.tx_builder = TransactionBuilder(self.env.chain_context)
        self.change_address = None
        self.mintables: List[BMMintable] = []
        self.payment_recipients: List[BMPaymentRecipient] = []
        self.minting_recipients: List[BMMintingRecipient] = []
        self.verify: BMAssetPattern = None
        self.projects: Set[BMProject] = set()
        self.utxos = None

        self.EXPERIMENTAL_mint = None
        self.EXPERIMENTAL_aux_data = None

    def log(self, message):
        print(message)
        return self

    # public:
    def set_change_address(self, change_address: BMCIP30ChangeAddress):
        self.change_address = change_address.value
        return self

    def set_utxos(self, utxos: BMUTxOSet):
        self.utxos = utxos.value
        return self

    def add_payment_recipient(self, payment_recipient: BMPaymentRecipient):
        self.payment_recipients.append(payment_recipient)
        return self

    def add_minting_recipient(self, minting_recipient: BMMintingRecipient):
        self.minting_recipients.append(minting_recipient)
        for mintable in minting_recipient.mintables:
            self.projects.add(mintable.project)
            self.mintables.append(mintable)
        return self

    def verify_on_mint(self, asset_pattern: BMAssetPattern):
        self.verify = asset_pattern
        return self

    def EXPERIMENTAL_override_mint(self, mint):
        self.EXPERIMENTAL_mint = mint
        return self

    def EXPERIMENTAL_override_aux_data(self, aux_data):
        self.EXPERIMENTAL_aux_data = aux_data
        return self

    def get_tx_cbor_and_aux_data(self):
        ttl_seconds = BMConstants.MINTING_SESSION_TTL_MINUTES * 60
        self.tx_builder.ttl = InvalidHereAfter(
            self.env.chain_context.last_block_slot + ttl_seconds
        ).after

        if (self.EXPERIMENTAL_mint):
            self.tx_builder.mint = self.EXPERIMENTAL_mint
        else:
            self.tx_builder.mint = BMMintable.to_multi_asset(self.mintables)

        if (self.EXPERIMENTAL_aux_data):
            self.tx_builder.auxiliary_data = self.EXPERIMENTAL_aux_data
        else:
            self.tx_builder.auxiliary_data = BMMintable.to_aux_data(
                self.mintables)

        # TODO: How should we approach this in the case of multiple policy ids, infer from mintables?
        self.tx_builder.native_scripts = [
            project.policy for project in self.projects]

        for utxo in self.utxos:
            self.tx_builder.add_input(utxo)

        self._set_payment_recipients()
        self._set_minting_recipients()
        self._verify_tokens_if_needed()

        tx_body = self.tx_builder.build(change_address=self.change_address)
        tx = Transaction(tx_body, self._create_dummy_witness_set())
        tx_cbor_string = str(tx.to_cbor())
        if (self.tx_builder.auxiliary_data):
            aux_data_cbor_string = self.tx_builder.auxiliary_data.to_cbor()
        else:
            aux_data_cbor_string = None
        return (tx_cbor_string, aux_data_cbor_string)

    # private

    def _create_dummy_witness_set(self):
        dummy_witness = '8258208814c250f40bfc74d6c64f02fc75a54e68a9a8b3736e408d9820a6093d5e38b95840f04a036fa56b180af6537b2bba79cec75191dc47419e1fd8a4a892e7d84b7195348b3989c15f1e7b895c5ccee65a1931615b4bdb8bbbd01e6170db7a6831310c'
        witness_set = TransactionWitnessSet(
            vkey_witnesses=[
                VerificationKeyWitness.from_cbor(dummy_witness),
                VerificationKeyWitness.from_cbor(dummy_witness),
                VerificationKeyWitness.from_cbor(dummy_witness),
            ]
        )
        return witness_set

    def _set_payment_recipients(self):
        for payment_recipient in self.payment_recipients:
            output = TransactionOutput(
                payment_recipient.address, payment_recipient.invoice_value
            )
            self.tx_builder.add_output(output)

    def _set_minting_recipients(self):
        for minting_recipient in self.minting_recipients:
            mint = BMMintable.to_multi_asset(
                minting_recipient.mintables, exclude_burned=True
            )
            if (not mint):
                continue

            min_lovelace_required = min_lovelace(
                context=self.env.chain_context,
                output=TransactionOutput(
                    minting_recipient.address,
                    Value(0, mint)
                )
            ) + 100_000

            output = TransactionOutput(
                minting_recipient.address,
                Value(min_lovelace_required, mint)
            )

            self.tx_builder.add_output(output)

    def _verify_tokens_if_needed(self):
        if (self.verify is None):
            return
        min_lovelace_required = min_lovelace(
            context=self.env.chain_context,
            output=TransactionOutput(
                self.change_address,
                Value.from_primitive([0, self.verify.primitive])
            )
        ) + 100_000

        verified_tokens_output = TransactionOutput(
            self.change_address,
            Value.from_primitive(
                [min_lovelace_required, self.verify.primitive])
        )

        self.tx_builder.add_output(verified_tokens_output)
