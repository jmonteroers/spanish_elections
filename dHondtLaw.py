# Here I implement a dHondt object, that allows to estimate how many seats each
# political party would get, given the number of votes to each party and the
# total number of seats that are to be assigned

# Assumes that most voted parties are entered first; important to handle draws
# according to the most-voted party rule
# see https://www.lne.es/espana/2017/12/13/funciona-ley-d-hont-publicar/2208031.html

from collections import defaultdict
import operator
import logging
logging.basicConfig(level=logging.INFO, format = ' %(lineno)d - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

class dHondt:
    def __init__(self, seats, results, extra=False):
        '''extra allows to see how many more votes would have
        needed a party to win an additional seat
        fewerVotes is a dictionary with only one element with the name of the
        winner and how many fewer votes would need to have to lose that last seats
        '''
        self.seats = seats
        self.results = results
        self.finalSeats = defaultdict(int)
        self.extra = extra
        if extra:
            # initially, all extraVotes are set to 0!
            self.extraVotes = dict(zip(list(results.keys()), [0]*len(results)))
            self.lastWinner = {}

    def __repr__(self):
        if self.finalSeats == {}:
            return 'No result has been computed yet'
        else:
            counter = 0  # to get the right ordinal
            ord = ['primer', 'segundo', 'tercer', 'cuarto', 'quinto', 'sexto']
            final_str = 'Las elecciones han quedado como sigue: \n'
            for name in sorted(self.finalSeats, key=self.finalSeats.get, reverse=True):
                if self.extra:
                    if name != list(self.lastWinner.keys())[0]:
                        final_str += (f'En {ord[counter]} lugar, {name}, con '
                                      f'{self.finalSeats[name]} escaño(s), '
                                      f'con {self.results[name]} votos.'
                                      f' Necesitaria {self.extraVotes[name]}'
                                      ' votos mas para el siguiente escaño \n')
                    else:
                        final_str += (f'En {ord[counter]} lugar, {name}, con '
                                      f'{self.finalSeats[name]} escaño(s), '
                                      f'con {self.results[name]} votos.'
                                      f' Con {self.lastWinner[name]}'
                                      ' votos menos perdería el siguiente escaño \n')
                else:
                    final_str += (f'En {ord[counter]} lugar, {name}, con '
                                  f'{self.finalSeats[name]} escaño(s), '
                                  f'con {self.results[name]} votos. \n')
                counter += 1
            return final_str

    def allocSeats(self):
        ''' Initialising variables
        # seat_rems is the number of remaining seats to be assigned
        # result is a dict with values the number of votes
        valid at each step of the algorithm
        # alloc_seats is a dict with the number of seats currently
        allocated to each party
        '''
        seats_rem = self.seats
        results = dict(self.results)
        alloc_seats = dict(zip(results.keys(), [0] * len(results)))
        # Assigning seats
        while seats_rem > 0:
            index_winner = max(results.items(), key=operator.itemgetter(1))[0]
            logging.info(index_winner)

            # Allocating seat to winner
            alloc_seats[index_winner] += 1
            seats_rem -= 1

            # Getting info to know how many more votes would have been needed
            # to obtain another seat
            if self.extra and seats_rem == 1:
                # needed to obtain how many more votes the last party winning
                # a seat would have needed to obtain another vote
                v_min_min = results[index_winner]
            # In final iteration, obtain self.extraVotes
            elif self.extra and seats_rem == 0:
                for name in self.results.keys():
                    logging.info(f'{name} will be assigned '
                    f'{results[index_winner] * (alloc_seats[name] + 1) - self.results[name]}')
                    self.extraVotes[name] = results[index_winner] \
                        * (alloc_seats[name] + 1) - self.results[name]
                # Change formula for last seat winner
                self.extraVotes[index_winner] = v_min_min * \
                    (alloc_seats[index_winner] + 1) \
                    - self.results[index_winner]
                # Modify fewerVotes with name of the winner and how many votes
                # it would have to lose to lose a seat
                # get list with last results sorted
                ordered_results = sorted(results, key=results.get, reverse=True)
                second_winner_votes = results[ordered_results[1]]
                fewerVotes = (results[ordered_results[0]]
                              - second_winner_votes) \
                    * alloc_seats[ordered_results[0]]
                self.lastWinner[ordered_results[0]] = fewerVotes



            # Adapting current vote count within the algorithm
            results[index_winner] = \
                results[index_winner] * (alloc_seats[index_winner]) \
                / (alloc_seats[index_winner] + 1)

            # Print statements
            print(f'{index_winner} ha ganado un escaño en el'
                  ' Congreso')

        # Finally, edit the corresponding attribute with the result
        self.finalSeats = alloc_seats
        return alloc_seats


# Testing
# This has lots of magic numbers, improve
# should improve with a dictionary
# keys, political parties' names; votes as values
resultados_Cord = dHondt(
                         6, {'PS0E': 146166.0, 'PP': 99766.0, 'Vox': 82162.0,
                             'Podemos': 64111.0, 'Cs': 36039.0}, True)
resultados_Cord.allocSeats()
print(resultados_Cord)

'''
resultados_inventados = dHondt(2, ['Joker', 'Batman'], [150000, 75000])
resultados_inventados.allocSeats()

# Counterfactual
# based on https://elpais.com/politica/2019/10/28/actualidad/1572277020_795493.html
# assumption: votes from MP go 1/3 and 2/3 to PSOE and Podemos, corr.
MP = 4.1  # votes to MP
rescaling = [(27+MP/3)/28.7, 21.6/17.1, 9.3/15.9, (12.3+2*MP/3)/14.3, 12.1/10.3]
votos = list(np.array(votos) * np.array(rescaling))
logging.info(votos)
resultados_Cord_pred = dHondt(6, ['PSOE', 'PP', 'Cs', 'Podemos', 'Vox'], votos, True)
resultados_Cord_pred.allocSeats()
print(resultados_Cord_pred)
'''
