# Gilded Rose — Python Refactoring Kata

My solution to the [Gilded Rose Refactoring Kata](https://github.com/emilybache/GildedRose-Refactoring-Kata) by Emily Bache.

## The Problem

The original `update_quality` method is a deeply nested tangle of conditionals that is hard to read, hard to test, and easy to break. The goal is to refactor it into clean, maintainable code — and then extend it with support for a new item type: Conjured items.

## My Approach

### Refactoring

I kept the `Item` class completely untouched (as required by the problem statement) and focused on restructuring `GildedRose`.

Key decisions:

- **Named constants** for all magic numbers (`MAX_QUALITY`, `BACKSTAGE_PASS_CLOSER_DAYS`, etc.) to make the rules explicit and easy to change
- **One method per item type** (`update_backstage_pass_quality`, `update_aged_brie_quality`, etc.) so each rule lives in one place
- **Centralised quality boundary enforcement** via `enforce_quality_boundaries` — the floor (0) and ceiling (50) are applied in one place rather than scattered across conditions
- **Sell-in is decremented before quality is calculated** — this simplifies the post-expiry checks to a single `if item.sell_in < 0` in each update method

### Extending with Conjured Items

Conjured items degrade at twice the normal rate (2 per day, 4 after expiry). Adding them required:

- A new `update_conjured_quality` method
- A `CONJURED_PREFIX` constant and a `startswith` check so any item named "Conjured ..." is handled correctly

### Testing

Two layers of tests:

- **Unit tests** (`tests/test_gilded_rose.py`) — one test per rule, covering normal items, Aged Brie, Sulfuras, Backstage passes (including all threshold boundaries), Conjured items, and quality floor/ceiling enforcement
- **Approval test** (`tests/test_gilded_rose_approvals.py`) — captures the full 30-day output of the fixture and compares it against an approved snapshot, acting as a regression guard

## Setup

```
pip install -r requirements.txt
```

## Running the Tests

```
python -m pytest
```

## Running the Fixture Manually

For example, 10 days:

```
python texttest_fixture.py 10
```
