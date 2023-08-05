"""Wrapper a bit similar to the Typescript SDK with signing integrations.
"""

import time
from dataclasses import dataclass
from enum import Enum

import fireblocks_sdk

from .errors import (
    KilnFireblocksFailedToSignError,
    KilnFireblocksNoForSmartContractAPIForAssetError,
    KilnFireblocksNonExistingDepositAddressError,
    KilnError  # noqa: F401
)
from .utils import (
    wei_to_gwei,
    wei_to_eth,
)


@dataclass
class IntegrationConfig:
    """Configuration of a Kiln integration.
    """
    name: str
    provider: str
    parameters: dict


class Asset(str, Enum):
    eth = "eth"
    xtz = "xtz"


class FireblocksIntegration:
    """Handles the Fireblocks integration.
    """

    def __init__(self, config: IntegrationConfig):
        self.fireblocks = None

        self.src = fireblocks_sdk.TransferPeerPath(
            "VAULT_ACCOUNT", config.parameters['vault_account_id'])
        self.assets = config.parameters['assets']

        with open(config.parameters['raw_key_path'], 'r') as pk:
            d = pk.read()
            self.fb = fireblocks_sdk.FireblocksSDK(
                d, config.parameters['api_token'])

    def get_destination_address(self, asset: Asset, destination_id: str) -> str:
        """Returns the destination address for a given asset.
        """
        return self.fb.get_contract_wallet_asset(destination_id, self.assets[asset]).get('address')

    def get_deposit_address(self, asset: Asset, wallet_id: str) -> str:
        """Returns the wallet address for a given asset.
        """
        addresses = self.fb.get_deposit_addresses(
            wallet_id, self.assets[asset])
        if not addresses:
            raise KilnFireblocksNonExistingDepositAddressError()

        return addresses[0].get('address')

    def sign_broadcast(self, asset: Asset, calldata: str, destination_id: str, params: dict) -> str:
        """Asks fireblocks to sign and broadcast a transaction via the smart-contract API.
        """
        if asset not in [Asset.eth]:
            raise KilnFireblocksNoForSmartContractAPIForAssetError()

        dst = {'type': fireblocks_sdk.EXTERNAL_WALLET, 'id': destination_id}
        asset = self.assets[asset]
        note = "Staked from Kiln SDK Python"
        fireblocks_sdk.RawMessage(
            [fireblocks_sdk.UnsignedMessage(calldata)])
        gas_limit = params.get('gas_limit')
        priority_fee = str(wei_to_gwei(
            params.get('max_priority_fee_per_gas_wei')))
        max_fee = str(wei_to_gwei(params.get('max_fee_per_gas_wei')))
        dst = fireblocks_sdk.DestinationTransferPeerPath(
            fireblocks_sdk.EXTERNAL_WALLET, destination_id)

        tx = self.fb.create_transaction(
            asset_id=asset,
            amount=str(wei_to_eth(params.get('amount_wei'))),
            source=self.src,
            destination=dst,
            tx_type=fireblocks_sdk.CONTRACT_CALL,
            note=note,
            extra_parameters={'contractCallData': calldata},
            gas_limit=gas_limit,
            priority_fee=priority_fee,
            max_fee=max_fee,
        )

        return self.wait_for_completion(tx.get('id'))

    def raw_sign(self, asset: Asset, unsigned_tx_hash: str) -> dict:
        """Asks fireblocks to raw sign TX hash and wait for completion.
        """
        msg = fireblocks_sdk.RawMessage(
            [fireblocks_sdk.UnsignedMessage(unsigned_tx_hash)])
        asset = self.assets[asset]
        note = "Staked from Kiln SDK Python"

        sign_tx = self.fb.create_raw_transaction(msg, self.src, asset, note)
        tx_id = sign_tx.get("id")


        signed_tx = self.wait_for_completion(tx_id)

        signatures = signed_tx.get("signedMessages")
        if not signatures or len(signatures) != 1:
            raise KilnFireblocksFailedToSignError()

        return signatures[0].get('signature')

    def wait_for_completion(self, tx_id: str) -> dict:
        """Waits for a transaction to complete.
        """
        failed_states = [
            fireblocks_sdk.TRANSACTION_STATUS_BLOCKED,
            fireblocks_sdk.TRANSACTION_STATUS_FAILED,
            fireblocks_sdk.TRANSACTION_STATUS_REJECTED,
            fireblocks_sdk.TRANSACTION_STATUS_CANCELLED
        ]

        signed_tx = None
        while True:
            signed_tx = self.fb.get_transaction_by_id(tx_id)
            status = signed_tx.get('status')
            if status == fireblocks_sdk.TRANSACTION_STATUS_COMPLETED:
                break
            if status in failed_states:
                break
            time.sleep(1)

        return signed_tx


class Integrations:
    """Handles integrations.

    For now it's kind of ad-hoc and we don't have a lot of
    integrations so we can keep it simple, once we start having a lot
    we can split each integration accordingly without changing this
    interface.
    """

    def __init__(self, configs: list[IntegrationConfig]):
        self.integrations = dict()

        for config in configs:
            if config.provider == "fireblocks":
                i = FireblocksIntegration(config)
                self.integrations[config.name] = i

    def get_integration(self, name: str):
        """Returns the configured integration
        """
        return self.integrations[name]
