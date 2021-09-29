from pathlib import Path
import json
import xml.etree.ElementTree as ET
from results import ProvinceResults, GeneralResults


election_results_path = Path(__file__).parent / "data"
def read_as_json(path):
    with open(path, encoding="utf8") as fd:
        return json.load(fd)

def load_election_results(year: str):
    ...


if __name__ == "__main__":
    ...
