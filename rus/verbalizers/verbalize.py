from pynini.lib import pynutil

from rus.graph_utils import GraphFst
from rus.verbalizers.cardinal import CardinalFst
from rus.verbalizers.date import DateFst
from rus.verbalizers.decimal import DecimalFst
from rus.verbalizers.electronic import ElectronicFst
from rus.verbalizers.fraction import FractionFst
from rus.verbalizers.measure import MeasureFst
from rus.verbalizers.money import MoneyFst
from rus.verbalizers.ordinal import OrdinalFst
from rus.verbalizers.telephone import TelephoneFst
from rus.verbalizers.time import TimeFst
from rus.verbalizers.whitelist import WhitelistFst
from rus.verbalizers.word import WordFst


class VerbalizeFst(GraphFst):
    def __init__(self):
        super().__init__(name="verbalize", kind="verbalize")

        self.cardinal = CardinalFst()
        self.decimal = DecimalFst()
        self.ordinal = OrdinalFst()
        self.fraction = FractionFst()
        self.telephone = TelephoneFst()
        self.electronic = ElectronicFst()
        self.measure = MeasureFst(decimal=self.decimal, cardinal=self.cardinal)
        self.money = MoneyFst(decimal=self.decimal)
        self.date = DateFst()
        self.time = TimeFst()
        self.word = WordFst()
        self.whitelist = WhitelistFst()

        graph = (
            self.whitelist.fst
            | self.time.fst
            | self.date.fst
            | self.money.fst
            | self.measure.fst
            | self.ordinal.fst
            | self.fraction.fst
            | self.telephone.fst
            | self.electronic.fst
            | self.decimal.fst
            | self.cardinal.fst
        )
        graph |= pynutil.add_weight(self.word.fst, 100)

        self.fst = graph

    def as_json(self):
        graph = (
            self.whitelist.as_json()
            | self.money.as_json()
            | self.measure.as_json()
            | self.time.as_json()
            | self.date.as_json()
            | self.ordinal.as_json()
            | self.fraction.as_json()
            | self.telephone.as_json()
            | self.electronic.as_json()
            | self.decimal.as_json()
            | self.cardinal.as_json()
        )

        graph |= pynutil.add_weight(self.word.as_json(), 100)

        return graph
