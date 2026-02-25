from dataclasses import dataclass, field
from enum import Enum

from src.models.card import Suit


class EnemyType(Enum):
    JACK = "jack"
    QUEEN = "queen"
    KING = "king"


# Enemy stats by type
ENEMY_STATS = {
    EnemyType.JACK: {"attack": 10, "health": 20},
    EnemyType.QUEEN: {"attack": 15, "health": 30},
    EnemyType.KING: {"attack": 20, "health": 40},
}


@dataclass
class Enemy:
    enemy_type: EnemyType
    health: int = 0
    shield: int = 0
    _immunity_suit: Suit | None = None
    jester_played: bool = False  # Jester cancels immunity

    def __post_init__(self):
        stats = ENEMY_STATS[self.enemy_type]
        if self.health == 0:
            self.health = stats["health"]
        self.max_health = stats["health"]
        self.attack = stats["attack"]

        # Default immunity to matching suit (Jack of Spades, etc.)
        if self._immunity_suit is None and self.enemy_type == EnemyType.JACK:
            self._immunity_suit = Suit.SPADES
        elif self._immunity_suit is None and self.enemy_type == EnemyType.QUEEN:
            self._immunity_suit = Suit.DIAMONDS
        elif self._immunity_suit is None and self.enemy_type == EnemyType.KING:
            self._immunity_suit = Suit.HEARTS

    @property
    def is_defeated(self) -> bool:
        return self.health <= 0

    @property
    def immunity(self) -> Suit | None:
        if self.jester_played:
            return None
        return self._immunity_suit

    def take_damage(self, damage: int) -> None:
        # Shield in this game doesn't block damage to enemy -
        # it only reduces enemy's attack against player
        # So all damage goes through
        self.health = max(0, self.health - damage)

    def add_shield(self, amount: int) -> None:
        self.shield += amount

    def get_effective_attack(self) -> int:
        return max(0, self.attack - self.shield)
