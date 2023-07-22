from pathlib import Path
import csv
from dataclasses import dataclass
from urllib.request import urlretrieve
from urllib.error import URLError
import time
from datetime import datetime

codes_filepath = Path(__file__).parent / "aacc_province_codes.csv"
data_filepath = Path(__file__).parent / "elections"

# Some codes provided by INE don't match those used in ElPais website
ac_corrections = {
    "Castilla y León": "08",
    "Castilla-La Mancha": "07",
    "Comunitat Valenciana": "17",
    "Extremadura": "10",
    "Galicia": "11",
    "Madrid, Comunidad de": "12",
    "Murcia, Región de": "15",
    "Navarra, Comunidad Foral de": "13",
    "País Vasco": "14",
    "Rioja, La": "16"
}


class ProvinceData:
    def __init__(self, name: str, code: str, autonomous_community: str,
                 autonomous_community_code: str):
        self.name = self.ensure_single_name(name)
        self.code = code
        self.autonomous_community = autonomous_community
        self.autonomous_community_code =  ac_corrections.get(
            autonomous_community, autonomous_community_code
        )

    @staticmethod
    def ensure_single_name(name: str) -> str:
        if "/" not in name:
            return name
        return name.split("/")[0]

    def get_general_elections_congreso_url(self, year: str) -> str:
        year_url = (
            f"https://rsl00.epimg.net/elecciones/{year}/generales/congreso"
        )
        return f"{year_url}/{self.autonomous_community_code}/{self.code}.xml2"


class ElPaisScraper:
    def __init__(self):
        self.election_years = ["2019", "2019-28A", "2016", "2015", "2011"]
        self.province_codes = list(self.get_province_codes())

    @staticmethod
    def get_province_codes():
        with open(codes_filepath) as f:
            codes_reader = csv.reader(f, delimiter="\t")
            for idx, province_line in enumerate(codes_reader):
                if idx == 0:
                    continue
                ac_code, ac, province_code, province = province_line
                yield ProvinceData(
                    name=province,
                    code=province_code,
                    autonomous_community=ac,
                    autonomous_community_code=ac_code
                )

    def scrape_elections_congreso_year(self, year: str):
        for province in self.province_codes:
            output_path = data_filepath / year / "congreso"
            output_path.mkdir(parents=True, exist_ok=True)
            try:
                province_url = province.get_general_elections_congreso_url(year)
                urlretrieve(
                    province_url,
                    output_path / f"{province.name}.xml"
                )
                # be respectful
                time.sleep(1)
            except URLError:
                print(f"Error retrieving {province} election results"
                      f" from {province_url}")

    def scrape_elections_congreso_all_years(self):
        for election_year in self.election_years:
            print(
                f"{datetime.utcnow()}: Starting download of "
                f"election year {election_year}"
                )
            self.scrape_elections_congreso_year(election_year)
            print(
                f"{datetime.utcnow()}: Finished download of "
                f"election year {election_year}"
                )




if __name__ == "__main__":
    ElPaisScraper().scrape_elections_congreso_all_years()
