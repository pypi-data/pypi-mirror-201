import re
from dataclasses import dataclass
from typing import Optional
import unicodedata
from protein_variant_nomenclature_parser import hugo


@dataclass
class NumberOrRange:
    start: int
    end: Optional[int] = None


@dataclass
class ProteinVariant:
    gene: Optional[str]
    ref: str
    position: NumberOrRange
    alt: str


def find_longest_prefix(s, prefixes=hugo.HUGO_GENE_NAMES):
    longest_prefix = ""
    for prefix in prefixes:
        if s.startswith(prefix) and len(prefix) > len(longest_prefix):
            longest_prefix = prefix
    return longest_prefix if longest_prefix else None


class InvalidProteinVariantError(Exception):
    pass


POSITION_AND_AA_REGEX = re.compile(
    "^([ARNDCQEGHILKMFPSTWYVUO*]+)([ \t])?(\d+)([-_]\d+)?([ \t>])?([ARNDCQEGHILKMFPSTWYVUO*]+)$"
)


def parse(input_string):
    input_string = input_string.strip()

    input_string = unicodedata.normalize("NFKC", input_string).upper()
    hugo_gene_name = find_longest_prefix(input_string.strip())

    if hugo_gene_name is None:
        raise InvalidProteinVariantError("No hugo gene name found")

    prefix_stripped_input = input_string[len(hugo_gene_name) :].strip()

    match = POSITION_AND_AA_REGEX.match(prefix_stripped_input)

    if not match:
        raise InvalidProteinVariantError("Invalid position/AA info")

    amino_acids_before = match.group(1)
    start = int(match.group(3))
    end = int(match.group(4)[1:]) if match.group(4) else None
    amino_acids_after = match.group(6)

    return ProteinVariant(
        hugo_gene_name,
        amino_acids_before,
        NumberOrRange(start=start, end=end),
        amino_acids_after,
    )
