import xml.etree.ElementTree as ET
from typing import Dict

import pytest

from spanish_elections.load import load_election_results, election_results_path


def get_expected_seats_from_xml(year: str, province: str) -> Dict[str, int]:
    filepath = election_results_path / year / "congreso" / f"{province}.xml"
    root = ET.parse(filepath).getroot()
    return {
        party_xml.find("nombre").text: int(party_xml.find("electos").text)
        for party_xml in root.iter("partido")
    }


@pytest.mark.parametrize("year", ["2019", "2019-28A", "2016", "2015", "2011"])
def test_assigned_seats(year: str):
    election_results = load_election_results(year)
    for province_result in election_results.province_results:
        computed_seats = province_result.seats_per_pparty
        expected_seats = get_expected_seats_from_xml(year, province_result.name)
        assert computed_seats == expected_seats, \
            (f"Computed seats for province {province_result.name}"
             " do not match expected seats")
