"""Helpers for unit conversions.
"""


def wei_to_eth(wei: int) -> float:
    """Convert wei to ether.
    """
    return int(wei) / 1e18


def wei_to_gwei(wei: int) -> float:
    """Convert wei to gwei.
    """
    return int(wei) / 1e9
