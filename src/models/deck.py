import random
from dataclasses import dataclass, field
from typing import Optional

from src.models.card import Card, Suit, Rank


@dataclass
class Deck:
    cards: list[Card] = field(default_factory=list)
    discard_pile: list[Card] = field(default_factory=list)

    @classmethod
    def create_tavern_deck(cls) -> "Deck":
        """Create deck: 2-10 of each suit + 4 animal companions."""
        cards = []
        # Number cards 2-10 for each suit
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:
            for rank in range(2, 11):  # 2-10
                cards.append(Card(rank=Rank(rank), suit=suit))
        # Add 4 animal companions (one per suit)
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:
            cards.append(Card(rank=Rank.ANIMAL, suit=suit, is_animal=True))

        deck = cls(cards=cards)
        deck.shuffle()
        return deck

    @classmethod
    def create_castle_deck(cls) -> "Deck":
        """Create deck: 4 Jacks, 4 Queens, 4 Kings (each suit)."""
        cards = []
        face_cards = [Rank.JACK, Rank.QUEEN, Rank.KING]
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:
            for rank in face_cards:
                cards.append(Card(rank=rank, suit=suit))

        deck = cls(cards=cards)
        deck.shuffle()
        return deck

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Optional[Card]:
        if not self.cards:
            return None
        return self.cards.pop(0)

    def discard(self, card: Card) -> None:
        self.discard_pile.append(card)
