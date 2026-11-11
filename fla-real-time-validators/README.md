# Designing Automata for Real-Time Applications
**21CSC301T Formal Language and Automata - CLA-2, Task 2** (SDG 9: Industry, Innovation and Infrastructure)

Finite automata (DFA) that validate the *syntax* of three real inputs, with a small Python engine, test evidence and diagrams.

| # | Application | Language | Automaton |
|---|-------------|----------|-----------|
| 1 | Password | length >= 8, has lower, upper, digit, special, no spaces | product DFA: length counter x seen-classes (144 states) |
| 2 | Email format | `local@label(.label)+`, TLD letters only, len >= 2 | 13-state hand-built DFA |
| 3 | ATM PIN | exactly 4 or 6 digits (+ attempt-counter DFA, locks after 3 wrong) | 7-state DFA + 5-state DFA |

## Run
```bash
pip install -r requirements.txt
python demo.py            # interactive, shows state-by-state trace
python demo.py --report   # accepted/rejected tables (use as evidence screenshot)
pytest                    # automated tests
python export_diagrams.py # .dot (and .png if Graphviz installed) in diagrams/
```

## Assumptions
- Alphabet = ASCII; characters are grouped into classes (L, U, D, S, ...) so the DFA stays small.
- Email is a simplified subset of RFC 5322 (no quoted strings, no `+`, no IP domains, no unicode).
- Missing transitions go to an implicit dead state (omitted from diagrams).

## Syntax vs semantic rules
| Syntax (finite automaton is enough) | Semantic / business (needs extra processing) |
|---|---|
| password has the required character classes | not a common password, doesn't contain username, not breached |
| email has valid shape | mailbox actually exists (send a confirmation mail), domain has MX record |
| PIN is 4 or 6 digits | PIN matches the bank database, not 0000/1234 |

## Limitations
- A DFA has finite memory: it cannot *count unboundedly* or compare two parts of the input
  (e.g. "password != username", "confirm-password equals password", nested/quoted email syntax).
- It can only say whether the string is *well-formed*, never whether it is *true/allowed*.
- Password DFA state count grows as 2^k x (min_len+1) with the number of required classes.

## Test evidence
>= 5 accepted and >= 5 rejected strings per application are in `automata/cases.py`.
