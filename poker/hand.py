from .card import Card


class Hand:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
