"""Minimal DFA engine used by every validator in this project.

A DFA is the 5-tuple (Q, Sigma, delta, q0, F).
Here Sigma is a set of *symbol classes* (e.g. 'L' = letter, 'D' = digit);
`classify` maps a raw character to its class. Any missing transition goes to
the implicit dead (trap) state DEAD, which never accepts.
"""
from collections import defaultdict
from dataclasses import dataclass, field

DEAD = "DEAD"


@dataclass
class Result:
    accepted: bool
    final_state: str
    trace: list = field(default_factory=list)  # (char, symbol, from_state, to_state)
    reason: str = ""


class DFA:
    def __init__(self, name, states, start, accepting, delta, classify):
        self.name = name
        self.states = list(states)
        self.start = start
        self.accepting = set(accepting)
        self.delta = delta          # {(state, symbol_class): next_state}
        self.classify = classify

    def run(self, text):
        state, trace = self.start, []
        for i, ch in enumerate(text):
            sym = self.classify(ch)
            nxt = self.delta.get((state, sym), DEAD)
            trace.append((ch, sym, state, nxt))
            state = nxt
            if state == DEAD:
                return Result(False, DEAD, trace,
                              f"no transition for {ch!r} (class {sym}) at position {i}")
        ok = state in self.accepting
        return Result(ok, state, trace,
                      "" if ok else f"input ended in non-accepting state {state}")

    def accepts(self, text):
        return self.run(text).accepted

    def to_dot(self):
        """Graphviz DOT source. The dead state is omitted to keep diagrams readable."""
        out = [f'digraph "{self.name}" {{', "  rankdir=LR;", "  __start [shape=point];"]
        for s in self.states:
            shape = "doublecircle" if s in self.accepting else "circle"
            out.append(f'  "{s}" [shape={shape}];')
        out.append(f'  __start -> "{self.start}";')
        edges = defaultdict(list)
        for (src, sym), dst in self.delta.items():
            if dst != DEAD:
                edges[(src, dst)].append(sym)
        for (src, dst), syms in edges.items():
            out.append(f'  "{src}" -> "{dst}" [label="{",".join(sorted(syms))}"];')
        out.append("}")
        return "\n".join(out)

    def transition_table(self):
        syms = sorted({s for (_, s) in self.delta})
        rows = [["state"] + syms]
        for q in self.states:
            mark = ("->" if q == self.start else "  ") + ("*" if q in self.accepting else " ")
            rows.append([mark + q] + [self.delta.get((q, s), DEAD) for s in syms])
        return rows
