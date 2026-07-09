import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_CHAR, NEMO_DIGIT, NEMO_NON_BREAKING_SPACE, GraphFst
from rus.taggers.cardinal import CardinalFst
from rus.utils import get_abs_path

# spoken keyword forms -> abbreviation
KEYWORDS = [
    ("ст.", ["статья", "статьи", "статью", "статьей", "статьёй"]),
    ("ч.", ["часть", "части", "частью"]),
    ("п.", ["пункт", "пункта", "пункту", "пункте", "пунктом"]),
    ("пп.", ["подпункт", "подпункта", "подпункту", "подпункте", "подпунктом"]),
    ("с.", ["страница", "страницы", "странице", "страницу", "страницей"]),
    ("разд.", ["раздел", "раздела", "разделу", "разделе", "разделом"]),
    ("гл.", ["глава", "главы", "главе", "главу", "главой"]),
    ("абз.", ["абзац", "абзаца", "абзацу", "абзаце", "абзацем"]),
    ("§", ["параграф", "параграфа", "параграфу", "параграфе", "параграфом"]),
]


class LegalFst(GraphFst):
    """
    Finite state transducer for legal and document references, e.g.
        статья пятая часть вторая -> word { name: "ст. 5 ч. 2" }
        страница сто двадцать -> word { name: "с. 120" }
        параграф третий -> word { name: "§ 3" }

    The keyword licenses single-digit ordinals/cardinals. Consecutive
    references chain into one token.

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="legal", kind="classify")

        delete_space = pynutil.delete(" ")
        nbsp = pynutil.insert(NEMO_NON_BREAKING_SPACE)
        strip_suffix = pynini.closure(NEMO_DIGIT) + pynutil.delete(pynini.union("-") + pynini.closure(NEMO_CHAR))

        def load_ordinal(name):
            return pynini.invert(pynini.string_file(get_abs_path(f"data/numbers/ordinal/{name}.tsv"))) @ strip_suffix

        ordinal = pynini.union(
            load_ordinal("ordinal_digit"),
            load_ordinal("ordinal_teen"),
            load_ordinal("ordinal_ties"),
            cardinal.graph_ties + delete_space + load_ordinal("ordinal_digit"),
        )
        number = ordinal | cardinal.graph | cardinal.graph_digit

        keyword = pynini.union(*(pynini.cross(pynini.union(*spoken), abbr) for abbr, spoken in KEYWORDS))

        item = keyword + nbsp + delete_space + number
        graph = item + pynini.closure(nbsp + delete_space + item)
        graph = pynutil.insert('word { name: "') + graph + pynutil.insert('" }')
        self.fst = graph.optimize()
