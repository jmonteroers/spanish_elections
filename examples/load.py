from spanish_elections.load import load_election_results

# available election years: "2011", "2015", "2016", "2019-28A", and "2019"
last_results = load_election_results("2019")
seats_last_results = last_results.get_seats_by_pparty()
pparties = last_results.get_pparties()
print(
    "November 2019 election results: \n"
    f"Seats: {seats_last_results} \n"
    f"Political parties that participated: {pparties}"
)
