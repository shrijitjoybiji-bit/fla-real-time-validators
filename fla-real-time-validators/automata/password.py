"""Application 1 - Password verification.

Policy (syntax only): length >= min_len AND at least one lowercase (L),
uppercase (U), digit (D) and special (S) character; spaces/non-ASCII rejected.

Sigma (symbol classes): L, U, D, S      (X = illegal char -> dead state)
State = (n, mask): n = min(chars read, min_len), mask = which required
classes have been seen. This is the PRODUCT of a length counter DFA and a
"seen-classes" DFA, so it is still a (finite) DFA.
"""
import string
from .dfa import DFA

SPECIALS = set(string.punctuation)


def classify(ch):
    if not ch.isascii():
        return "X"
    if ch.islower():
        return "L"
    if ch.isupper():
        return "U"
    if ch.isdigit():
        return "D"
    if ch in SPECIALS:
        return "S"
    return "X"          # space, control chars, ...


def build_password_dfa(min_len=8, required=("L", "U", "D", "S")):
    k = len(required)
    full = (1 << k) - 1
    name = lambda n, m: f"{n}:{m:0{k}b}"
    states, delta = [], {}
    for n in range(min_len + 1):
        for m in range(1 << k):
            states.append(name(n, m))
            for sym in ("L", "U", "D", "S"):
                m2 = m | (1 << required.index(sym)) if sym in required else m
                delta[(name(n, m), sym)] = name(min(n + 1, min_len), m2)
    accepting = [name(min_len, full)]
    return DFA(f"password_min{min_len}_{''.join(required)}", states,
               name(0, 0), accepting, delta, classify)


password_dfa = build_password_dfa()

# ---- semantic / business rules (NOT regular - done outside the automaton) ----
COMMON = {"password", "password1!", "qwerty123!", "admin@123", "welcome@1"}


def semantic_issues(pw, username=""):
    issues = []
    if pw.lower() in COMMON:
        issues.append("appears in common-password blacklist")
    if username and username.lower() in pw.lower():
        issues.append("contains the username")
    return issues
