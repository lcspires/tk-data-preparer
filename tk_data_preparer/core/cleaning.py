"""
Core text-cleaning utilities for tk_data_preparer.

Design goals (academic, not marketing):
- Pure, GUI-agnostic functions operating on pandas objects.
- Robust handling of missing values (NaN/<NA>) without converting them to the
  string "nan".
- Unicode-aware whitespace normalization with optional Unicode normalization
  (NFKC by default) and optional case folding.
- Metrics returned alongside transformed DataFrames to enable instrumentation
  in the UI layer (e.g., how many whitespace characters were removed).

Notes
-----
* We operate column-wise and prefer vectorized ops (`.str`) when possible.
* We do NOT modify the input DataFrame in-place.
* We detect textual columns using pandas dtypes ("string" / object) instead of
  brittle `dtype == object` checks.

Public API
----------
- CleanConfig: configuration dataclass with sensible defaults.
- clean_columns(df, columns=None, config=...):
    Clean specified columns (or auto-detected textual columns) and return
    (df_clean, metrics_dict).

Returned metrics include:
    {
        "total_whitespace_removed": int,
        "per_column_whitespace_removed": Dict[str, int],
        "cells_modified": int,
        "empty_strings_to_na": int,
        "columns_processed": List[str],
    }

This module intentionally stays independent from any GUI/toolkit concerns.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Literal
import re
import unicodedata

import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype, is_object_dtype

__all__ = [
    "CleanConfig",
    "clean_columns",
]


# --- Configuration -----------------------------------------------------------------

# Regex that captures a wide range of whitespace characters, not just ASCII space.
# `\s` in Python regex is already Unicode-aware, but we keep it explicit
# in one place for potential future tightening/loosening.
WS_CHAR_PATTERN = r"\s"
WS_SEQUENCE_PATTERN = r"\s+"
TRIM_PATTERN = r"^\s+|\s+$"


@dataclass(frozen=True)
class CleanConfig:
    """Configuration for text cleaning.

    Parameters
    ----------
    strip : bool
        Remove leading/trailing whitespace.
    collapse_whitespace : bool
        Collapse internal runs of whitespace to a single ASCII space.
    unicode_normalization : {"NFC", "NFKC", "NFD", "NFKD", None}
        Apply Unicode normalization; default NFKC (compatibility composition).
    case : {"lower", "upper", None}
        Optional case transform.
    transliterate_ascii : bool
        If True, attempt a simple ASCII transliteration by removing combining
        marks after NFKD decomposition. This is intentionally minimal.
    coerce_non_strings : bool
        If True, non-textual columns selected will be coerced to pandas
        "string" dtype and cleaned; else they are left untouched.
    empty_to_na : bool
        Convert empty strings (after cleaning) to <NA>.
    """

    strip: bool = True
    collapse_whitespace: bool = True
    unicode_normalization: Optional[Literal["NFC", "NFKC", "NFD", "NFKD"]] = "NFKC"
    case: Optional[Literal["lower", "upper"]] = None
    transliterate_ascii: bool = False
    coerce_non_strings: bool = False
    empty_to_na: bool = True


# --- Helpers -----------------------------------------------------------------------

def _is_textual_dtype(dtype) -> bool:
    """Return True if dtype is textual (pandas string dtype or object).

    We avoid brittle equality checks; `is_string_dtype` covers both pandas
    "string" extension types and object arrays of strings. We also accept
    object dtype as textual, because many CSVs land there by default.
    """
    return is_string_dtype(dtype) or is_object_dtype(dtype)


def _normalize_unicode(series: pd.Series, form: Optional[str]) -> pd.Series:
    if not form:
        return series
    # Use map with a safe function; pandas string ops don't expose Unicode
    # normalize directly.
    def _norm(x):
        if pd.isna(x):
            return x
        try:
            return unicodedata.normalize(form, str(x))
        except Exception:
            return str(x)
    return series.map(_norm)


def _transliterate_ascii(series: pd.Series) -> pd.Series:
    """Best-effort ASCII transliteration by dropping combining marks after NFKD.
    Not locale-aware; intended only for rough normalization.
    """
    def _trans(x):
        if pd.isna(x):
            return x
        # Decompose then strip combining marks; keep only ASCII range
        decomp = unicodedata.normalize("NFKD", str(x))
        base = "".join(ch for ch in decomp if not unicodedata.combining(ch))
        return base.encode("ascii", "ignore").decode("ascii")
    return series.map(_trans)


def _count_whitespace_chars(series: pd.Series) -> pd.Series:
    """Count whitespace characters per cell using a Unicode-aware regex.

    Returns a Series of integer counts with NA filled as 0.
    """
    counts = series.str.count(WS_CHAR_PATTERN)
    return counts.fillna(0).astype(int)


def _ensure_string_dtype(series: pd.Series) -> pd.Series:
    """Return a pandas "string" dtype Series preserving missing values.

    Unlike `.astype(str)`, this does not convert NaN to the literal "nan".
    """
    # Prefer pandas StringDtype; fallback to object if unavailable.
    try:
        return series.astype("string")
    except Exception:
        # Last resort: object but keep NaN as np.nan
        return series.astype(object)


# --- Public API --------------------------------------------------------------------

def clean_columns(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    *,
    config: Optional[CleanConfig] = None,
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Clean textual columns of a DataFrame according to `config`.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame. Will NOT be modified in-place.
    columns : sequence of str, optional
        Columns to clean. If None, textual columns are auto-detected.
    config : CleanConfig, optional
        Cleaning configuration. Defaults are sensible for common CSV/Excel data.

    Returns
    -------
    df_clean : DataFrame
        A copy of `df` with cleaned columns.
    metrics : dict
        Instrumentation of the cleaning process with keys:
            - total_whitespace_removed : int
            - per_column_whitespace_removed : Dict[str, int]
            - cells_modified : int
            - empty_strings_to_na : int
            - columns_processed : List[str]

    Notes
    -----
    * "Whitespace removed" counts the difference in number of whitespace code
      points before vs. after applying collapse+strip. It purposely ignores
      changes due to Unicode normalization or case transforms.
    * Missing values are preserved (<NA>/NaN) and are not turned into strings.
    """
    if config is None:
        config = CleanConfig()

    if columns is None:
        # Auto-detect textual columns
        columns = [c for c in df.columns if _is_textual_dtype(df[c].dtype)]

    # Prepare output df
    out = df.copy(deep=True)

    per_col_ws_removed: Dict[str, int] = {}
    cells_modified_total = 0
    empty_to_na_total = 0

    for col in columns:
        if col not in out.columns:
            # Skip silently; higher layer can decide whether to warn.
            continue

        s = out[col]
        is_textual = _is_textual_dtype(s.dtype)
        if not is_textual and not config.coerce_non_strings:
            continue

        s0 = _ensure_string_dtype(s)

        # Count whitespace before cleaning (Unicode-aware)
        ws_before = _count_whitespace_chars(s0)

        # Apply whitespace transforms first to compute accurate removal counts
        s1 = s0
        if config.collapse_whitespace:
            s1 = s1.str.replace(WS_SEQUENCE_PATTERN, " ", regex=True)
        if config.strip:
            s1 = s1.str.replace(TRIM_PATTERN, "", regex=True)

        # Count whitespace after whitespace-focused transforms
        ws_after = _count_whitespace_chars(s1)
        per_col_ws_removed[col] = int((ws_before - ws_after).sum())

        # Apply Unicode normalization, case, and optional transliteration
        s2 = s1
        s2 = _normalize_unicode(s2, config.unicode_normalization)
        if config.transliterate_ascii:
            s2 = _transliterate_ascii(s2)
        if config.case == "lower":
            s2 = s2.str.lower()
        elif config.case == "upper":
            s2 = s2.str.upper()

        # Convert empty strings to <NA> if requested
        if config.empty_to_na:
            empties = s2.fillna("").str.len() == 0
            empty_to_na_total += int(empties.sum())
            # Replace only empties, preserve existing NA as NA
            s2 = s2.mask(empties, other=pd.NA)

        # Cells modified (exclude NA vs NA comparisons)
        changed_mask = s2.ne(s0)
        changed_mask = changed_mask & ~(s2.isna() & s0.isna())
        cells_modified_total += int(changed_mask.sum())

        out[col] = s2

    metrics: Dict[str, object] = {
        "total_whitespace_removed": int(sum(per_col_ws_removed.values())),
        "per_column_whitespace_removed": per_col_ws_removed,
        "cells_modified": cells_modified_total,
        "empty_strings_to_na": empty_to_na_total,
        "columns_processed": list(columns),
    }

    return out, metrics
