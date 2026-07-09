import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_NON_BREAKING_SPACE, GraphFst
from rus.taggers.cardinal import CardinalFst


class ScoreFst(GraphFst):
    """
    Finite state transducer for sports scores, gated on «счет», e.g.
        счет два один -> word { name: "счет 2:1" }
        с счетом три ноль -> с word { name: "счетом 3:0" }

    Bare digit pairs («два один») never match — the keyword is required.

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="score", kind="classify")

        keyword = pynini.union("счет", "счёт", "счета", "счету", "счёту", "счетом", "счётом")
        number = cardinal.graph_zero | cardinal.graph_digit | cardinal.graph_teen | cardinal.graph

        graph = keyword + pynini.cross(" ", NEMO_NON_BREAKING_SPACE) + number + pynini.cross(" ", ":") + number
        graph = pynutil.insert('word { name: "') + graph + pynutil.insert('" }')
        self.fst = graph.optimize()
