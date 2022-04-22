from spanish_elections.load import load_election_results

import pytest

@pytest.mark.parametrize("year", ["2019", "2019-28A", "2016", "2015", "2011"])
def test_load_election_results(year: str):
    election_results = load_election_results(year)
    assert len(election_results.province_results) > 0
