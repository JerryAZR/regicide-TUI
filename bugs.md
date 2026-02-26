# Bug Tracker

## Iteration 1

### BUG-1: Missing enemy suit

**Expected** -- I can see the enemy suit so I can plan my moves with immunity
in mind.

**Actual** -- Enemy shows only name, ATK, and health, no suit.

### BUG-2: Cannot select cards to discard for defense

**Expected** -- I should be able to select which cards to discard during
defense phase.

**Actual** -- Some of my cards are automatically discarded.

### BUG-3: Cannot filp Jester

**Expected** -- I press j to flip jester, discard my current hand and draw 8
new cards. Jester should be set aside and available for filp before I play or
discard cards.

**Actual** -- System warns "No Jester in hand".

### BUG-4: Diamond power not activating

**Expected** -- I should be able to draw cards equal to the rank when playing
a diamond card (without exceeding the "8 cards in hand" limit).

**Actual** -- I am not getting any draws.

### BUG-5: Heart power not activating

**Expected** -- Playing a heart card should recycle cards from the discard pile
back to the deck.

**Actual** -- Neither the discard pile nor the deck is changing.

### BUG-6: Played cards not going into the discard pile

**Expected** -- Cards played against an enemy should be added to the discard
pile when the enemy is defeated.

**Actual** -- Played cards aren't added to discard pile. They are lost forever.

### BUG-7: Cannot play multiple cards as combos

**Expected** -- I should be able to play multiple same-rank cards (total <= 10)
or a pet with any card and activate all the suit powers.

**Actual** -- There is no way to play multiple cards. Pressing enter plays the
selected card and ends my turn.
