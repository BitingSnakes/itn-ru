from collections import defaultdict

import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_DIGIT, GraphFst, delete_space
from rus.taggers.cardinal import CardinalFst
from rus.utils import get_abs_path, load_labels


def prepare_labels_for_insertion(file_path: str) -> dict:
    labels = load_labels(file_path)
    mapping = defaultdict(list)
    for k, v in labels:
        mapping[k].append(v)

    for k in mapping:
        mapping[k] = pynini.union(*mapping[k]).optimize()
    return mapping


class DecimalFst(GraphFst):
    def __init__(
        self,
        cardinal: CardinalFst,
    ):
        super().__init__(name="decimal", kind="classify")

        delimiter = pynini.string_file(get_abs_path("data/numbers/decimal_delimiter.tsv"))

        delimiter = pynini.cross(delimiter, " ") + pynini.closure(delete_space + pynutil.delete("и"), 0, 1)
        delimiter |= pynini.closure(delete_space + pynini.cross("и", " "), 1, 1)

        decimal_endings_map = prepare_labels_for_insertion(get_abs_path("data/numbers/decimal_endings.tsv"))

        tenth_labels = pynutil.delete(decimal_endings_map["10"])
        tenth = cardinal.graph @ NEMO_DIGIT + delete_space + tenth_labels

        hundreds_labels = pynutil.delete(decimal_endings_map["100"])
        hundreds = cardinal.graph @ (NEMO_DIGIT + NEMO_DIGIT) + delete_space + hundreds_labels
        hundreds |= cardinal.graph @ (pynutil.insert("0") + NEMO_DIGIT) + delete_space + hundreds_labels

        thousands_labels = pynutil.delete(decimal_endings_map["1000"])
        thousands = cardinal.graph @ (NEMO_DIGIT + NEMO_DIGIT + NEMO_DIGIT) + delete_space + thousands_labels
        thousands |= cardinal.graph @ (pynutil.insert("0") + NEMO_DIGIT + NEMO_DIGIT) + delete_space + thousands_labels
        thousands |= cardinal.graph @ (pynutil.insert("0") + pynutil.insert("0") + NEMO_DIGIT) + delete_space + thousands_labels

        graph_fractional_part = pynini.union(tenth, hundreds, thousands).optimize()

        graph_integer = cardinal.graph_integer

        billion = pynini.string_file(get_abs_path("data/numbers/cardinals_billion.tsv"))
        million = pynini.string_file(get_abs_path("data/numbers/cardinals_million.tsv"))

        quantity = pynutil.insert(' quantity: "') + (billion | million) + pynutil.insert('"')
        optional_graph_quantity = pynini.closure(" " + quantity, 0, 1)

        graph_fractional = pynutil.insert('fractional_part: "') + graph_fractional_part + pynutil.insert('"')

        self.graph = graph_integer + delete_space + delimiter + delete_space + graph_fractional + optional_graph_quantity
        self.graph |= graph_integer + delete_space + quantity
        only_fractional = pynutil.insert('integer_part: "0" fractional_part: "') + (tenth | hundreds | thousands) + pynutil.insert('"')
        # Standalone thousandths overlap with the ordinal-thousand grammar;
        # prefer the decimal reading, as for tenths and hundredths.
        self.graph |= pynutil.add_weight(only_fractional, -0.01)

        optional_minus_graph = pynini.closure(pynutil.insert('negative: "true" ') + pynutil.delete("минус"), 0, 1)

        final_graph = optional_minus_graph + self.graph
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
