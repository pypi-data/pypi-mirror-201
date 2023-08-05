"""Solana wrapper class.

This SOL class is meant to be accessed via KilnConnect.sol, it is
publicly exported in the SDK. This file contains helpers to
integration our Solana API with integrations such as Fireblocks. It
provides convenient shortcuts to use our SDK.
"""

from kiln_connect.integrations import Integrations

from kiln_connect.openapi_client import (
    ApiClient,
)
from kiln_connect.openapi_client import (
    SolApi,
)


class SOL(SolApi):
    """Wrapper for the Solana API.
    """

    def __init__(self, api: ApiClient, integrations: Integrations):
        super().__init__(api)
        self.integrations = integrations
