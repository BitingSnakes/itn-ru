import pynini
from pynini.lib import pynutil

from rus.graph_utils import GraphFst
from rus.taggers.cardinal import CardinalFst
from rus.utils import get_abs_path

# Russian-to-Latin fallback romanization for dictated e-mail and URL parts.
TRANSLIT = [
    ("а", "a"),
    ("б", "b"),
    ("в", "v"),
    ("г", "g"),
    ("д", "d"),
    ("е", "e"),
    ("ё", "e"),
    ("ж", "zh"),
    ("з", "z"),
    ("и", "i"),
    ("й", "y"),
    ("к", "k"),
    ("л", "l"),
    ("м", "m"),
    ("н", "n"),
    ("о", "o"),
    ("п", "p"),
    ("р", "r"),
    ("с", "s"),
    ("т", "t"),
    ("у", "u"),
    ("ф", "f"),
    ("х", "kh"),
    ("ц", "ts"),
    ("ч", "ch"),
    ("ш", "sh"),
    ("щ", "shch"),
    ("ъ", ""),
    ("ы", "y"),
    ("э", "e"),
    ("ю", "yu"),
    ("я", "ya"),
    ("ь", ""),
]


class ElectronicFst(GraphFst):
    """
    Finite state transducer for classifying e-mail addresses and web
    addresses as dictated to ASR, e.g.
        иван точка петренко собака джимейл точка ком
            -> electronic { address: "ivan.petrenko@gmail.com" }
        ве ве ве точка пример точка уа
            -> electronic { address: "www.primer.ua" }

    Free-form words are romanized with the fallback table above; known
    providers («джимейл» -> gmail) and TLDs («ком» -> com, «юей» -> ua) come
    from data files. An e-mail requires «собака», a URL requires the
    «ве ве ве» prefix, so ordinary text never matches.

    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="electronic", kind="classify")

        delete_space = pynutil.delete(" ")

        translit = pynini.closure(pynini.union(*(pynini.cross(c, l) for c, l in TRANSLIT)), 1)
        provider = pynini.invert(pynini.string_file(get_abs_path("data/electronic/providers.tsv")))
        symbol = pynini.invert(pynini.string_file(get_abs_path("data/electronic/symbols.tsv")))
        tld = pynini.invert(pynini.string_file(get_abs_path("data/electronic/tlds.tsv")))

        number = pynini.union(
            cardinal.graph_zero,
            cardinal.graph_digit,
            cardinal.graph_teen,
            cardinal.graph_ties + pynutil.insert("0"),
            cardinal.graph_ties + delete_space + cardinal.graph_digit,
        )

        # transliteration is the fallback: known symbols, providers and TLDs
        # must win over romanizing the same spoken word letter-by-letter
        translit = pynutil.add_weight(translit, 1.0)

        word = provider | translit | number
        part = word + pynini.closure(delete_space + (symbol | word), 0)

        dot = delete_space + pynini.cross("точка", ".") + delete_space
        # a domain is either a known provider on its own (мейл ру -> mail.ru)
        # or dotted labels ending in at least one dot
        domain = provider | ((provider | translit) + pynini.closure(dot + (tld | translit), 1))

        email = part + delete_space + pynini.cross("собака", "@") + delete_space + domain

        www = pynini.cross(pynini.union("ве ве ве", "дабл ю дабл ю дабл ю"), "www")
        url = www + dot + domain

        graph = pynutil.insert('address: "') + (email | url) + pynutil.insert('"')
        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()
