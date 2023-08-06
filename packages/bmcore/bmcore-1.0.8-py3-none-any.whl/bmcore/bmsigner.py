from bmcore.bmenv import *
from bmcore.bmtypes import *
from pycardano import *
from typing import List, Set, Union

# get_tx_cbor_and_aux_data


class BMSigner:

    def __init__(self, environment: BMEnvironment, tx_cbor: str, aux_data_cbor: str) -> None:
        self.environment = environment
        self.tx: Transaction = Transaction.from_cbor(tx_cbor)

        if (aux_data_cbor):
            self.aux_data = AuxiliaryData.from_cbor(aux_data_cbor)
        else:
            self.aux_data = None

        self.witnesses = []
        self.policies = []
        self.projects: Set[BMProject] = set()
        pass

    def add_witness_cbor(self, witness_cbor):
        self.witnesses.extend(TransactionWitnessSet.from_cbor(
            witness_cbor).vkey_witnesses)
        return self

    def add_project(self, project: BMProject):
        self.projects.add(project)
        return self

    def get_multi_signed_tx_cbor(self):
        witness_set = TransactionWitnessSet(vkey_witnesses=[])
        witness_set.vkey_witnesses.extend(self.witnesses)
        witness_set.vkey_witnesses.extend(self._get_witnesses_from_projects())
        witness_set.native_scripts = [
            project.policy for project in self.projects]
        self.tx.transaction_witness_set = witness_set
        if (self.aux_data):
            self.tx.auxiliary_data = self.aux_data
        return self.tx.to_cbor()

    def _get_witnesses_from_projects(self):
        project_witnesses = []
        for project in self.projects:
            skey = project.skey
            vkey = project.vkey
            sig = skey.sign(self.tx.transaction_body.hash())
            project_witnesses.append(VerificationKeyWitness(vkey, sig))
        return project_witnesses
