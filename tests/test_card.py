import pytest
from src.models.card import Card, Suit, Rank


class TestCard:
    def test_create_number_card(self):
        card = Card(rank=Rank(7), suit=Suit.HEARTS)
        assert card.rank == Rank(7)
        assert card.suit == Suit.HEARTS
        assert card.is_animal is False
        assert card.is_jester is False

    def test_card_value(self):
        card = Card(rank=Rank(7), suit=Suit.HEARTS)
        assert card.value == 7

    def test_hearts_suit_identified(self):
        """Test that Hearts suit is identified correctly for power."""
        card = Card(rank=Rank(7), suit=Suit.HEARTS)
        assert card.suit == Suit.HEARTS

    def test_animal_companion(self):
        animal = Card(rank=Rank.ANIMAL, suit=Suit.CLUBS, is_animal=True)
        assert animal.is_animal is True
        assert animal.value == 1

    def test_jester(self):
        jester = Card(rank=Rank.JESTER, suit=None, is_jester=True)
        assert jester.is_jester is True
        assert jester.value == 0

    def test_jack_is_ten(self):
        """Jacks in hand count as 10."""
        card = Card(rank=Rank.JACK, suit=Suit.SPADES)
        assert card.value == 10

    def test_queen_is_fifteen(self):
        """Queens in hand count as 15."""
        card = Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS)
        assert card.value == 15

    def test_king_is_twenty(self):
        """Kings in hand count as 20."""
        card = Card(rank=Rank.KING, suit=Suit.HEARTS)
        assert card.value == 20
