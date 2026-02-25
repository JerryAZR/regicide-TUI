# Regicide TUI - Design Document

**Date:** 2026-02-26
**Project:** Terminal-based Regicide game

---

## Overview

A polished, keyboard-driven terminal UI implementation of the Regicide solo card game using Python with Rich and Textual frameworks.

---

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│           TUI Layer                 │  Textual App, Screens, Widgets
├─────────────────────────────────────┤
│          Bridge Layer               │  Connects Game Logic ↔ UI
├─────────────────────────────────────┤
│         Game Logic Layer            │  Pure game state, rules, deck management
└─────────────────────────────────────┘
```

### Directory Structure

```
regicide-tui/
├── src/
│   ├── models/           # Card, Deck, Enemy, Player, GameState
│   ├── engine/           # Game rules, turn processing, damage calculation
│   ├── ui/               # Textual screens, card widgets, layouts
│   └── utils/            # Card rendering, colors, helpers
├── docs/
│   └── plans/            # Design documents
└── tests/                # Unit tests
```

---

## Core Components

### Models (`models/`)

| Class | Responsibility |
|-------|----------------|
| `Card` | rank, suit, is_animal, is_jester, display properties |
| `Deck` | shuffle, draw, discard pile management |
| `Enemy` | type (Jack/Queen/King), attack, health, immunity |
| `Player` | hand, max_hand_size |
| `GameState` | complete game state (hand, deck, discard, castle, jester count) |

### Engine (`engine/`)

| Function | Responsibility |
|----------|----------------|
| `create_deck()` | Build tavern deck (2-10 + animals, no Jesters) |
| `create_castle()` | Build castle deck (Jacks, Queens, Kings) |
| `apply_suit_power()` | Hearts: heal, Diamonds: draw, Clubs: double damage, Spades: shield |
| `process_turn()` | Execute full turn: play card → suit power → damage → enemy attack |
| `check_victory()` | Win (all Kings defeated) / Lose (can't cover damage) |
| `calculate_damage()` | Handle clubs doubling, spades shielding |
| `check_immunity()` | Enemy immunity to matching suit powers |

### UI (`ui/`)

| Component | Purpose |
|----------|---------|
| `GameScreen` | Main gameplay screen |
| `CardWidget` | Individual card rendering |
| `HandWidget` | Player's hand display |
| `EnemyWidget` | Current enemy display |
| `InfoBar` | Deck/discard count, jester usage |

---

## UI Layout

```
┌─────────────────────────────────────────────┐
│  ⚔️ BATTLE ZONE                             │
│  ┌──────── │
│  │  JACK─┐                                  │  ATK: 10  HP: 20/20           │
│  │   ♥️    │  Shield: 5                    │
│  └─────────┘                                │
├─────────────────────────────────────────────┤
│  YOUR HAND (5/8)                            │
│  [7♥] [A♠] [4♦] [J♣] [K♥] [2♥] [9♦] [5♠] │
├─────────────────────────────────────────────┤
│  🃏 DISCARD: 12 cards   DECK: 24 cards     │
│  Last: 7♣ 4♦ 9♥                             │
├─────────────────────────────────────────────┤
│  [Enter] Play  [↑↓] Select  [H] Help  [Q] Quit │
└─────────────────────────────────────────────┘
```

---

## Suit Color Scheme

| Suit | Color | Hex |
|------|-------|-----|
| Hearts | Red | `#FF6B6B` |
| Diamonds | Gold | `#FFD93D` |
| Clubs | Green | `#6BCB77` |
| Spades | Blue | `#4D96FF` |

---

## Interaction

- **Arrow Keys** — Navigate cards in hand
- **Enter** — Play selected card
- **H** — Show help overlay
- **Q** — Quit game
- **J** — Flip Jester (solo power)
- **C** — Play combo (2-4 cards same number, sum ≤ 10)

---

## Error Handling

- Invalid moves show inline error message (auto-dismiss after 2s)
- Empty deck draws handled gracefully per rules
- Clear win/lose screens with stats (Jesters used, enemies defeated)

---

## Testing Strategy

- Unit tests for game logic (engine, models)
- Integration tests for game flow
- UI tested manually for polish

---

## Acceptance Criteria

1. ✅ Game follows all rules in Regicide_Rules.md
2. ✅ Visual card rendering with colored suits
3. ✅ Keyboard-first navigation feels smooth
4. ✅ Clear display of hand, enemy, deck, discard
5. ✅ Win/Lose screens with game stats
6. ✅ Clean code structure for future extension
