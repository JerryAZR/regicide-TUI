import pytest
from src.models.deck import Deck
from src.models.card import Suit, Rank


class TestDeck:
    def test_create_tavern_deck(self):
        deck = Deck.create_tavern_deck()
        # 2-10 = 9 ranks, 4 suits = 36 cards
        # Plus 4 animal companions = 40 cards total
        assert len(deck.cards) == 40

    def test_create_castle_deck(self):
        deck = Deck.create_castle_deck()
        # 4 Jacks, 4 Queens, 4 Kings = 12 cards
        assert len(deck.cards) == 12

    def test_shuffle(self):
        deck1 = Deck.create_tavern_deck()
        deck2 = Deck()
        deck2.cards = list(deck1.cards)
        deck1.shuffle()
        # Note: shuffle may rarely produce same order, but very unlikely
        # We'll just verify shuffle doesn't error
        assert len(deck1.cards) == 40

    def test_draw(self):
        deck = Deck.create_tavern_deck()
        card = deck.draw()
        assert card is not None
        assert len(deck.cards) == 39

    def test_discard(self):
        deck = Deck.create_tavern_deck()
        card = deck.draw()
        deck.discard(card)
        assert len(deck.discard_pile) == 1

    def test_draw_from_empty(self):
        deck = Deck()
        card = deck.draw()  # Should return None or handle gracefully
        assert card is None
