import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
from automata.cases import CASES
from automata.password import password_dfa, semantic_issues
from automata.email_validator import email_dfa
from automata.atm_pin import pin_format_dfa, session_dfa, verify, weak_pin_reasons

DFAS = {"password": password_dfa, "email": email_dfa,
        "atm_pin": pin_format_dfa, "atm_session": session_dfa}


@pytest.mark.parametrize("app", DFAS)
def test_accepted(app):
    for s in CASES[app]["accept"]:
        assert DFAS[app].accepts(s), f"{app}: {s!r} should be accepted"


@pytest.mark.parametrize("app", DFAS)
def test_rejected(app):
    for s in CASES[app]["reject"]:
        assert not DFAS[app].accepts(s), f"{app}: {s!r} should be rejected"


def test_minimum_five_each():
    for app, c in CASES.items():
        assert len(c["accept"]) >= 5 and len(c["reject"]) >= 5


def test_semantic_layer_is_separate():
    assert password_dfa.accepts("Admin@123")                 # syntactically fine ...
    assert semantic_issues("Admin@123") != []             # ... but blacklisted (semantic)
    assert pin_format_dfa.accepts("1234") and weak_pin_reasons("1234")  # valid format, weak PIN
    assert verify("1234", "4321") == "WRONG PIN"
    assert verify("12a4", "1234").startswith("REJECTED")
