from poker import *

hand = Hand([
    Card(SPADE, 3),
    Card(HEART, 6)
])
table = [
    Card(CLUB, 4),
    Card(DIAMOND, 2),
    Card(SPADE, 10),
    Card(CLUB, 7),
    Card(HEART, ACE)
]

print(hand_ranking(hand, table))
