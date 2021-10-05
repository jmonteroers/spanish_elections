from spanish_elections.blocs import load_bloc_by_name
from spanish_elections.load import load_election_results

def test_investment_2020():
    seats_nov_2019 = load_election_results("2019").get_seats_by_pparty()
    bloc_inv_2020 = load_bloc_by_name("investment_2020")
    bloc_seats_nov_2019 = bloc_inv_2020.get_results_by_bloc(seats_nov_2019)
    assert bloc_seats_nov_2019["pro"] > bloc_seats_nov_2019["against"], \
        "2020 Investment must have more votes in favour than against"
    assert bloc_seats_nov_2019 == {
        "pro": 166,
        "against": 164,
        "abstain": 18,
        None: 2
    }, "Investment results don't match - not counting CCa-PNC-NC"
