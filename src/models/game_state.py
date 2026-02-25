from dataclasses import dataclass, field
from typing import Optional

from src.models.card import Card
from src.models.deck import Deck
from src.models.enemy import Enemy, EnemyType


@dataclass
class Player:
    hand: list[Card] = field(default_factory=list)
    max_hand_size: int = 8

    def draw_card(self, deck: Deck) -> Card | None:
        if len(self.hand) >= self.max_hand_size:
            return None
        card = deck.draw()
        if card:
            self.hand.append(card)
        return card

    def play_card(self, index: int) -> Card | None:
        if 0 <= index < len(self.hand):
            return self.hand.pop(index)
        return None

    def discard_for_damage(self, damage: int) -> list[Card]:
        """Discard cards to cover damage. Returns discarded cards."""
        discarded = []
        total = 0

        # Simple greedy algorithm: discard highest value cards first
        sorted_hand = sorted(enumerate(self.hand),
                           key=lambda x: x[1].value,
                           reverse=True)

        for idx, card in sorted_hand:
            if total >= damage:
                break
            self.hand.remove(card)
            discarded.append(card)
            total += card.value

        return discarded


@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    tavern_deck: Deck = field(default_factory=Deck)
    castle_deck: Deck = field(default_factory=Deck)
    current_enemy: Optional[Enemy] = None
    jesters_flipped: int = 0
    enemies_defeated: int = 0
    turn_count: int = 0

    @classmethod
    def new_game(cls) -> "GameState":
        # Create decks
        tavern = Deck.create_tavern_deck()
        castle = Deck.create_castle_deck()

        # Create player and deal initial hand
        player = Player()
        for _ in range(8):
            player.draw_card(tavern)

        # Get first enemy (top of castle deck is a Jack)
        enemy = Enemy(EnemyType.JACK)

        return cls(
            player=player,
            tavern_deck=tavern,
            castle_deck=castle,
            current_enemy=enemy,
        )

    def handle_enemy_defeated(self) -> None:
        """Handle enemy being defeated."""
        self.enemies_defeated += 1

        # Draw next enemy from castle
        next_card = self.castle_deck.draw()
        if next_card:
            enemy_type = EnemyType.JACK  # Simplified - would need rank parsing
            self.current_enemy = Enemy(enemy_type)
        else:
            self.current_enemy = None  # No more enemies - win!
