from enum import Enum
from os import environ
import logging

from cachetools import cached, TTLCache
import requests

from .constants import CHAIN_IDS, DATASET_IDS, QUERY_PAYLOAD


class ScanCountType(Enum):
    CONTRACT_CREATION_COUNT = 1
    CONTRACT_INTERACTION_COUNT = 2
    CUSTOM_SCAN_COUNT = 3
    ERC_APPROVAL_ALL_COUNT = 4
    ERC_APPROVAL_COUNT = 5
    ERC_TRANSFER_COUNT = 6
    LARGE_VALUE_TRANSFER_COUNT = 7
    TRANSFER_COUNT = 8
    TX_COUNT = 9
    TX_WITH_INPUT_DATA_COUNT = 10


@cached(cache=TTLCache(maxsize=100, ttl=300))
def get_alert_count(bot_id: str, alert_id: str, chain_id: int) -> int:
    """Gets alert count in the last 24 hours via Forta's Alert Stats API"""
    alert_stats_url = (
        f"https://api.forta.network/stats/bot/{bot_id}/alerts?chainId={chain_id}"
    )
    alert_id_counts = 1
    try:
        result = requests.get(alert_stats_url).json()
        if alert_id in result["alertIds"]:
            alert_id_counts = int(result["alertIds"][alert_id]["count"])
    except Exception as err:
        logging.warning(f"Error obtaining alert counts: {err}")

    return alert_id_counts


@cached(cache=TTLCache(maxsize=100, ttl=60))
def get_scan_counts(chain_id: int):
    """Gets all scan counts for given chain via Zettablock."""
    dataset_id = DATASET_IDS[chain_id]
    if not dataset_id.startswith("sq"):
        raise NotImplementedError(dataset_id)
    scan_counts_url = f"https://api.zettablock.com/api/v1/dataset/{dataset_id}/graphql"
    payload = QUERY_PAYLOAD
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": environ["ZETTABLOCK_API_KEY"],
    }
    scan_counts = {}
    try:
        result = requests.post(scan_counts_url, json=payload, headers=headers).json()
        scan_counts = result["data"]["records"][0]
    except Exception as err:
        logging.warning(f"Error obtaining scan counts: {err}")
    return scan_counts


def get_scan_count(scan_count_type: ScanCountType, chain_id: int) -> int:
    """Gets scan count in the last 24 hours via Zettablock GraphQL API"""
    scan_counts = get_scan_counts(chain_id)
    scan_count_name = scan_count_type.name.lower()
    scan_count = int(scan_counts.get(scan_count_name, 1.0))
    return max(scan_count, 1.0)


def calculate_alert_rate(
    chain_id: int,
    bot_id: str,
    alert_id: str,
    scan_count_type: ScanCountType,
    custom_scan_count: int = None,
) -> float:
    """Calculate bot's alert rate in the last 24 hours.
    Alert Rate Formula: ( bot alert count / scan_count )

    E.g. Bot A's alert rate with scan count type set to
    contract_creation_count on a chain X will be a quotient of 2 numbers:

    1. The bot alert count on chain X
    2. Contract creation counts on chain X

    Args:
        chain_id (int): EIP155 identifier of the chain
        bot_id (str): Forta bot ID
        alert_id (str): Forta bot alert id
        scan_count_type (ScanCountType): Type to use for the denominator value.
        custom_scan_count (int, optional): Custom scan count.Defaults to None.

    Returns:
        float: Bot alert rate
    """
    alert_count = get_alert_count(bot_id, alert_id, chain_id)
    scan_count = custom_scan_count
    if chain_id not in CHAIN_IDS:
        raise ValueError(f"Chain id {chain_id} is not supported.")
    if scan_count_type == ScanCountType.CUSTOM_SCAN_COUNT:
        if not isinstance(custom_scan_count, int):
            raise ValueError("Please pass in an int value for custom_scan_count.")
        if custom_scan_count < alert_count:
            raise ValueError("custom_scan_count can't be less than alert_count.")
    else:
        scan_count = get_scan_count(scan_count_type, chain_id)

    return min(alert_count / scan_count, 1.0)
