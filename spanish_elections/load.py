from pathlib import Path
import json
import xml.etree.ElementTree as ET
from typing import TextIO, Dict

from results import ProvinceResults, GeneralResults


election_results_path = Path(__file__).parent / "data"


def read_as_json(path):
    with open(path, encoding="utf8") as fd:
        return json.load(fd)


def load_election_results(year: str) -> GeneralResults:
    election_data_path = election_results_path / "elections" / year / "congreso"
    province_results = []
    for xml_filepath in election_data_path.glob("*.xml"):
        province_name = xml_filepath.stem
        xml_root = ET.parse(xml_filepath).getroot()
        nseats = extract_nseats_from_xml(xml_root)
        votes_per_pparty = extract_votes_per_pparty_from_xml(xml_root)
        province_results.append(
            ProvinceResults(
                name=province_name,
                nseats=nseats,
                votes_per_pparty=votes_per_pparty
            )
        )
    return GeneralResults(province_results)


def extract_votes_per_pparty_from_xml(root: ET.Element) -> Dict[str, int]:
    votes_per_pparty = {}
    for pparty_xml in root.iter("partido"):
        pparty = pparty_xml.find("nombre").text
        votes = int(pparty_xml.find("votos_numero").text)
        votes_per_pparty[pparty] = votes
    return votes_per_pparty


def extract_nseats_from_xml(root: ET.Element) -> int:
    return int(root.find("num_a_elegir").text)


if __name__ == "__main__":
    last_results = load_election_results("2019")
    breakpoint()
