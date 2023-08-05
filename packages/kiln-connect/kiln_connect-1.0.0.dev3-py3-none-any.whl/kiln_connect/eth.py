"""Ethereum wrapper class.

This ETH class is meant to be accessed via KilnConnect.eth, it is
publicly exported in the SDK. This file contains helpers to
integration our Ethereum API with integrations such as Fireblocks. It
provides convenient shortcuts to use our SDK.
"""
import logging

from .errors import (
    KilnInternalServerError,
    KilnFireblocksNonExistingWalletIdError,
)
from kiln_connect.integrations import Integrations, Asset

from kiln_connect.openapi_client import (
    ApiClient,
)
from kiln_connect.openapi_client import (
    EthApi,
    ETHCraftStakeTxPayload,
    ETHPrepareTxPayload,
    ETHBroadcastTxPayload,
    ETHBroadcastedTx,
)
from kiln_connect.openapi_client.exceptions import ServiceException


class ETH(EthApi):
    """Wrapper for the Ethereum API.
    """

    def __init__(self, api: ApiClient, integrations: Integrations):
        super().__init__(api)
        self.integrations = integrations

    def stake_smart_contract(self, integration: str, account_id: str, destination_id: str, amount_wei: int) -> dict:
        """Helper to stake on Ethereum using smart-contract signing.
        """
        fb = self.integrations.get_integration(integration)

        # Fetch fireblocks wallet for ETH.
        wallet = fb.get_deposit_address(Asset.eth, fb.src.id)
        if not wallet:
            raise KilnFireblocksNonExistingWalletIdError()

        # Craft TX.
        craft_tx = ETHCraftStakeTxPayload(
            account_id=account_id,
            wallet=wallet,
            amount_wei=str(amount_wei),
        )

        logging.debug(
            "Crafting TX - account_id={0}, wallet={1}, amount_wei={2}".format(
                craft_tx.account_id, craft_tx.wallet, craft_tx.amount_wei))

        response = super().post_eth_stake_tx(craft_tx)
        logging.debug("TX Crafted")

        # Sign & broadcast TX.
        tx = fb.sign_broadcast(
            Asset.eth, response.data.contract_call_data, destination_id, response.data.__dict__)

        return tx

    def stake_raw(self, integration: str, account_id: str, wallet: str, amount_wei: int) -> ETHBroadcastedTx:
        """Helper to stake on Ethereum using Fireblocks and raw signing.
        """
        fb = self.integrations.get_integration(integration)

        # Craft TX.
        craft_tx = ETHCraftStakeTxPayload(
            account_id=account_id,
            wallet=wallet,
            amount_wei=str(amount_wei),
        )

        logging.debug(
            "Crafting TX - account_id={0}, wallet={1}, amount_wei={2}".format(
                craft_tx.account_id, craft_tx.wallet, craft_tx.amount_wei))

        response = super().post_eth_stake_tx(craft_tx)
        logging.debug("TX Crafted")

        unsigned_tx_payload = response.data.unsigned_tx_serialized
        unsigned_tx_hash = response.data.unsigned_tx_hash

        # Sign TX.
        sig = fb.raw_sign(Asset.eth, unsigned_tx_hash)

        # Prepare TX.
        prepare_tx = ETHPrepareTxPayload(
            unsigned_tx_serialized=unsigned_tx_payload,
            r=sig.get("r"),
            s=sig.get("s"),
            v=sig.get("v", 0)
        )

        logging.debug(
            "Preparing TX - unsigned_tx_serialized={0}, r={1}, s={2}, v={3}".format(
                prepare_tx.unsigned_tx_serialized, prepare_tx.r, prepare_tx.s, prepare_tx.v))

        response = super().post_eth_prepare_tx(prepare_tx)
        logging.debug("TX Prepared")

        # Broadcast TX.
        broadcast_tx = ETHBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized,
        )

        logging.debug(
            f"Broadcasting TX - tx_serialized={broadcast_tx.tx_serialized}")

        try:
            response = super().post_eth_broadcast_tx(broadcast_tx)
        except ServiceException:
            # Currently our OpenAPI specs does not expose schemas for error code responses so impossible
            # to provide better info
            logging.debug(r"/!\ Kiln API Internal Error /!\\")
            raise KilnInternalServerError()
        # Likely need to check response here and throw appropriate errors.

        return response.data
