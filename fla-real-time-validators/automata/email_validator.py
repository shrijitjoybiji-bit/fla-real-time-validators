"""Application 2 - Email format validation (simplified, NOT full RFC 5322).

Language:  local '@' label ('.' label)+     with
  local  : starts with letter/digit; may contain letters, digits, '_', '-';
           single '.' allowed only between alphanumerics (no '..', no trailing '.')
  label  : letters/digits/'-' , must not start or end with '-'
  TLD    : last label = letters only, length >= 2

Sigma classes: L letter, N digit, '.' dot, '-' hyphen, '_' underscore, '@' at.
"""
from .dfa import DFA


def classify(ch):
    if ch.isascii() and ch.isalpha():
        return "L"
    if ch.isascii() and ch.isdigit():
        return "N"
    return ch if ch in ".-_@" else "X"


def build_email_dfa():
    d = {}

    def add(src, syms, dst):
        for s in syms:
            d[(src, s)] = dst

    # local part
    add("q0", "LN", "q1")                 # first char alphanumeric
    add("q1", ["L", "N", "-", "_"], "q1")
    add("q1", ".", "q2")                  # dot must be followed by alnum
    add("q2", "LN", "q1")
    add("q1", "@", "D0")                  # start of first domain label

    # domain, phase 1 (no dot seen yet)  and phase 2 (after >=1 dot)
    def domain(prefix, start_state):
        a1, a2, b, h = (prefix + x for x in ("A1", "A2", "B", "H"))
        add(start_state, "L", a1)
        add(start_state, "N", b)
        add(a1, "L", a2)
        add(a2, "L", a2)
        add(a1, "N", b); add(a2, "N", b)
        add(b, "LN", b)
        add(a1, "-", h); add(a2, "-", h); add(b, "-", h); add(h, "-", h)
        add(h, "LN", b)
        for s in (a1, a2, b):
            add(s, ".", "E0")             # '.' only after a non-hyphen char
        return a2

    domain("1", "D0")                     # labels before the first dot
    tld_ok = domain("2", "E0")            # labels after a dot (accepting: all-letters, len>=2)

    states = ["q0", "q1", "q2", "D0", "1A1", "1A2", "1B", "1H",
              "E0", "2A1", "2A2", "2B", "2H"]
    return DFA("email_format", states, "q0", [tld_ok], d, classify)


email_dfa = build_email_dfa()
