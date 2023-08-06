# Generated from ProteinVariant.g4 by ANTLR 4.12.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,7,36,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,3,0,13,
        8,0,1,0,1,0,3,0,17,8,0,1,0,1,0,3,0,21,8,0,1,0,1,0,1,1,1,1,1,2,1,
        2,1,2,3,2,30,8,2,1,3,1,3,1,4,1,4,1,4,0,0,5,0,2,4,6,8,0,2,1,0,1,2,
        1,0,5,6,34,0,10,1,0,0,0,2,24,1,0,0,0,4,26,1,0,0,0,6,31,1,0,0,0,8,
        33,1,0,0,0,10,12,3,2,1,0,11,13,5,3,0,0,12,11,1,0,0,0,12,13,1,0,0,
        0,13,14,1,0,0,0,14,16,3,6,3,0,15,17,5,3,0,0,16,15,1,0,0,0,16,17,
        1,0,0,0,17,18,1,0,0,0,18,20,3,4,2,0,19,21,5,3,0,0,20,19,1,0,0,0,
        20,21,1,0,0,0,21,22,1,0,0,0,22,23,3,6,3,0,23,1,1,0,0,0,24,25,5,7,
        0,0,25,3,1,0,0,0,26,29,3,8,4,0,27,28,7,0,0,0,28,30,3,8,4,0,29,27,
        1,0,0,0,29,30,1,0,0,0,30,5,1,0,0,0,31,32,7,1,0,0,32,7,1,0,0,0,33,
        34,5,4,0,0,34,9,1,0,0,0,4,12,16,20,29
    ]

class ProteinVariantParser ( Parser ):

    grammarFileName = "ProteinVariant.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'-'", "'_'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'*'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "WS", "INT", 
                      "AMINO_ACID", "STOP_CODON", "GENE" ]

    RULE_mutation = 0
    RULE_gene = 1
    RULE_number_or_range = 2
    RULE_amino_acid_or_stop = 3
    RULE_number = 4

    ruleNames =  [ "mutation", "gene", "number_or_range", "amino_acid_or_stop", 
                   "number" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    WS=3
    INT=4
    AMINO_ACID=5
    STOP_CODON=6
    GENE=7

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class MutationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def gene(self):
            return self.getTypedRuleContext(ProteinVariantParser.GeneContext,0)


        def amino_acid_or_stop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProteinVariantParser.Amino_acid_or_stopContext)
            else:
                return self.getTypedRuleContext(ProteinVariantParser.Amino_acid_or_stopContext,i)


        def number_or_range(self):
            return self.getTypedRuleContext(ProteinVariantParser.Number_or_rangeContext,0)


        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(ProteinVariantParser.WS)
            else:
                return self.getToken(ProteinVariantParser.WS, i)

        def getRuleIndex(self):
            return ProteinVariantParser.RULE_mutation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMutation" ):
                listener.enterMutation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMutation" ):
                listener.exitMutation(self)




    def mutation(self):

        localctx = ProteinVariantParser.MutationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_mutation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.gene()
            self.state = 12
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 11
                self.match(ProteinVariantParser.WS)


            self.state = 14
            self.amino_acid_or_stop()
            self.state = 16
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 15
                self.match(ProteinVariantParser.WS)


            self.state = 18
            self.number_or_range()
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 19
                self.match(ProteinVariantParser.WS)


            self.state = 22
            self.amino_acid_or_stop()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GeneContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GENE(self):
            return self.getToken(ProteinVariantParser.GENE, 0)

        def getRuleIndex(self):
            return ProteinVariantParser.RULE_gene

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGene" ):
                listener.enterGene(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGene" ):
                listener.exitGene(self)




    def gene(self):

        localctx = ProteinVariantParser.GeneContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_gene)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(ProteinVariantParser.GENE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Number_or_rangeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ProteinVariantParser.NumberContext)
            else:
                return self.getTypedRuleContext(ProteinVariantParser.NumberContext,i)


        def getRuleIndex(self):
            return ProteinVariantParser.RULE_number_or_range

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber_or_range" ):
                listener.enterNumber_or_range(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber_or_range" ):
                listener.exitNumber_or_range(self)




    def number_or_range(self):

        localctx = ProteinVariantParser.Number_or_rangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_number_or_range)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26
            self.number()
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1 or _la==2:
                self.state = 27
                _la = self._input.LA(1)
                if not(_la==1 or _la==2):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 28
                self.number()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Amino_acid_or_stopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AMINO_ACID(self):
            return self.getToken(ProteinVariantParser.AMINO_ACID, 0)

        def STOP_CODON(self):
            return self.getToken(ProteinVariantParser.STOP_CODON, 0)

        def getRuleIndex(self):
            return ProteinVariantParser.RULE_amino_acid_or_stop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAmino_acid_or_stop" ):
                listener.enterAmino_acid_or_stop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAmino_acid_or_stop" ):
                listener.exitAmino_acid_or_stop(self)




    def amino_acid_or_stop(self):

        localctx = ProteinVariantParser.Amino_acid_or_stopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_amino_acid_or_stop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            _la = self._input.LA(1)
            if not(_la==5 or _la==6):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(ProteinVariantParser.INT, 0)

        def getRuleIndex(self):
            return ProteinVariantParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = ProteinVariantParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.match(ProteinVariantParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





