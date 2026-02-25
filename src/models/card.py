from enum import Enum
from dataclasses import dataclass


class Suit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"


class Rank(Enum):
    # Number cards
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    # Face cards (used in hand as values)
    JACK = 10
    QUEEN = 15
    KING = 20
    # Special cards
    ANIMAL = "animal"
    JESTER = "jester"


@dataclass
class Card:
    rank: Rank
    suit: Suit | None
    is_animal: bool = False
    is_jester: bool = False

    @property
    def value(self) -> int:
        if self.is_jester:
            return 0
        if self.is_animal:
            return 1
        if isinstance(self.rank, Rank):
            return self.rank.value
        # Handle integer ranks (2-10)
        try:
            return int(self.rank.value)
        except (AttributeError, ValueError):
            return 1
