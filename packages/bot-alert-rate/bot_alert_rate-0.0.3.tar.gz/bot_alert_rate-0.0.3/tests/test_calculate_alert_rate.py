import pytest

from bot_alert_rate import calculate_alert_rate, ScanCountType, get_scan_count

EXAMPLE_SCAN_COUNTS = {
    "contract_creation_count": 1250,
    "contract_interaction_count": 1067066,
    "erc_approval_all_count": 2909,
    "erc_approval_count": 68538,
    "erc_transfer_count": 24139,
    "large_value_transfer_count": 58,
    "transfer_count": 60553,
    "tx_count": 1068316,
    "tx_with_input_data_count": 1006267,
}


@pytest.mark.parametrize("chain_id", [1, 56, 42161, 137, 43114, 10, 250])
def test_calculate_alert_rate_with_custom_scan_count(mocker, chain_id):
    bot_id = "test_bot"
    alert_id = "TEST-ALERT"
    custom_value = 1000
    mocker.patch(
        "bot_alert_rate.get_alert_count",
        return_value=1,
    )
    assert (
        calculate_alert_rate(
            chain_id, bot_id, alert_id, ScanCountType.CUSTOM_SCAN_COUNT, custom_value
        )
        == 0.001
    )


@pytest.mark.parametrize("chain_id", [1, 56, 42161, 137])
def test_get_scan_count_for_zettablock_supported_chains(mocker, chain_id):
    zettablock_response = mocker.patch("bot_alert_rate.requests.post")
    zettablock_response.return_value.json.return_value = {
        "data": {"records": [EXAMPLE_SCAN_COUNTS]}
    }
    for scan_type in ScanCountType:
        if scan_type != ScanCountType.CUSTOM_SCAN_COUNT:
            assert (
                get_scan_count(scan_type, chain_id)
                == EXAMPLE_SCAN_COUNTS[scan_type.name.lower()]
            )


@pytest.mark.parametrize("chain_id", [43114, 10, 250])
def test_raise_error_for_zettablock_unsupported_chains(mocker, chain_id):
    for scan_type in ScanCountType:
        if scan_type != ScanCountType.CUSTOM_SCAN_COUNT:
            with pytest.raises(NotImplementedError):
                get_scan_count(scan_type, chain_id)
