from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Header, Footer
from textual.binding import Binding

from src.models.game_state import GameState
from src.models.card import Card, Suit, Rank
from src.models.enemy import Enemy, EnemyType
from src.engine.engine import calculate_damage, apply_suit_power, check_immunity
from src.ui.widgets import EnemyWidget
from src.utils.render import SUIT_SYMBOLS


class GameScreen(App):
    """Main Regicide game screen."""

    CSS = """
Screen {
    background: $surface;
}

#game-container {
    height: 100%;
    padding: 1;
}

#enemy-section {
    height: 3;
    margin-bottom: 1;
}

#hand-section {
    height: auto;
    margin-bottom: 1;
}

#info-section {
    height: 3;
}

#status-bar {
    dock: bottom;
    height: 1;
}

.card {
    margin: 0 1;
}

.selected {
    background: $accent;
}
"""

    BINDINGS = [
        Binding("left", "select_previous", "Previous Card"),
        Binding("right", "select_next", "Next Card"),
        Binding("enter", "play_card", "Play Card"),
        Binding("j", "flip_jester", "Flip Jester"),
        Binding("h", "show_help", "Help"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.game_state = GameState.new_game()
        self.selected_index = 0
        self.message = ""
        self.message_timeout = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("", id="enemy-section"),
            Static("", id="hand-section"),
            Static("", id="info-section"),
            Static("", id="status-bar"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.update_display()

    def update_display(self) -> None:
        state = self.game_state
        enemy = state.current_enemy

        # Enemy section
        enemy_widget = self.query_one("#enemy-section")
        if enemy:
            shield_str = f" | 🛡️{enemy.shield}" if enemy.shield else ""
            enemy_text = f"[bold]⚔️ {enemy.enemy_type.value.upper()}[/bold] | ATK: {enemy.attack} | ❤️ {enemy.health}/{enemy.max_health}{shield_str}"
        else:
            enemy_text = "[bold green]🎉 VICTORY! All enemies defeated![/bold green]"
        enemy_widget.update(enemy_text)

        # Hand section
        hand_widget = self.query_one("#hand-section")
        hand = state.player.hand
        if hand:
            cards_str = "YOUR HAND: "
            for i, card in enumerate(hand):
                marker = "►" if i == self.selected_index else " "
                cards_str += f"{marker}{card.value}{self._suit_symbol(card.suit)} "
            cards_str += f"({len(hand)}/8)"
        else:
            cards_str = "YOUR HAND: [red]EMPTY![/red]"
        hand_widget.update(cards_str)

        # Info section
        info_widget = self.query_one("#info-section")
        discard_count = len(state.tavern_deck.discard_pile)
        deck_count = len(state.tavern_deck.cards)
        jesters = 2 - state.jesters_flipped
        info_text = f"🃏 DISCARD: {discard_count} | 📚 DECK: {deck_count} | 🃏 JESTERS: {jesters}"
        info_widget.update(info_text)

        # Status bar
        status_widget = self.query_one("#status-bar")
        status_text = "[Enter] Play  [←→] Navigate  [J] Jester  [H] Help  [Q] Quit"
        if self.message:
            status_text = f"[yellow]{self.message}[/yellow] | " + status_text
        status_widget.update(status_text)

    def _suit_symbol(self, suit) -> str:
        return SUIT_SYMBOLS.get(suit, "?")

    def action_select_previous(self) -> None:
        if self.game_state.player.hand:
            self.selected_index = (self.selected_index - 1) % len(self.game_state.player.hand)
            self.update_display()

    def action_select_next(self) -> None:
        if self.game_state.player.hand:
            self.selected_index = (self.selected_index + 1) % len(self.game_state.player.hand)
            self.update_display()

    def action_play_card(self) -> None:
        state = self.game_state
        hand = state.player.hand

        if not hand:
            self.message = "No cards in hand!"
            self.update_display()
            return

        if self.selected_index >= len(hand):
            return

        card = hand[self.selected_index]

        # Check for jester
        if card.is_jester:
            self.message = "Use J key to flip Jester!"
            self.update_display()
            return

        enemy = state.current_enemy
        if not enemy:
            self.message = "You already won!"
            self.update_display()
            return

        # Check immunity
        is_immune = check_immunity(card, enemy)

        # Apply suit power (if not immune)
        if not is_immune:
            apply_suit_power(card, enemy, state.tavern_deck, state.player)

        # Deal damage
        damage = calculate_damage([card])
        enemy.take_damage(damage)

        if is_immune:
            self.message = f"Immunity! Power blocked, but {damage} damage dealt."
        else:
            self.message = f"Dealt {damage} damage!"

        # Remove card from hand
        state.player.hand.pop(self.selected_index)

        # Check if enemy defeated
        if enemy.is_defeated:
            self.handle_enemy_defeat()
        else:
            # Enemy attacks
            self.handle_enemy_attack()

        # Clamp selected index
        if self.selected_index >= len(state.player.hand):
            self.selected_index = max(0, len(state.player.hand) - 1)

        self.update_display()

    def handle_enemy_defeat(self) -> None:
        state = self.game_state
        state.enemies_defeated += 1

        # Check victory
        if state.enemies_defeated >= 12:
            self.message = "🎉 VICTORY! All 12 enemies defeated!"
        else:
            # Draw next enemy
            defeated_so_far = state.enemies_defeated
            if defeated_so_far < 4:
                enemy_type = EnemyType.JACK
            elif defeated_so_far < 8:
                enemy_type = EnemyType.QUEEN
            else:
                enemy_type = EnemyType.KING
            state.current_enemy = Enemy(enemy_type)
            self.message = f"Enemy defeated! New enemy: {enemy_type.value.upper()}"

    def handle_enemy_attack(self) -> None:
        state = self.game_state
        enemy = state.current_enemy

        attack_power = enemy.get_effective_attack()

        # Discard cards to cover damage
        discarded = state.player.discard_for_damage(attack_power)

        if discarded:
            # Add to discard pile
            for card in discarded:
                state.tavern_deck.discard(card)
            self.message = f"Enemy deals {attack_power} damage! Discarded {len(discarded)} cards."
        else:
            # Player loses!
            self.message = "💀 GAME OVER! Couldn't cover damage!"
            # Could trigger game over screen here

    def action_flip_jester(self) -> None:
        state = self.game_state

        # Check if player has jester in hand
        jester_in_hand = any(c.is_jester for c in state.player.hand)

        if not jester_in_hand:
            self.message = "No Jester in hand!"
            self.update_display()
            return

        if state.jesters_flipped >= 2:
            self.message = "Already used both Jesters!"
            self.update_display()
            return

        # Flip a jester (discard hand and redraw)
        # Remove jesters from hand
        state.player.hand = [c for c in state.player.hand if not c.is_jester]

        # Draw back up to 8
        for _ in range(8):
            state.player.draw_card(state.tavern_deck)

        state.jesters_flipped += 1
        self.message = f"Jester flipped! ({state.jesters_flipped}/2 used)"
        self.update_display()

    def action_show_help(self) -> None:
        self.message = "HEARTS: recycle discards | DIAMONDS: draw cards | CLUBS: 2x damage | SPADES: shield"
        self.update_display()

    def action_quit(self) -> None:
        self.exit()
