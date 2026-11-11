"""Application 3 - ATM PIN verification.

(a) PIN FORMAT DFA : exactly 4 or 6 decimal digits.  Sigma = {d (digit), x (other)}
(b) SESSION DFA    : tracks attempts. Sigma = {C (correct PIN), W (wrong PIN)}.
    Locks the card after 3 consecutive wrong attempts.

Whether a PIN is *correct* needs the bank database -> semantic rule, outside the FA.
"""
from .dfa import DFA

# ---------- (a) format ----------
fmt_delta = {(f"s{i}", "d"): f"s{i+1}" for i in range(6)}
pin_format_dfa = DFA("atm_pin_format",
                     [f"s{i}" for i in range(7)], "s0", ["s4", "s6"],
                     fmt_delta, lambda ch: "d" if ch.isascii() and ch.isdigit() else "x")

# ---------- (b) attempt/session automaton ----------
sess_delta = {
    ("A0", "C"): "OPEN", ("A0", "W"): "A1",
    ("A1", "C"): "OPEN", ("A1", "W"): "A2",
    ("A2", "C"): "OPEN", ("A2", "W"): "LOCKED",
    ("OPEN", "C"): "OPEN", ("OPEN", "W"): "OPEN",
    ("LOCKED", "C"): "LOCKED", ("LOCKED", "W"): "LOCKED",
}
session_dfa = DFA("atm_session", ["A0", "A1", "A2", "OPEN", "LOCKED"], "A0",
                  ["OPEN"], sess_delta, lambda ch: ch)

# ---------- semantic rules (outside the automaton) ----------
def weak_pin_reasons(pin):
    reasons = []
    if len(set(pin)) == 1:
        reasons.append("all digits identical")
    if pin in "01234567890" or pin in "09876543210":
        reasons.append("sequential digits")
    if pin in {"1234", "1111", "0000", "2580", "1212"}:
        reasons.append("very common PIN")
    return reasons


def verify(pin, stored_pin):
    """Syntax first (DFA), then business rule (database comparison)."""
    if not pin_format_dfa.accepts(pin):
        return "REJECTED: bad format"
    return "ACCEPTED" if pin == stored_pin else "WRONG PIN"
