import pytest
from src.models.enemy import Enemy, EnemyType
from src.models.card import Suit


class TestEnemy:
    def test_create_jack(self):
        enemy = Enemy(EnemyType.JACK)
        assert enemy.enemy_type == EnemyType.JACK
        assert enemy.attack == 10
        assert enemy.max_health == 20
        assert enemy.health == 20

    def test_create_queen(self):
        enemy = Enemy(EnemyType.QUEEN)
        assert enemy.enemy_type == EnemyType.QUEEN
        assert enemy.attack == 15
        assert enemy.max_health == 30
        assert enemy.health == 30

    def test_create_king(self):
        enemy = Enemy(EnemyType.KING)
        assert enemy.enemy_type == EnemyType.KING
        assert enemy.attack == 20
        assert enemy.max_health == 40
        assert enemy.health == 40

    def test_take_damage(self):
        enemy = Enemy(EnemyType.JACK)
        enemy.take_damage(7)
        assert enemy.health == 13

    def test_is_defeated(self):
        enemy = Enemy(EnemyType.JACK)
        enemy.take_damage(20)
        assert enemy.is_defeated is True

    def test_shield_reduces_damage(self):
        enemy = Enemy(EnemyType.JACK)
        enemy.add_shield(5)
        assert enemy.shield == 5
        # Shield should reduce incoming damage
        effective = enemy.get_effective_attack()
        assert effective == 5  # 10 - 5 = 5

    def test_immunity(self):
        enemy = Enemy(EnemyType.JACK)  # Jack of Spades
        # Default immunity to matching suit
        assert enemy.immunity == Suit.SPADES

    def test_take_shield_damage(self):
        enemy = Enemy(EnemyType.JACK)
        enemy.add_shield(8)
        enemy.take_damage(5)  # Only 5 damage through shield
        assert enemy.health == 15  # 20 - 5 = 15
