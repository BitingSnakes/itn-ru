import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_CHAR, NEMO_DIGIT, NEMO_NON_BREAKING_SPACE, GraphFst
from rus.taggers.cardinal import CardinalFst
from rus.utils import get_abs_path


class RangeFst(GraphFst):
    """
    Finite state transducer for numeric, time and date ranges, e.g.
        от пяти до десяти процентов -> name: "5–10 %"
        от ста до двухсот километров -> name: "100–200 км"
        два-три часа -> name: "2–3 ч"
        с девятого до восемнадцатого часа -> name: "с 09:00 до 18:00"
        с первого по пятое января -> name: "с 1 по 5 января"

    Numeric ranges support «от/с A до/по B [unit]» and a hyphenated
    approximation «A-B [unit]». Time ranges require the «час» word and
    date ranges require a month name; the trailing anchor is what keeps
    phrases like «с первой по пятую попытку» out of this class. Time-of-day
    grammar owns «час» phrases; the duration units («ч», «мин») are only
    recognised inside a range, where the meaning is unambiguous.

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="range", kind="classify")

        delete_space = pynutil.delete(" ")

        number = cardinal.graph | cardinal.graph_digit

        unit = pynini.invert(pynini.string_file(get_abs_path("data/measurements.tsv")))
        duration = pynini.union(
            pynini.cross(pynini.union("час", "часа", "часов"), "ч"),
            pynini.cross(pynini.union("минута", "минуты", "минут", "минуту"), "мин"),
        )
        unit |= duration
        optional_unit = pynini.closure(pynini.cross(" ", NEMO_NON_BREAKING_SPACE) + unit, 0, 1)

        dash = pynutil.insert("–")

        # от/с A до/по B
        prefixed = (
            pynutil.delete(pynini.union("от", "с"))
            + delete_space
            + number
            + delete_space
            + pynutil.delete(pynini.union("до", "по"))
            + dash
            + delete_space
            + number
        )
        # hyphenated approximation: два-три
        hyphenated = number + pynini.cross("-", "–") + number

        numeric = (prefixed | hyphenated) + optional_unit

        # --- time and date ranges (ordinal-based) ---
        strip_suffix = pynini.closure(NEMO_DIGIT) + pynutil.delete(pynini.union("-") + pynini.closure(NEMO_CHAR))

        def load_ordinal(name):
            return pynini.invert(pynini.string_file(get_abs_path(f"data/numbers/ordinal/{name}.tsv"))) @ strip_suffix

        ordinal = pynini.union(
            load_ordinal("ordinal_digit"),
            load_ordinal("ordinal_teen"),
            load_ordinal("ordinal_ties"),
            cardinal.graph_ties + delete_space + load_ordinal("ordinal_digit"),
        )

        # с девятого до восемнадцатого часа -> с 09:00 до 18:00
        pad = (NEMO_DIGIT + NEMO_DIGIT) | (pynutil.insert("0") + NEMO_DIGIT)
        hour = (ordinal @ pad) + pynutil.insert(":00")
        nbsp = pynini.cross(" ", NEMO_NON_BREAKING_SPACE)
        time_range = (
            pynini.union("с", "от") + nbsp + hour + nbsp + pynini.union("до", "по") + nbsp + hour + pynutil.delete(pynini.union(" часа", " часов", " час"))
        )

        # с первого по пятое января -> с 1 по 5 января
        month = pynini.string_file(get_abs_path("data/month.tsv"))
        date_range = pynini.union("с", "от") + nbsp + ordinal + nbsp + pynini.union("до", "по") + nbsp + ordinal + nbsp + month

        graph = numeric | time_range | date_range
        graph = pynutil.insert('word { name: "') + graph + pynutil.insert('" }')
        # emitted as a `word` token so the existing word verbalizer handles it
        self.fst = graph.optimize()
