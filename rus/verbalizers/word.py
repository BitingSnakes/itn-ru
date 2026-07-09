import pynini
from pynini.lib import pynutil

from rus.graph_utils import NEMO_CHAR, NEMO_SIGMA, GraphFst, delete_space


class WordFst(GraphFst):
    """
    Finite state transducer for verbalizing plain tokens
        e.g. tokens { name: "sleep" } -> sleep
    """

    def __init__(self):
        super().__init__(name="word", kind="verbalize")
        chars = pynini.closure(NEMO_CHAR - " ", 1)
        char = pynutil.delete("name:") + delete_space + pynutil.delete('"') + chars + pynutil.delete('"')
        graph = char @ pynini.cdrewrite(pynini.cross("\u00a0", " "), "", "", NEMO_SIGMA)

        graph = self.delete_tokens(graph)
        self.fst = graph.optimize()

        # Quotes, backslashes, and control characters are valid input token
        # content but must be escaped inside a JSON string.
        control_chars = pynini.union(*(chr(codepoint) for codepoint in range(0x20)))
        escaped_control = pynini.union(
            *(pynini.cross(chr(codepoint), f"\\u{codepoint:04x}") for codepoint in range(0x20))
        )
        json_char = pynini.union(
            pynini.cross('"', '\\"'),
            # Pynini parses backslash escapes in string literals, so four
            # output backslashes are required here to emit the JSON pair ``\\``.
            pynini.cross('\\', '\\\\\\\\'),
            escaped_control,
            pynini.difference(NEMO_CHAR, pynini.union(" ", '"', '\\', control_chars)),
        )
        json_chars = pynini.closure(json_char, 1)
        json_value = pynutil.delete("name:") + delete_space + pynutil.delete('"') + json_chars + pynutil.delete('"')
        self._json_fst = self.delete_tokens(json_value).optimize()

    def as_json(self):
        """Serializes a plain token as a valid JSON object."""
        return pynutil.insert('{"word": "') + self._json_fst + pynutil.insert('"}')
