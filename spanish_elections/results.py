from typing import Dict, List, Tuple
from collections import defaultdict


def argmax_dict(d: dict) -> str:
    return sorted(d, key=lambda x: -d[x])[0]


class DictWithAddition:
    def __init__(self, d: dict):
        self.d = d

    def __add__(self, other: DictWithAddition) -> DictWithAddition:
        out_d = self.d.copy()
        for key, value in other.d.items():
            out_d[key] = self.d.get(key, 0) + value
        return DictWithAddition(out_d)


class ProvinceResults:
    def __init__(name: str, nseats: int, from_pparty_to_votes: Dict[str, int]):
        self.name = name
        self.nseats = nseats
        self.votest_per_pparty = votes
        self.seats_per_pparty = self.assign_seats_to_pparty()

    def assign_seats_to_pparty(self) -> Dict[str, int]:
        remaining_nseats = self.nseats
        seats = {party: 0 for party in self.votest_per_pparty}
        transformed_results = self.votest_per_pparty.copy()
        while n_seats_remaining:
            most_voted_party = argmax_dict(transformed_results)
            seats[most_voted_party] += 1
            n_seats_remaining -= 1
            ratio_seats = seats[most_voted_party]/(1 + seats[most_voted_party])
            transformed_results[most_voted_party] *= ratio_seats
        return seats

    def transfer_votes(self, transfer_rates: List[Tuple[str, str, float]]):
        '''
        Arguments:
        - transfer_rates: list of tuples with the following structure,
        (source, dest, proportion of votes from source to dest)

        The transfers are applied from the original votes, so the order within
        list_transfer_votes does not affect the result
        '''
        original_votes = self.votest_per_pparty.copy()
        for source, dest, prop in transfer_rates:
            votes_transferred = round(prop*original_votes[source])
            self.votes_per_pparty[source] -= votes_transferred
            self.votes_per_pparty[dest] += votes_transferred
        self.seats_per_pparty = self.assign_seats_to_pparty()


class GeneralResults:
    def __init__(self, province_results: List[ProvinceResults]):
        self.province_results = province_results

    def get_seats_by_pparty(self) -> Dict[str, int]:
        return sum([
        DictWithAddition(province_result.seats_per_pparty)
        for province_result in self.province_results
        ]).d

    def get_votes_by_pparty(self) -> Dict[str, int]:
        return sum([
        DictWithAddition(province_result.votes_per_pparty)
        for province_result in self.province_results
        ]).d

    def retrieve_results_by_province(self,
        name: str) -> Optional[ProvinceResults]:
        for province in self.province_results:
            if province.name == name:
                return province

    def get_results(self) -> List[Tuple[str, int, int]]:
        seats_by_pparty = self.get_seats_by_pparty()
        votes_by_pparty = self.get_votes_by_pparty()
        return [
            (pparty, votes_by_pparty[pparty], seats_by_pparty[pparty])
            for pparty in votes_by_pparty
        ]

    def transfer_votes(self, transfer_rates: List[Tuple[str, str, float]]):
        for province_result in self.province_results:
            province_result.transfer_votes(transfer_rates)

    def get_pparties(self) -> Set[str]:
        return set(
            pparty for province_result.votes_per_pparty.keys()
            for province_result in self.province_results
        )
