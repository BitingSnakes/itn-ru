import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_DIGIT, GraphFst
from rus.taggers.cardinal import CardinalFst


class TelephoneFst(GraphFst):
    """
    Finite state transducer for classifying Russian telephone numbers as
    dictated to ASR. Accepts the country prefix («плюс семь» -> +7) or
    the trunk «восемь» -> 8, followed by ten more digits spoken as any mix of
    single digits, teens, tens,
    tens-plus-digit and hundreds groups, e.g.

        восемь девятьсот двенадцать триста сорок пять шестьдесят семь восемьдесят девять
            -> telephone { number: "89123456789" }
        плюс семь девятьсот двенадцать триста сорок пять шестьдесят семь восемьдесят девять
            -> telephone { number: "+79123456789" }

    ASR punctuation between groups (commas) is consumed. The total length is
    constrained to the Russian format (prefix + exactly ten digits), which
    keeps ordinary numbers out of this class.

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="telephone", kind="classify")

        delete_space = pynutil.delete(" ")
        # ASR may punctuate between dictated groups: "восемь девятьсот двенадцать , триста ..."
        group_sep = delete_space + pynini.closure(pynutil.delete(",") + delete_space, 0, 1)

        zero = cardinal.graph_zero
        digit = cardinal.graph_digit
        teen = cardinal.graph_teen
        ties = cardinal.graph_ties
        hundred3 = cardinal.graph_hundred_component @ (NEMO_DIGIT**3)

        group = pynini.union(
            zero,
            digit,
            teen,
            ties + pynutil.insert("0"),  # сорок -> 40
            ties + delete_space + digit,  # сорок пять -> 45
            hundred3,  # сто двадцать три -> 123
        )

        prefix = pynini.union(
            pynini.cross("плюс семь", "+7"),
            pynini.cross("восемь", "8"),
            pynini.cross("ноль", "0"),
            pynini.cross("нуль", "0"),
        )

        number = prefix + pynini.closure(group_sep + group, 1)
        # Russian numbers: prefix followed by ten digits.
        shape = (pynini.accep("+7") | pynini.accep("8") | pynini.accep("0")) + NEMO_DIGIT**10
        number = (number @ shape).optimize()

        graph = pynutil.insert('number: "') + number + pynutil.insert('"')
        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()
