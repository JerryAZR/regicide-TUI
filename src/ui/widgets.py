from textual.widgets import Static

from src.models.card import Card, Suit, Rank
from src.utils.render import SUIT_COLORS, SUIT_SYMBOLS


class CardWidget(Static):
    """A widget that displays a single card."""

    def __init__(self, card: Card, selected: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.selected = selected

    def render(self):
        # Simple text representation
        if self.card.is_jester:
            return "[bold]🃏[/bold]"
        if self.card.is_animal:
            suit = SUIT_SYMBOLS.get(self.card.suit, "?")
            color = SUIT_COLORS.get(self.card.suit, "white")
            return f"[bold {color}]A{suit}[/bold {color}]"

        suit = SUIT_SYMBOLS.get(self.card.suit, "?")
        color = SUIT_COLORS.get(self.card.suit, "white")
        marker = "►" if self.selected else " "
        return f"[bold]{marker}{self.card.value}{suit}[/bold]"


class HandWidget(Static):
    """Displays the player's hand."""

    def __init__(self, hand: list[Card], selected_index: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.hand = hand
        self.selected_index = selected_index


class EnemyWidget(Static):
    """Displays the current enemy."""

    def __init__(self, enemy, **kwargs):
        super().__init__(**kwargs)
        self.enemy = enemy

    def render(self) -> str:
        if not self.enemy:
            return "[bold green]VICTORY![/bold green]"

        name = self.enemy.enemy_type.value.upper()
        atk = self.enemy.attack
        hp = self.enemy.health
        max_hp = self.enemy.max_health
        shield = self.enemy.shield

        shield_str = f" | 🛡️{shield}" if shield > 0 else ""

        return f"[bold]{name}[/bold] | ⚔️{atk} | ❤️{hp}/{max_hp}{shield_str}"
