"""WFST-based Inverse Text Normalization (ITN) for Russian.

Public API::

    from rus import normalize

    normalize("двадцать две тысячи сто один")  # "22101"

Grammar construction is deferred until the first call, so importing
this package is cheap.
"""

__version__ = "0.1.9"

__all__ = ["normalize", "InverseNormalizer", "__version__"]


def __getattr__(name):
    # Lazy re-export: building the grammars takes seconds, so avoid it
    # unless the caller actually needs the normalizer.
    if name in ("normalize", "InverseNormalizer"):
        from rus import wfst

        return getattr(wfst, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
