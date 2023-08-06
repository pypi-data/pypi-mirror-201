from phiterm.conf.constants import PHI_API_MODE


def test_api_in_prd_mode():
    assert PHI_API_MODE == "prd"
