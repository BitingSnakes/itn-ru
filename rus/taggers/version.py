import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_NON_BREAKING_SPACE, GraphFst
from rus.taggers.cardinal import CardinalFst


class VersionFst(GraphFst):
    """
    Finite state transducer for version numbers, gated on «версия», e.g.
        версия два точка пять -> word { name: "версия 2.5" }
        версии три точка десять точка один -> word { name: "версии 3.10.1" }
        версия пять -> word { name: "версия 5" }

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="version", kind="classify")

        keyword = pynini.union("версия", "версии", "версию", "версией")
        number = pynini.union(
            cardinal.graph_zero,
            cardinal.graph_digit,
            cardinal.graph_teen,
            cardinal.graph,
        )

        graph = keyword + pynini.cross(" ", NEMO_NON_BREAKING_SPACE) + number + pynini.closure(pynini.cross(" точка ", ".") + number)
        graph = pynutil.insert('word { name: "') + graph + pynutil.insert('" }')
        self.fst = graph.optimize()
