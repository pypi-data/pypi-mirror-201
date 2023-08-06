from antlr4 import *
from dataclasses import dataclass
from typing import Optional

from protein_variant_nomenclature_parser.generated.ProteinVariantLexer import (
    ProteinVariantLexer,
)
from protein_variant_nomenclature_parser.generated.ProteinVariantParser import (
    ProteinVariantParser,
)
from protein_variant_nomenclature_parser.generated.ProteinVariantListener import (
    ProteinVariantListener,
)


@dataclass
class NumberOrRange:
    start: int
    end: Optional[int] = None


@dataclass
class ProteinVariant:
    gene: Optional[str]
    amino_acid_before: str
    number_or_range: NumberOrRange
    amino_acid_after: str


class InvalidProteinVariantError(Exception):
    pass


class ProteinVariantExtractListener(ProteinVariantListener):
    def __init__(self):
        self.result = []

    def exitGene(self, ctx):
        self.result.append(ctx.getText())

    def exitAmino_acid_or_stop(self, ctx):
        self.result.append(ctx.getText())

    def exitNumber_or_range(self, ctx):
        numbers = [int(number.getText()) for number in ctx.number()]

        self.result.append(numbers)


def parse_ProteinVariant_string(input_string):
    input_stream = InputStream(input_string)
    lexer = ProteinVariantLexer(input_stream)
    lexer.removeErrorListeners()
    token_stream = CommonTokenStream(lexer)
    parser = ProteinVariantParser(token_stream)
    parser.removeErrorListeners()
    tree = parser.mutation()

    if parser.getNumberOfSyntaxErrors() > 0:  # Check if there were any syntax errors
        raise InvalidProteinVariantError("Invalid ProteinVariant string")

    listener = ProteinVariantExtractListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.result


def parse(input_string):
    gene, ref, pos, alt = parse_ProteinVariant_string(input_string)
    return ProteinVariant(gene, ref, NumberOrRange(*pos), alt)
