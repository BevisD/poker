JACK, QUEEN, KING, ACE = 11, 12, 13, 14
CLUB, DIAMOND, HEART, SPADE = 0, 1, 2, 3

SUITS = {
    CLUB: "\u2663",
    DIAMOND: "\u2666",
    HEART: "\u2665",
    SPADE: "\u2660",
}

VALUES = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "T",
    JACK: "J",
    QUEEN: "Q",
    KING: "K",
    ACE: "A",

}


class Card:
    def __init__(self, suit: int, value: int) -> None:
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return (self.suit == other.suit) and (self.value == other.value)

    def __str__(self):
        return VALUES[self.value] + SUITS[self.suit]

    def __repr__(self):
        return self.__str__()