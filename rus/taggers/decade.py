import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_NON_BREAKING_SPACE, GraphFst

# decade forms, case-aligned with the appropriate «годы» form
DECADES = [
    ("20", "двадцат"),
    ("30", "тридцат"),
    ("50", "пятидесят"),
    ("60", "шестидесят"),
    ("70", "семидесят"),
    ("80", "восьмидесят"),
]
SUFFIXES = [("ые", "-е"), ("ых", "-х"), ("ым", "-м"), ("ыми", "-ми")]
# stems with non-standard endings
IRREGULAR = [
    ("40-е", "сороковые"),
    ("40-х", "сороковых"),
    ("40-м", "сороковым"),
    ("40-ми", "сороковыми"),
    ("90-е", "девяностые"),
    ("90-х", "девяностых"),
    ("90-м", "девяностым"),
    ("90-ми", "девяностыми"),
]


class DecadeFst(GraphFst):
    """
    Finite state transducer for decades, e.g.
        девяностые годы -> word { name: "90-е годы" }
        в восьмидесятых годах -> в word { name: "80-х годах" }

    The «годы» word is required, so other uses of decade words
    and other uses are unaffected.
    """

    def __init__(self):
        super().__init__(name="decade", kind="classify")

        pairs = list(IRREGULAR)
        for digits, stem in DECADES:
            for spoken_suf, written_suf in SUFFIXES:
                pairs.append((digits + written_suf, stem + spoken_suf))

        decade = pynini.union(*(pynini.cross(s, w) for w, s in pairs))
        roky = pynini.union("годы", "годов", "годам", "годами", "годах")

        graph = decade + pynini.cross(" ", NEMO_NON_BREAKING_SPACE) + roky
        graph = pynutil.insert('word { name: "') + graph + pynutil.insert('" }')
        self.fst = graph.optimize()
