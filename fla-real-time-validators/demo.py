"""Run:  python demo.py            -> interactive menu
       python demo.py --report    -> print all accepted/rejected test tables (screenshot for evidence)"""
import sys
from automata.cases import CASES
from automata.password import password_dfa, semantic_issues
from automata.email_validator import email_dfa
from automata.atm_pin import pin_format_dfa, session_dfa, weak_pin_reasons

APPS = {"1": ("password", password_dfa), "2": ("email", email_dfa),
        "3": ("atm_pin", pin_format_dfa), "4": ("atm_session", session_dfa)}


def show(dfa, text):
    r = dfa.run(text)
    print(f"\nInput {text!r}")
    for ch, sym, a, b in r.trace:
        print(f"   {a:>8} --{ch!r}({sym})--> {b}")
    print("   =>", "ACCEPTED" if r.accepted else f"REJECTED ({r.reason})")


def report():
    for app, dfa in ((a, d) for a, d in (v for v in APPS.values())):
        print(f"\n=== {app.upper()} ({dfa.name}) ===")
        for kind in ("accept", "reject"):
            for s in CASES[app][kind]:
                ok = dfa.accepts(s)
                flag = "PASS" if ok == (kind == "accept") else "FAIL"
                print(f"  [{flag}] {kind:6} {s!r:28} -> {'ACCEPT' if ok else 'REJECT'}")


def menu():
    while True:
        print("\n1) Password  2) Email  3) ATM PIN format  4) ATM attempts (type C/W)  q) quit")
        c = input("choose: ").strip()
        if c == "q":
            return
        if c in APPS:
            name, dfa = APPS[c]
            text = input(f"enter {name} input: ")
            show(dfa, text)
            if name == "password" and dfa.accepts(text):
                print("   semantic issues:", semantic_issues(text) or "none")
            if name == "atm_pin" and dfa.accepts(text):
                print("   weak-PIN check :", weak_pin_reasons(text) or "none")


if __name__ == "__main__":
    report() if "--report" in sys.argv else menu()
