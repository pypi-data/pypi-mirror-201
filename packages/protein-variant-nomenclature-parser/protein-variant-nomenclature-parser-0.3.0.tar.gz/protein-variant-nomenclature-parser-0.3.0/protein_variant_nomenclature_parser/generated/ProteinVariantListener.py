# Generated from ProteinVariant.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ProteinVariantParser import ProteinVariantParser
else:
    from ProteinVariantParser import ProteinVariantParser

# This class defines a complete listener for a parse tree produced by ProteinVariantParser.
class ProteinVariantListener(ParseTreeListener):

    # Enter a parse tree produced by ProteinVariantParser#gene.
    def enterGene(self, ctx:ProteinVariantParser.GeneContext):
        pass

    # Exit a parse tree produced by ProteinVariantParser#gene.
    def exitGene(self, ctx:ProteinVariantParser.GeneContext):
        pass


    # Enter a parse tree produced by ProteinVariantParser#mutation.
    def enterMutation(self, ctx:ProteinVariantParser.MutationContext):
        pass

    # Exit a parse tree produced by ProteinVariantParser#mutation.
    def exitMutation(self, ctx:ProteinVariantParser.MutationContext):
        pass


    # Enter a parse tree produced by ProteinVariantParser#number_or_range.
    def enterNumber_or_range(self, ctx:ProteinVariantParser.Number_or_rangeContext):
        pass

    # Exit a parse tree produced by ProteinVariantParser#number_or_range.
    def exitNumber_or_range(self, ctx:ProteinVariantParser.Number_or_rangeContext):
        pass


    # Enter a parse tree produced by ProteinVariantParser#amino_acid_or_stop.
    def enterAmino_acid_or_stop(self, ctx:ProteinVariantParser.Amino_acid_or_stopContext):
        pass

    # Exit a parse tree produced by ProteinVariantParser#amino_acid_or_stop.
    def exitAmino_acid_or_stop(self, ctx:ProteinVariantParser.Amino_acid_or_stopContext):
        pass


    # Enter a parse tree produced by ProteinVariantParser#number.
    def enterNumber(self, ctx:ProteinVariantParser.NumberContext):
        pass

    # Exit a parse tree produced by ProteinVariantParser#number.
    def exitNumber(self, ctx:ProteinVariantParser.NumberContext):
        pass



del ProteinVariantParser