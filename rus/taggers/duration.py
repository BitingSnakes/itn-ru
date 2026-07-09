import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_NON_BREAKING_SPACE, GraphFst
from rus.taggers.cardinal import CardinalFst
from rus.utils import get_abs_path


class DurationFst(GraphFst):
    """
    Finite state transducer for durations and half-quantities, e.g.
        два часа тридцать минут -> word { name: "2 ч 30 мин" }
        сорок минут -> word { name: "40 мин" }
        полтора часа -> word { name: "1.5 ч" }
        пол килограмма / полчаса -> word { name: "0.5 кг" / "0.5 ч" }

    Time-of-day uses ordinal hours («сьома година»), durations use cardinals
    («два часа»), so the two grammars do not overlap. Standalone durations
    require a multi-digit number (single digits keep the words, protecting
    idioms like «пять минут двенадцатого»); compounds may use any digit.

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="duration", kind="classify")

        nbsp = pynini.cross(" ", NEMO_NON_BREAKING_SPACE)

        number_any = cardinal.graph | cardinal.graph_digit
        number_multi = cardinal.graph

        hour_u = pynini.cross(pynini.union("час", "часа", "часов"), "ч")
        minute_u = pynini.cross(pynini.union("минута", "минуты", "минут", "минуту"), "мин")
        second_u = pynini.cross(pynini.union("секунда", "секунды", "секунд", "секунду"), "с")

        def part(number, unit):
            return number + nbsp + unit

        compound = pynini.union(
            part(number_any, hour_u) + nbsp + part(number_any, minute_u) + pynini.closure(nbsp + part(number_any, second_u), 0, 1),
            part(number_any, minute_u) + nbsp + part(number_any, second_u),
        )
        standalone = part(number_multi, hour_u | minute_u | second_u)

        # пол / полтора / полторы + any known unit (measure or duration)
        measure_unit = pynini.invert(pynini.string_file(get_abs_path("data/measurements.tsv")))
        any_unit = measure_unit | hour_u | minute_u | second_u
        half = pynini.cross(pynini.union("полтора", "полторы"), "1.5") + nbsp + any_unit
        half |= pynini.cross("пол", "0.5") + nbsp + any_unit
        # one-word forms: полчаса, полкилограмма, ...
        half |= pynini.cross("пол", "0.5") + pynutil.insert(NEMO_NON_BREAKING_SPACE) + any_unit

        graph = compound | standalone | half
        graph = pynutil.insert('word { name: "') + graph + pynutil.insert('" }')
        self.fst = graph.optimize()
