import pytest
from src.models.game_state import Player, GameState
from src.models.card import Card, Suit, Rank
from src.models.deck import Deck
from src.models.enemy import Enemy, EnemyType


class TestPlayer:
    def test_create_player(self):
        player = Player()
        assert player.hand == []
        assert player.max_hand_size == 8

    def test_draw_card(self):
        player = Player()
        deck = Deck.create_tavern_deck()
        player.draw_card(deck)
        assert len(player.hand) == 1

    def test_play_card(self):
        player = Player()
        card = Card(rank=Rank(7), suit=Suit.HEARTS)
        player.hand.append(card)
        played = player.play_card(0)
        assert played == card
        assert len(player.hand) == 0

    def test_discard_for_damage(self):
        player = Player()
        player.hand = [
            Card(rank=Rank(7), suit=Suit.HEARTS),
            Card(rank=Rank(5), suit=Suit.SPADES),
            Card(rank=Rank(3), suit=Suit.CLUBS),
        ]
        discarded = player.discard_for_damage(10)  # 7 + 3 = 10
        assert len(discarded) == 2


class TestGameState:
    def test_create_initial_state(self):
        state = GameState.new_game()
        assert len(state.player.hand) == 8
        assert len(state.tavern_deck.cards) == 32  # 40 - 8 dealt
        assert state.current_enemy is not None
        assert state.jesters_flipped == 0

    def test_jester_flip(self):
        state = GameState.new_game()
        state.jesters_flipped = 1
        assert state.jesters_flipped == 1
