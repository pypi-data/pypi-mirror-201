"""Tezos wrapper class.

This XTZ class is meant to accessed via KilnConnect.xtz. It
contains helpers around tezos management.
"""
import logging

from .errors import KilnInternalServerError
from kiln_connect.integrations import (
    Integrations,
    Asset
)
from kiln_connect.openapi_client import (
    ApiClient,
)
from kiln_connect.openapi_client import (
    XtzApi,
    XTZCraftStakeTxPayload,
    XTZCraftUnStakeTxPayload,
    XTZPrepareTxPayload,
    XTZBroadcastTxPayload,
    XTZBroadcastedTx
)
from kiln_connect.openapi_client.exceptions import ServiceException


class XTZ(XtzApi):
    """Wrapper for the Tezos API.
    """

    def __init__(self, api: ApiClient, integrations: Integrations):
        super().__init__(api)
        self.integrations = integrations

    def stake(self, integration: str, account_id: str, wallet: str, baker: str) -> XTZBroadcastedTx:
        """Helper to stake on Tezos using Fireblocks
        """
        fb = self.integrations.get_integration(integration)

        # Craft TX.
        craft_tx = XTZCraftStakeTxPayload(
            account_id=account_id,
            wallet=wallet,
            baker_address=baker
        )

        logging.debug(
            "Crafting TX - account_id={0}, wallet={1}, baker_address={2}".format(
                craft_tx.account_id, craft_tx.wallet, craft_tx.baker_address))

        response = super().post_xtz_stake_tx(craft_tx)
        logging.debug("TX Crafted")

        unsigned_tx_payload = response.data.unsigned_tx_serialized
        unsigned_tx_hash = response.data.unsigned_tx_hash

        # Sign TX.
        sig = fb.raw_sign(Asset.xtz, unsigned_tx_hash)

        # Prepare TX.
        prepare_tx = XTZPrepareTxPayload(
            unsigned_tx_serialized=unsigned_tx_payload,
            signature=sig['fullSig']
        )

        logging.debug(
            "Preparing TX - unsigned_tx_serialized={0}, signature={1}".format(
                prepare_tx.unsigned_tx_serialized, prepare_tx.signature))

        response = super().post_xtz_prepare_tx(prepare_tx)
        logging.debug("TX Prepared")

        # Broadcast TX.
        broadcast_tx = XTZBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized,
        )
        logging.debug(
            f"Broadcasting TX - tx_serialized={broadcast_tx.tx_serialized}")
        try:
            response = super().post_xtz_broadcast_tx(broadcast_tx)
        except ServiceException:
            logging.debug(r"/!\ Kiln API Internal Error /!\\")
            logging.debug(response.data)
            raise KilnInternalServerError()

        logging.debug("TX Broadcast")
        # Likely need to check response here and throw appropriate errors.
        return response.data

    def unstake(self, integration: str, account_id: str, wallet: str) -> XTZBroadcastedTx:
        """Helper to stake on Tezos using Fireblocks
        """
        fb = self.integrations.get_integration(integration)

        # Craft TX.
        craft_tx = XTZCraftUnStakeTxPayload(
            wallet=wallet,
        )
        logging.debug(f"Crafting TX - wallet={craft_tx.wallet}")
        response = super().post_xtz_un_stake_tx(craft_tx)
        logging.debug("TX Crafted")
        unsigned_tx_payload = response.data.unsigned_tx_serialized
        unsigned_tx_hash = response.data.unsigned_tx_hash

        # Sign TX.
        sig = fb.sign(Asset.xtz, unsigned_tx_hash)

        # Prepare TX.
        prepare_tx = XTZPrepareTxPayload(
            unsigned_tx_serialized=unsigned_tx_payload,
            signature=sig['fullSig']
        )
        logging.debug("Preparing TX",
                      prepare_tx.unsigned_tx_serialized, prepare_tx.signature)
        response = super().post_xtz_prepare_tx(prepare_tx)
        logging.debug("TX Prepared")
        # Broadcast TX.
        broadcast_tx = XTZBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized,
        )

        logging.debug(f"Broadcasting TX - {broadcast_tx.tx_serialized}")
        try:
            response = super().post_xtz_broadcast_tx(broadcast_tx)
        except ServiceException:
            # Currently our OpenAPI specs does not expose schemas for error code responses so impossible
            # to provide better info
            logging.debug(r"/!\ Kiln API Internal Error /!\\")
            raise KilnInternalServerError()

        logging.debug("TX Broadcast")
        return response.data
