"""Writes Graphviz .dot files to diagrams/ and renders PNGs if `dot` is installed
(sudo apt install graphviz / winget install graphviz)."""
import os, shutil, subprocess
from automata.password import build_password_dfa
from automata.email_validator import email_dfa
from automata.atm_pin import pin_format_dfa, session_dfa

os.makedirs("diagrams", exist_ok=True)
dfas = {
    # full 8-char/4-class policy has 144 states -> unreadable; draw the same construction on a small policy
    "password_small_min3_L_D": build_password_dfa(min_len=3, required=("L", "D")),
    "email": email_dfa, "atm_pin_format": pin_format_dfa, "atm_session": session_dfa,
}
for name, d in dfas.items():
    path = f"diagrams/{name}.dot"
    open(path, "w").write(d.to_dot())
    if shutil.which("dot"):
        subprocess.run(["dot", "-Tpng", path, "-o", f"diagrams/{name}.png"], check=True)
    print("wrote", path)
