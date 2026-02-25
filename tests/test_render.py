import pytest
from src.models.card import Card, Suit, Rank
from src.utils.render import render_card, SUIT_COLORS, SUIT_SYMBOLS


class TestCardRendering:
    def test_suit_colors_defined(self):
        assert Suit.HEARTS in SUIT_COLORS
        assert Suit.DIAMONDS in SUIT_COLORS
        assert Suit.CLUBS in SUIT_COLORS
        assert Suit.SPADES in SUIT_COLORS

    def test_render_card_returns_string(self):
        card = Card(rank=Rank(7), suit=Suit.HEARTS)
        rendered = render_card(card)
        assert isinstance(rendered, str)
        assert "7" in rendered
        assert "♥" in rendered

    def test_render_animal_companion(self):
        animal = Card(rank=Rank.ANIMAL, suit=Suit.CLUBS, is_animal=True)
        rendered = render_card(animal)
        assert "A" in rendered or "animal" in rendered.lower()
