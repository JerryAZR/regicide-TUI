from rich.console import Console
from rich.text import Text
from rich.style import Style

from src.models.card import Card, Suit, Rank

# Suit colors from design spec
SUIT_COLORS = {
    Suit.HEARTS: "#FF6B6B",   # Red
    Suit.DIAMONDS: "#FFD93D",  # Gold
    Suit.CLUBS: "#6BCB77",    # Green
    Suit.SPADES: "#4D96FF",   # Blue
}

SUIT_SYMBOLS = {
    Suit.HEARTS: "♥",
    Suit.DIAMONDS: "♦",
    Suit.CLUBS: "♣",
    Suit.SPADES: "♠",
}


def render_card(card: Card, selected: bool = False) -> str:
    """Render a card as string."""
    if card.is_jester:
        return "🃏"
    if card.is_animal:
        suit = SUIT_SYMBOLS.get(card.suit, "?")
        return f"A{suit}"

    suit = SUIT_SYMBOLS.get(card.suit, "?")
    marker = "►" if selected else ""
    return f"{marker}{card.value}{suit}"


def render_card_simple(card: Card) -> str:
    """Simple string rendering of a card."""
    if card.is_jester:
        return "🃏"
    if card.is_animal:
        suit = SUIT_SYMBOLS.get(card.suit, "?")
        return f"A{suit}"

    suit = SUIT_SYMBOLS.get(card.suit, "?")
    return f"{card.value}{suit}"
