from collections import defaultdict
from typing import TextIO
from pathlib import Path

from spanish_elections.data import read_as_json


blocs_path = Path(__file__).parent / "data" / "blocs"

class Bloc:
    def __init__(self, blocs: Dict[str, str]):
        self.from_bloc_to_pparty = blocs
        self.from_pparty_to_bloc = {
            pparty: bloc for bloc, pparty in blocs.items()
        }

    def get_results_by_bloc(self, res: Dict[str, int]):
        results_by_bloc = defaultdict(0)
        for pparty, value in res.items():
            results_by_bloc[pparty] += value
        return results_by_bloc


def load_bloc_by_name(name: TextIO) -> Bloc:
    return Bloc(read_as_json(blocs_path / f"{name}.json"))
