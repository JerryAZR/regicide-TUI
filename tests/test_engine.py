import pytest
from src.models.card import Suit, Rank, Card
from src.models.enemy import Enemy, EnemyType
from src.engine.engine import (
    calculate_damage,
    apply_suit_power,
    check_immunity,
)


class TestDamageCalculation:
    def test_clubs_double_damage(self):
        card = Card(rank=Rank(8), suit=Suit.CLUBS)
        damage = calculate_damage([card])
        assert damage == 16  # 8 * 2

    def test_non_clubs_no_doubling(self):
        card = Card(rank=Rank(8), suit=Suit.HEARTS)
        damage = calculate_damage([card])
        assert damage == 8

    def test_combo_damage(self):
        # Play 3 + 4 + 2 = 9 (under 10)
        # Clubs (2) doubles to 4, so total = 3 + 4 + 4 = 11
        cards = [
            Card(rank=Rank(3), suit=Suit.DIAMONDS),
            Card(rank=Rank(4), suit=Suit.SPADES),
            Card(rank=Rank(2), suit=Suit.CLUBS),
        ]
        damage = calculate_damage(cards)
        assert damage == 11  # 3 + 4 + (2*2) = 11


class TestSuitPower:
    def test_spades_add_shield(self):
        card = Card(rank=Rank(5), suit=Suit.SPADES)
        enemy = Enemy(EnemyType.JACK)
        apply_suit_power(card, enemy, None)  # No deck for this test
        assert enemy.shield == 5


class TestImmunity:
    def test_jack_immune_to_spades(self):
        enemy = Enemy(EnemyType.JACK)
        card = Card(rank=Rank(7), suit=Suit.SPADES)
        is_immune = check_immunity(card, enemy)
        assert is_immune is True

    def test_non_matching_suit_not_immune(self):
        enemy = Enemy(EnemyType.JACK)
        card = Card(rank=Rank(7), suit=Suit.HEARTS)
        is_immune = check_immunity(card, enemy)
        assert is_immune is False
