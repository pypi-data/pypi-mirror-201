class KilnError(Exception):
    """Base class for Kiln errors.
    """


class KilnInvalidEnvError(KilnError):
    """Invalid environment config.
    """


class KilnIntegrationConfigError(KilnError):
    """Invalid integration config.
    """


class KilnFireblocksFailedToSignError(KilnError):
    """Failed to sign the fireblocks transaction.
    """


class KilnFireblocksNonExistingDestinationIdError(KilnError):
    """Fireblocks destination does not exist.
    """


class KilnFireblocksNonExistingWalletIdError(KilnError):
    """Fireblocks wallet does not exist.
    """


class KilnFireblocksNonExistingDepositAddressError(KilnError):
    """Fireblocks account has no deposit address for this asset.
    """


class KilnFireblocksNoForSmartContractAPIForAssetError(KilnError):
    """This asset does not support the smart-contract API call.
    """


class KilnInternalServerError(KilnError):
    """Kiln API returned a 500
    """
