import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_DIGIT, GraphFst
from rus.taggers.cardinal import CardinalFst


class IpFst(GraphFst):
    """
    Finite state transducer for IPv4 addresses, e.g.
        сто девяносто два точка сто шестьдесят восемь точка один точка один
            -> word { name: "192.168.1.1" }

    Exactly four dotted groups are required, so version numbers and ordinary
    «точка» mentions never match.

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="ip", kind="classify")

        group = pynini.union(
            cardinal.graph_zero,
            cardinal.graph_digit,
            cardinal.graph_teen,
            cardinal.graph,
        ) @ pynini.closure(NEMO_DIGIT, 1, 3)

        dot_group = pynini.cross(" точка ", ".") + group
        graph = group + dot_group**3

        graph = pynutil.insert('word { name: "') + graph + pynutil.insert('" }')
        self.fst = graph.optimize()
