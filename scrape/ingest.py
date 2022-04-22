from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict, List
from datetime import datetime

from models import Election, PPartyResult, ProvinceResult, create_databases


DB_FILENAME = "elections.db"
INPUT_PATH = Path(__file__).parent / "elections"
OUTPUT_PATH = Path(__file__).parent / DB_FILENAME


from_year_to_date = {
    "2011": "2011-11-20",
    "2015": "2015-12-20",
    "2016": "2016-06-26", 
    "2019-28A": "2019-04-28",
    "2019": "2019-11-10"
}


class ElectionCollection:
    def __init__(self, election: Election):
        self.election = election
        self.province_results = []
        self.pparty_results = []
    
    def add_result_in_province(self, province_result: ProvinceResult, pparty_results: List[PPartyResult]):
        self.province_results.append(province_result)
        for pparty_result in pparty_results:
            self.pparty_results.append(pparty_result)
    
    def save_to_db(self, session):
        """Add Election collection in the right order to Database"""
        session.add(self.election)
        session.add_all(self.province_results)
        session.add_all(self.pparty_results)


def load_data_for_election(session, year: str, election_type: str):
    election_path = INPUT_PATH / year / election_type
    election = Election(
        date=datetime.strptime(from_year_to_date[year], "%Y-%m-%d"), 
        type=election_type
        )
    for xml_path in election_path.glob("*.xml"):
        map_province_result = extract_province_result_from_xml(xml_path)
        province_result = ProvinceResult(**map_province_result)
        map_pparty_results = extract_pparty_results_from_xml(xml_path)
        province_result.results_per_pparty = [
            PPartyResult(province_result_id=province_result.id, **map_results)
            for map_results in map_pparty_results
        ]
        election.province_results.append(province_result)
    session.add(election)
    session.commit()


def extract_province_result_from_xml(path: Path) -> Dict[str, str]:
    xml_root = ET.parse(path).getroot()
    res = {}
    res["province_name"] = xml_root.find("nombre_sitio").text
    res["perc_counted"] = xml_root.find("porciento_escrutado").text
    res["province_id"] = xml_root.find("id").text
    res["total_seats"] = xml_root.find("num_a_elegir").text
    res["ballots"] = xml_root.find("votos").find("contabilizados").find("cantidad").text
    res["null_ballots"] = xml_root.find("votos").find("nulos").find("cantidad").text
    res["blank_ballots"] = xml_root.find("votos").find("blancos").find("cantidad").text
    res["abstentions"] = xml_root.find("votos").find("abstenciones").find("cantidad").text
    return res

def extract_pparty_results_from_xml(path: Path) -> List[Dict[str, str]]:
    root = ET.parse(path).getroot()
    pparties_results = []
    for pparty_xml in root.iter("partido"):
        pparty = {}
        pparty["name"] = pparty_xml.find("nombre").text
        pparty["pparty_id"] = pparty_xml.find("id_partido").text
        pparty["ballots"] = pparty_xml.find("votos_numero").text
        pparty["seats"] = pparty_xml.find("electos").text
        pparties_results.append(pparty)
    return pparties_results


def main():
    engine = create_engine(f"sqlite:///{str(OUTPUT_PATH)}")
    Session = sessionmaker(bind=engine)
    session = Session()
    create_databases(engine)
    for election_year in from_year_to_date.keys():
        load_data_for_election(session, election_year, "congreso")


if __name__ == "__main__":
    main()