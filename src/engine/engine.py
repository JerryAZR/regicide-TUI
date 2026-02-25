from src.models.card import Card, Suit, Rank
from src.models.enemy import Enemy, EnemyType
from src.models.deck import Deck
from src.models.game_state import Player


def calculate_damage(cards: list[Card]) -> int:
    """Calculate total damage from played cards.

    Clubs double their value, other suits are face value.
    """
    total = 0
    for card in cards:
        value = card.value
        if card.suit == Suit.CLUBS:
            value *= 2
        total += value
    return total


def apply_suit_power(card: Card, enemy: Enemy, deck: 'Deck | None', player: 'Player | None' = None) -> dict:
    """Apply the suit power of the played card.

    Returns dict with actions taken (draw, heal, shield, etc.)
    """
    result = {}

    if card.is_animal:
        # Animal companions pair with another card - already accounted for
        pass

    if card.is_jester:
        # Jester cancels immunity
        enemy.jester_played = True
        result['cancelled_immunity'] = True
        return result

    if card.suit == Suit.SPADES:
        enemy.add_shield(card.value)
        result['shield_added'] = card.value

    # Hearts and Diamonds handled in main loop with deck access

    return result


def check_immunity(card: Card, enemy: Enemy) -> bool:
    """Check if the enemy is immune to the card's suit power."""
    if enemy.immunity is None:
        return False
    return card.suit == enemy.immunity


def resolve_hearts_power(deck: 'Deck', attack_value: int) -> int:
    """Hearts: Heal from discard - shuffle discard and put under deck."""
    if not deck.discard_pile:
        return 0

    # Shuffle discard
    import random
    random.shuffle(deck.discard_pile)

    # Move cards under deck (up to attack value)
    cards_to_recycle = min(attack_value, len(deck.discard_pile))
    for _ in range(cards_to_recycle):
        card = deck.discard_pile.pop(0)
        deck.cards.append(card)

    return cards_to_recycle


def resolve_diamonds_power(deck: 'Deck', attack_value: int, player: Player) -> int:
    """Diamonds: Draw cards up to attack value."""
    drawn = 0
    for _ in range(attack_value):
        if len(player.hand) >= player.max_hand_size:
            break
        card = deck.draw()
        if card is None:
            break
        player.hand.append(card)
        drawn += 1
    return drawn
