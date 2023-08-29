from .hand import Hand
from .card import Card
from .card import JACK, QUEEN, KING, ACE, CLUB, DIAMOND, HEART, SPADE

straights = [
    {10, JACK, QUEEN, KING, ACE},
    {9, 10, JACK, QUEEN, KING},
    {8, 9, 10, JACK, QUEEN},
    {7, 8, 9, 10, JACK},
    {6, 7, 8, 9, 10},
    {5, 6, 7, 8, 9},
    {4, 5, 6, 7, 8},
    {3, 4, 5, 6, 7},
    {2, 3, 4, 5, 6},
    {ACE, 2, 3, 4, 5}
]

"""
ROYAL FLUSH: (9)
STRAIGHT FLUSH: (8, A)
FOUR KIND: (7, A, B)
FULL HOUSE: (6, A, B)
FLUSH: (5, A, B, C, D, E)
STRAIGHT: (4, A)
THREE KIND: (3, A, B, C)
TWO PAIR: (2, A, B, C)
PAIR: (1, A, B, C, D)
HIGH CARD: (0, A, B, C, D, E)
"""


def royal_flush(suit_groups: dict, value_groups: dict) -> list[int]:
    for suit, values in suit_groups.items():
        if values.issuperset({10, JACK, QUEEN, KING, ACE}):
            return [9]
    return []


def straight_flush(suit_groups: dict, value_groups: dict) -> list[int]:
    for suit, values in suit_groups.items():
        if len(values) < 5:
            continue

        for straight_set in straights:
            if values.issuperset(straight_set):
                return [8, max(straight_set)]
    return []


def four_kind(suit_groups: dict, value_groups: dict) -> list[int]:
    for value, suits in value_groups.items():
        if len(suits) == 4:
            new_groups = value_groups.copy()
            new_groups.pop(value)
            return [7, value] + get_highest_cards(new_groups, 1)
    return []


def full_house(suit_groups: dict, value_groups: dict) -> list[int]:
    tk = three_kind(suit_groups, value_groups)
    if not tk:
        return []
    new_groups = value_groups.copy()
    new_groups.pop(tk[1])
    pr = pair(suit_groups, new_groups)

    if pr:
        return [6, tk[1], pr[1]]


def flush(suit_groups: dict, value_groups: dict) -> list[int]:
    for suit, values in suit_groups.items():
        if len(values) >= 5:
            return [5] + sorted(values, reverse=True)[:5]
    return []


def straight(suit_groups: dict, value_groups: dict) -> list[int]:
    values = value_groups.keys()
    for straight_set in straights:
        if straight_set.issubset(values):
            return [4, max(straight_set)]
    return []


def three_kind(suit_groups: dict, value_groups: dict) -> list[int]:
    for value, suits in value_groups.items():
        if len(suits) == 3:
            new_groups = value_groups.copy()
            new_groups.pop(value)
            return [3, value] + get_highest_cards(new_groups, 2)
    return []


def two_pair(suit_groups: dict, value_groups: dict) -> list[int]:
    pr1 = pair(suit_groups, value_groups)
    if not pr1:
        return []

    new_groups = value_groups.copy()
    new_groups.pop(pr1[1])
    pr2 = pair(suit_groups, new_groups)

    if not pr2:
        return []

    new_groups.pop(pr2[1])

    return [2] + \
        sorted([pr1[1], pr2[1]], reverse=True) + \
        get_highest_cards(new_groups, 1)


def pair(suit_groups: dict, value_groups: dict) -> list[int]:
    for value, suits in value_groups.items():
        if len(suits) == 2:
            new_groups = value_groups.copy()
            new_groups.pop(value)
            return [1, value] + get_highest_cards(new_groups, 2)
    return []


def high_card(suit_groups: dict, value_groups: dict) -> list[int]:
    return [0] + get_highest_cards(value_groups, 5)


def get_highest_cards(value_groups: dict, n: int = 1) -> list[int]:
    temp_groups = value_groups.copy()
    result = []
    for i in range(n):
        highest = max(temp_groups.keys())
        result.append(highest)
        temp_groups.pop(highest)
    return result


hand_rankings = [
    royal_flush,
    straight_flush,
    four_kind,
    full_house,
    flush,
    straight,
    three_kind,
    two_pair,
    pair,
    high_card
]


def winning_hands(hands: list[Hand], table: list[Card]) -> list[int]:
    player_hands = [hand_ranking(hand) for hand in hands]

    winners = [0]
    best_hand = player_hands[0]

    for player_index, player_hand in enumerate(player_hands[1:]):

        if player_hand == best_hand:
            winners.append(player_index)
            continue

        for h1, h2 in zip(player_hand, best_hand):
            if h1 < h2:
                break
            elif h1 > h2:
                winners = [player_index]
                best_hand = player_hand
                break
    return winners


def hand_ranking(hand: Hand, table: list[Card]) -> list[int]:
    cards = hand.cards + table
    suit_groups = {}
    value_groups = {}

    for card in cards:
        try:
            suit_groups[card.suit].add(card.value)
        except KeyError:
            suit_groups[card.suit] = {card.value}

        try:
            value_groups[card.value].add(card.suit)
        except KeyError:
            value_groups[card.value] = {card.suit}

    for rank in hand_rankings:
        result = rank(suit_groups, value_groups)
        if result:
            return result
