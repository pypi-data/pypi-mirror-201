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
        4,1,199,36,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,1,1,
        1,3,1,15,8,1,1,1,1,1,3,1,19,8,1,1,1,1,1,3,1,23,8,1,1,1,1,1,1,2,1,
        2,1,2,3,2,30,8,2,1,3,1,3,1,4,1,4,1,4,0,0,5,0,2,4,6,8,0,3,1,0,7,199,
        1,0,1,2,1,0,5,6,34,0,10,1,0,0,0,2,12,1,0,0,0,4,26,1,0,0,0,6,31,1,
        0,0,0,8,33,1,0,0,0,10,11,7,0,0,0,11,1,1,0,0,0,12,14,3,0,0,0,13,15,
        5,3,0,0,14,13,1,0,0,0,14,15,1,0,0,0,15,16,1,0,0,0,16,18,3,6,3,0,
        17,19,5,3,0,0,18,17,1,0,0,0,18,19,1,0,0,0,19,20,1,0,0,0,20,22,3,
        4,2,0,21,23,5,3,0,0,22,21,1,0,0,0,22,23,1,0,0,0,23,24,1,0,0,0,24,
        25,3,6,3,0,25,3,1,0,0,0,26,29,3,8,4,0,27,28,7,1,0,0,28,30,3,8,4,
        0,29,27,1,0,0,0,29,30,1,0,0,0,30,5,1,0,0,0,31,32,7,2,0,0,32,7,1,
        0,0,0,33,34,5,4,0,0,34,9,1,0,0,0,4,14,18,22,29
    ]

class ProteinVariantParser ( Parser ):

    grammarFileName = "ProteinVariant.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'-'", "'_'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'*'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "WS", "INT", 
                      "AMINO_ACID", "STOP_CODON", "GENE0", "GENE1", "GENE2", 
                      "GENE3", "GENE4", "GENE5", "GENE6", "GENE7", "GENE8", 
                      "GENE9", "GENE10", "GENE11", "GENE12", "GENE13", "GENE14", 
                      "GENE15", "GENE16", "GENE17", "GENE18", "GENE19", 
                      "GENE20", "GENE21", "GENE22", "GENE23", "GENE24", 
                      "GENE25", "GENE26", "GENE27", "GENE28", "GENE29", 
                      "GENE30", "GENE31", "GENE32", "GENE33", "GENE34", 
                      "GENE35", "GENE36", "GENE37", "GENE38", "GENE39", 
                      "GENE40", "GENE41", "GENE42", "GENE43", "GENE44", 
                      "GENE45", "GENE46", "GENE47", "GENE48", "GENE49", 
                      "GENE50", "GENE51", "GENE52", "GENE53", "GENE54", 
                      "GENE55", "GENE56", "GENE57", "GENE58", "GENE59", 
                      "GENE60", "GENE61", "GENE62", "GENE63", "GENE64", 
                      "GENE65", "GENE66", "GENE67", "GENE68", "GENE69", 
                      "GENE70", "GENE71", "GENE72", "GENE73", "GENE74", 
                      "GENE75", "GENE76", "GENE77", "GENE78", "GENE79", 
                      "GENE80", "GENE81", "GENE82", "GENE83", "GENE84", 
                      "GENE85", "GENE86", "GENE87", "GENE88", "GENE89", 
                      "GENE90", "GENE91", "GENE92", "GENE93", "GENE94", 
                      "GENE95", "GENE96", "GENE97", "GENE98", "GENE99", 
                      "GENE100", "GENE101", "GENE102", "GENE103", "GENE104", 
                      "GENE105", "GENE106", "GENE107", "GENE108", "GENE109", 
                      "GENE110", "GENE111", "GENE112", "GENE113", "GENE114", 
                      "GENE115", "GENE116", "GENE117", "GENE118", "GENE119", 
                      "GENE120", "GENE121", "GENE122", "GENE123", "GENE124", 
                      "GENE125", "GENE126", "GENE127", "GENE128", "GENE129", 
                      "GENE130", "GENE131", "GENE132", "GENE133", "GENE134", 
                      "GENE135", "GENE136", "GENE137", "GENE138", "GENE139", 
                      "GENE140", "GENE141", "GENE142", "GENE143", "GENE144", 
                      "GENE145", "GENE146", "GENE147", "GENE148", "GENE149", 
                      "GENE150", "GENE151", "GENE152", "GENE153", "GENE154", 
                      "GENE155", "GENE156", "GENE157", "GENE158", "GENE159", 
                      "GENE160", "GENE161", "GENE162", "GENE163", "GENE164", 
                      "GENE165", "GENE166", "GENE167", "GENE168", "GENE169", 
                      "GENE170", "GENE171", "GENE172", "GENE173", "GENE174", 
                      "GENE175", "GENE176", "GENE177", "GENE178", "GENE179", 
                      "GENE180", "GENE181", "GENE182", "GENE183", "GENE184", 
                      "GENE185", "GENE186", "GENE187", "GENE188", "GENE189", 
                      "GENE190", "GENE191", "GENE192" ]

    RULE_gene = 0
    RULE_mutation = 1
    RULE_number_or_range = 2
    RULE_amino_acid_or_stop = 3
    RULE_number = 4

    ruleNames =  [ "gene", "mutation", "number_or_range", "amino_acid_or_stop", 
                   "number" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    WS=3
    INT=4
    AMINO_ACID=5
    STOP_CODON=6
    GENE0=7
    GENE1=8
    GENE2=9
    GENE3=10
    GENE4=11
    GENE5=12
    GENE6=13
    GENE7=14
    GENE8=15
    GENE9=16
    GENE10=17
    GENE11=18
    GENE12=19
    GENE13=20
    GENE14=21
    GENE15=22
    GENE16=23
    GENE17=24
    GENE18=25
    GENE19=26
    GENE20=27
    GENE21=28
    GENE22=29
    GENE23=30
    GENE24=31
    GENE25=32
    GENE26=33
    GENE27=34
    GENE28=35
    GENE29=36
    GENE30=37
    GENE31=38
    GENE32=39
    GENE33=40
    GENE34=41
    GENE35=42
    GENE36=43
    GENE37=44
    GENE38=45
    GENE39=46
    GENE40=47
    GENE41=48
    GENE42=49
    GENE43=50
    GENE44=51
    GENE45=52
    GENE46=53
    GENE47=54
    GENE48=55
    GENE49=56
    GENE50=57
    GENE51=58
    GENE52=59
    GENE53=60
    GENE54=61
    GENE55=62
    GENE56=63
    GENE57=64
    GENE58=65
    GENE59=66
    GENE60=67
    GENE61=68
    GENE62=69
    GENE63=70
    GENE64=71
    GENE65=72
    GENE66=73
    GENE67=74
    GENE68=75
    GENE69=76
    GENE70=77
    GENE71=78
    GENE72=79
    GENE73=80
    GENE74=81
    GENE75=82
    GENE76=83
    GENE77=84
    GENE78=85
    GENE79=86
    GENE80=87
    GENE81=88
    GENE82=89
    GENE83=90
    GENE84=91
    GENE85=92
    GENE86=93
    GENE87=94
    GENE88=95
    GENE89=96
    GENE90=97
    GENE91=98
    GENE92=99
    GENE93=100
    GENE94=101
    GENE95=102
    GENE96=103
    GENE97=104
    GENE98=105
    GENE99=106
    GENE100=107
    GENE101=108
    GENE102=109
    GENE103=110
    GENE104=111
    GENE105=112
    GENE106=113
    GENE107=114
    GENE108=115
    GENE109=116
    GENE110=117
    GENE111=118
    GENE112=119
    GENE113=120
    GENE114=121
    GENE115=122
    GENE116=123
    GENE117=124
    GENE118=125
    GENE119=126
    GENE120=127
    GENE121=128
    GENE122=129
    GENE123=130
    GENE124=131
    GENE125=132
    GENE126=133
    GENE127=134
    GENE128=135
    GENE129=136
    GENE130=137
    GENE131=138
    GENE132=139
    GENE133=140
    GENE134=141
    GENE135=142
    GENE136=143
    GENE137=144
    GENE138=145
    GENE139=146
    GENE140=147
    GENE141=148
    GENE142=149
    GENE143=150
    GENE144=151
    GENE145=152
    GENE146=153
    GENE147=154
    GENE148=155
    GENE149=156
    GENE150=157
    GENE151=158
    GENE152=159
    GENE153=160
    GENE154=161
    GENE155=162
    GENE156=163
    GENE157=164
    GENE158=165
    GENE159=166
    GENE160=167
    GENE161=168
    GENE162=169
    GENE163=170
    GENE164=171
    GENE165=172
    GENE166=173
    GENE167=174
    GENE168=175
    GENE169=176
    GENE170=177
    GENE171=178
    GENE172=179
    GENE173=180
    GENE174=181
    GENE175=182
    GENE176=183
    GENE177=184
    GENE178=185
    GENE179=186
    GENE180=187
    GENE181=188
    GENE182=189
    GENE183=190
    GENE184=191
    GENE185=192
    GENE186=193
    GENE187=194
    GENE188=195
    GENE189=196
    GENE190=197
    GENE191=198
    GENE192=199

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class GeneContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GENE0(self):
            return self.getToken(ProteinVariantParser.GENE0, 0)

        def GENE1(self):
            return self.getToken(ProteinVariantParser.GENE1, 0)

        def GENE2(self):
            return self.getToken(ProteinVariantParser.GENE2, 0)

        def GENE3(self):
            return self.getToken(ProteinVariantParser.GENE3, 0)

        def GENE4(self):
            return self.getToken(ProteinVariantParser.GENE4, 0)

        def GENE5(self):
            return self.getToken(ProteinVariantParser.GENE5, 0)

        def GENE6(self):
            return self.getToken(ProteinVariantParser.GENE6, 0)

        def GENE7(self):
            return self.getToken(ProteinVariantParser.GENE7, 0)

        def GENE8(self):
            return self.getToken(ProteinVariantParser.GENE8, 0)

        def GENE9(self):
            return self.getToken(ProteinVariantParser.GENE9, 0)

        def GENE10(self):
            return self.getToken(ProteinVariantParser.GENE10, 0)

        def GENE11(self):
            return self.getToken(ProteinVariantParser.GENE11, 0)

        def GENE12(self):
            return self.getToken(ProteinVariantParser.GENE12, 0)

        def GENE13(self):
            return self.getToken(ProteinVariantParser.GENE13, 0)

        def GENE14(self):
            return self.getToken(ProteinVariantParser.GENE14, 0)

        def GENE15(self):
            return self.getToken(ProteinVariantParser.GENE15, 0)

        def GENE16(self):
            return self.getToken(ProteinVariantParser.GENE16, 0)

        def GENE17(self):
            return self.getToken(ProteinVariantParser.GENE17, 0)

        def GENE18(self):
            return self.getToken(ProteinVariantParser.GENE18, 0)

        def GENE19(self):
            return self.getToken(ProteinVariantParser.GENE19, 0)

        def GENE20(self):
            return self.getToken(ProteinVariantParser.GENE20, 0)

        def GENE21(self):
            return self.getToken(ProteinVariantParser.GENE21, 0)

        def GENE22(self):
            return self.getToken(ProteinVariantParser.GENE22, 0)

        def GENE23(self):
            return self.getToken(ProteinVariantParser.GENE23, 0)

        def GENE24(self):
            return self.getToken(ProteinVariantParser.GENE24, 0)

        def GENE25(self):
            return self.getToken(ProteinVariantParser.GENE25, 0)

        def GENE26(self):
            return self.getToken(ProteinVariantParser.GENE26, 0)

        def GENE27(self):
            return self.getToken(ProteinVariantParser.GENE27, 0)

        def GENE28(self):
            return self.getToken(ProteinVariantParser.GENE28, 0)

        def GENE29(self):
            return self.getToken(ProteinVariantParser.GENE29, 0)

        def GENE30(self):
            return self.getToken(ProteinVariantParser.GENE30, 0)

        def GENE31(self):
            return self.getToken(ProteinVariantParser.GENE31, 0)

        def GENE32(self):
            return self.getToken(ProteinVariantParser.GENE32, 0)

        def GENE33(self):
            return self.getToken(ProteinVariantParser.GENE33, 0)

        def GENE34(self):
            return self.getToken(ProteinVariantParser.GENE34, 0)

        def GENE35(self):
            return self.getToken(ProteinVariantParser.GENE35, 0)

        def GENE36(self):
            return self.getToken(ProteinVariantParser.GENE36, 0)

        def GENE37(self):
            return self.getToken(ProteinVariantParser.GENE37, 0)

        def GENE38(self):
            return self.getToken(ProteinVariantParser.GENE38, 0)

        def GENE39(self):
            return self.getToken(ProteinVariantParser.GENE39, 0)

        def GENE40(self):
            return self.getToken(ProteinVariantParser.GENE40, 0)

        def GENE41(self):
            return self.getToken(ProteinVariantParser.GENE41, 0)

        def GENE42(self):
            return self.getToken(ProteinVariantParser.GENE42, 0)

        def GENE43(self):
            return self.getToken(ProteinVariantParser.GENE43, 0)

        def GENE44(self):
            return self.getToken(ProteinVariantParser.GENE44, 0)

        def GENE45(self):
            return self.getToken(ProteinVariantParser.GENE45, 0)

        def GENE46(self):
            return self.getToken(ProteinVariantParser.GENE46, 0)

        def GENE47(self):
            return self.getToken(ProteinVariantParser.GENE47, 0)

        def GENE48(self):
            return self.getToken(ProteinVariantParser.GENE48, 0)

        def GENE49(self):
            return self.getToken(ProteinVariantParser.GENE49, 0)

        def GENE50(self):
            return self.getToken(ProteinVariantParser.GENE50, 0)

        def GENE51(self):
            return self.getToken(ProteinVariantParser.GENE51, 0)

        def GENE52(self):
            return self.getToken(ProteinVariantParser.GENE52, 0)

        def GENE53(self):
            return self.getToken(ProteinVariantParser.GENE53, 0)

        def GENE54(self):
            return self.getToken(ProteinVariantParser.GENE54, 0)

        def GENE55(self):
            return self.getToken(ProteinVariantParser.GENE55, 0)

        def GENE56(self):
            return self.getToken(ProteinVariantParser.GENE56, 0)

        def GENE57(self):
            return self.getToken(ProteinVariantParser.GENE57, 0)

        def GENE58(self):
            return self.getToken(ProteinVariantParser.GENE58, 0)

        def GENE59(self):
            return self.getToken(ProteinVariantParser.GENE59, 0)

        def GENE60(self):
            return self.getToken(ProteinVariantParser.GENE60, 0)

        def GENE61(self):
            return self.getToken(ProteinVariantParser.GENE61, 0)

        def GENE62(self):
            return self.getToken(ProteinVariantParser.GENE62, 0)

        def GENE63(self):
            return self.getToken(ProteinVariantParser.GENE63, 0)

        def GENE64(self):
            return self.getToken(ProteinVariantParser.GENE64, 0)

        def GENE65(self):
            return self.getToken(ProteinVariantParser.GENE65, 0)

        def GENE66(self):
            return self.getToken(ProteinVariantParser.GENE66, 0)

        def GENE67(self):
            return self.getToken(ProteinVariantParser.GENE67, 0)

        def GENE68(self):
            return self.getToken(ProteinVariantParser.GENE68, 0)

        def GENE69(self):
            return self.getToken(ProteinVariantParser.GENE69, 0)

        def GENE70(self):
            return self.getToken(ProteinVariantParser.GENE70, 0)

        def GENE71(self):
            return self.getToken(ProteinVariantParser.GENE71, 0)

        def GENE72(self):
            return self.getToken(ProteinVariantParser.GENE72, 0)

        def GENE73(self):
            return self.getToken(ProteinVariantParser.GENE73, 0)

        def GENE74(self):
            return self.getToken(ProteinVariantParser.GENE74, 0)

        def GENE75(self):
            return self.getToken(ProteinVariantParser.GENE75, 0)

        def GENE76(self):
            return self.getToken(ProteinVariantParser.GENE76, 0)

        def GENE77(self):
            return self.getToken(ProteinVariantParser.GENE77, 0)

        def GENE78(self):
            return self.getToken(ProteinVariantParser.GENE78, 0)

        def GENE79(self):
            return self.getToken(ProteinVariantParser.GENE79, 0)

        def GENE80(self):
            return self.getToken(ProteinVariantParser.GENE80, 0)

        def GENE81(self):
            return self.getToken(ProteinVariantParser.GENE81, 0)

        def GENE82(self):
            return self.getToken(ProteinVariantParser.GENE82, 0)

        def GENE83(self):
            return self.getToken(ProteinVariantParser.GENE83, 0)

        def GENE84(self):
            return self.getToken(ProteinVariantParser.GENE84, 0)

        def GENE85(self):
            return self.getToken(ProteinVariantParser.GENE85, 0)

        def GENE86(self):
            return self.getToken(ProteinVariantParser.GENE86, 0)

        def GENE87(self):
            return self.getToken(ProteinVariantParser.GENE87, 0)

        def GENE88(self):
            return self.getToken(ProteinVariantParser.GENE88, 0)

        def GENE89(self):
            return self.getToken(ProteinVariantParser.GENE89, 0)

        def GENE90(self):
            return self.getToken(ProteinVariantParser.GENE90, 0)

        def GENE91(self):
            return self.getToken(ProteinVariantParser.GENE91, 0)

        def GENE92(self):
            return self.getToken(ProteinVariantParser.GENE92, 0)

        def GENE93(self):
            return self.getToken(ProteinVariantParser.GENE93, 0)

        def GENE94(self):
            return self.getToken(ProteinVariantParser.GENE94, 0)

        def GENE95(self):
            return self.getToken(ProteinVariantParser.GENE95, 0)

        def GENE96(self):
            return self.getToken(ProteinVariantParser.GENE96, 0)

        def GENE97(self):
            return self.getToken(ProteinVariantParser.GENE97, 0)

        def GENE98(self):
            return self.getToken(ProteinVariantParser.GENE98, 0)

        def GENE99(self):
            return self.getToken(ProteinVariantParser.GENE99, 0)

        def GENE100(self):
            return self.getToken(ProteinVariantParser.GENE100, 0)

        def GENE101(self):
            return self.getToken(ProteinVariantParser.GENE101, 0)

        def GENE102(self):
            return self.getToken(ProteinVariantParser.GENE102, 0)

        def GENE103(self):
            return self.getToken(ProteinVariantParser.GENE103, 0)

        def GENE104(self):
            return self.getToken(ProteinVariantParser.GENE104, 0)

        def GENE105(self):
            return self.getToken(ProteinVariantParser.GENE105, 0)

        def GENE106(self):
            return self.getToken(ProteinVariantParser.GENE106, 0)

        def GENE107(self):
            return self.getToken(ProteinVariantParser.GENE107, 0)

        def GENE108(self):
            return self.getToken(ProteinVariantParser.GENE108, 0)

        def GENE109(self):
            return self.getToken(ProteinVariantParser.GENE109, 0)

        def GENE110(self):
            return self.getToken(ProteinVariantParser.GENE110, 0)

        def GENE111(self):
            return self.getToken(ProteinVariantParser.GENE111, 0)

        def GENE112(self):
            return self.getToken(ProteinVariantParser.GENE112, 0)

        def GENE113(self):
            return self.getToken(ProteinVariantParser.GENE113, 0)

        def GENE114(self):
            return self.getToken(ProteinVariantParser.GENE114, 0)

        def GENE115(self):
            return self.getToken(ProteinVariantParser.GENE115, 0)

        def GENE116(self):
            return self.getToken(ProteinVariantParser.GENE116, 0)

        def GENE117(self):
            return self.getToken(ProteinVariantParser.GENE117, 0)

        def GENE118(self):
            return self.getToken(ProteinVariantParser.GENE118, 0)

        def GENE119(self):
            return self.getToken(ProteinVariantParser.GENE119, 0)

        def GENE120(self):
            return self.getToken(ProteinVariantParser.GENE120, 0)

        def GENE121(self):
            return self.getToken(ProteinVariantParser.GENE121, 0)

        def GENE122(self):
            return self.getToken(ProteinVariantParser.GENE122, 0)

        def GENE123(self):
            return self.getToken(ProteinVariantParser.GENE123, 0)

        def GENE124(self):
            return self.getToken(ProteinVariantParser.GENE124, 0)

        def GENE125(self):
            return self.getToken(ProteinVariantParser.GENE125, 0)

        def GENE126(self):
            return self.getToken(ProteinVariantParser.GENE126, 0)

        def GENE127(self):
            return self.getToken(ProteinVariantParser.GENE127, 0)

        def GENE128(self):
            return self.getToken(ProteinVariantParser.GENE128, 0)

        def GENE129(self):
            return self.getToken(ProteinVariantParser.GENE129, 0)

        def GENE130(self):
            return self.getToken(ProteinVariantParser.GENE130, 0)

        def GENE131(self):
            return self.getToken(ProteinVariantParser.GENE131, 0)

        def GENE132(self):
            return self.getToken(ProteinVariantParser.GENE132, 0)

        def GENE133(self):
            return self.getToken(ProteinVariantParser.GENE133, 0)

        def GENE134(self):
            return self.getToken(ProteinVariantParser.GENE134, 0)

        def GENE135(self):
            return self.getToken(ProteinVariantParser.GENE135, 0)

        def GENE136(self):
            return self.getToken(ProteinVariantParser.GENE136, 0)

        def GENE137(self):
            return self.getToken(ProteinVariantParser.GENE137, 0)

        def GENE138(self):
            return self.getToken(ProteinVariantParser.GENE138, 0)

        def GENE139(self):
            return self.getToken(ProteinVariantParser.GENE139, 0)

        def GENE140(self):
            return self.getToken(ProteinVariantParser.GENE140, 0)

        def GENE141(self):
            return self.getToken(ProteinVariantParser.GENE141, 0)

        def GENE142(self):
            return self.getToken(ProteinVariantParser.GENE142, 0)

        def GENE143(self):
            return self.getToken(ProteinVariantParser.GENE143, 0)

        def GENE144(self):
            return self.getToken(ProteinVariantParser.GENE144, 0)

        def GENE145(self):
            return self.getToken(ProteinVariantParser.GENE145, 0)

        def GENE146(self):
            return self.getToken(ProteinVariantParser.GENE146, 0)

        def GENE147(self):
            return self.getToken(ProteinVariantParser.GENE147, 0)

        def GENE148(self):
            return self.getToken(ProteinVariantParser.GENE148, 0)

        def GENE149(self):
            return self.getToken(ProteinVariantParser.GENE149, 0)

        def GENE150(self):
            return self.getToken(ProteinVariantParser.GENE150, 0)

        def GENE151(self):
            return self.getToken(ProteinVariantParser.GENE151, 0)

        def GENE152(self):
            return self.getToken(ProteinVariantParser.GENE152, 0)

        def GENE153(self):
            return self.getToken(ProteinVariantParser.GENE153, 0)

        def GENE154(self):
            return self.getToken(ProteinVariantParser.GENE154, 0)

        def GENE155(self):
            return self.getToken(ProteinVariantParser.GENE155, 0)

        def GENE156(self):
            return self.getToken(ProteinVariantParser.GENE156, 0)

        def GENE157(self):
            return self.getToken(ProteinVariantParser.GENE157, 0)

        def GENE158(self):
            return self.getToken(ProteinVariantParser.GENE158, 0)

        def GENE159(self):
            return self.getToken(ProteinVariantParser.GENE159, 0)

        def GENE160(self):
            return self.getToken(ProteinVariantParser.GENE160, 0)

        def GENE161(self):
            return self.getToken(ProteinVariantParser.GENE161, 0)

        def GENE162(self):
            return self.getToken(ProteinVariantParser.GENE162, 0)

        def GENE163(self):
            return self.getToken(ProteinVariantParser.GENE163, 0)

        def GENE164(self):
            return self.getToken(ProteinVariantParser.GENE164, 0)

        def GENE165(self):
            return self.getToken(ProteinVariantParser.GENE165, 0)

        def GENE166(self):
            return self.getToken(ProteinVariantParser.GENE166, 0)

        def GENE167(self):
            return self.getToken(ProteinVariantParser.GENE167, 0)

        def GENE168(self):
            return self.getToken(ProteinVariantParser.GENE168, 0)

        def GENE169(self):
            return self.getToken(ProteinVariantParser.GENE169, 0)

        def GENE170(self):
            return self.getToken(ProteinVariantParser.GENE170, 0)

        def GENE171(self):
            return self.getToken(ProteinVariantParser.GENE171, 0)

        def GENE172(self):
            return self.getToken(ProteinVariantParser.GENE172, 0)

        def GENE173(self):
            return self.getToken(ProteinVariantParser.GENE173, 0)

        def GENE174(self):
            return self.getToken(ProteinVariantParser.GENE174, 0)

        def GENE175(self):
            return self.getToken(ProteinVariantParser.GENE175, 0)

        def GENE176(self):
            return self.getToken(ProteinVariantParser.GENE176, 0)

        def GENE177(self):
            return self.getToken(ProteinVariantParser.GENE177, 0)

        def GENE178(self):
            return self.getToken(ProteinVariantParser.GENE178, 0)

        def GENE179(self):
            return self.getToken(ProteinVariantParser.GENE179, 0)

        def GENE180(self):
            return self.getToken(ProteinVariantParser.GENE180, 0)

        def GENE181(self):
            return self.getToken(ProteinVariantParser.GENE181, 0)

        def GENE182(self):
            return self.getToken(ProteinVariantParser.GENE182, 0)

        def GENE183(self):
            return self.getToken(ProteinVariantParser.GENE183, 0)

        def GENE184(self):
            return self.getToken(ProteinVariantParser.GENE184, 0)

        def GENE185(self):
            return self.getToken(ProteinVariantParser.GENE185, 0)

        def GENE186(self):
            return self.getToken(ProteinVariantParser.GENE186, 0)

        def GENE187(self):
            return self.getToken(ProteinVariantParser.GENE187, 0)

        def GENE188(self):
            return self.getToken(ProteinVariantParser.GENE188, 0)

        def GENE189(self):
            return self.getToken(ProteinVariantParser.GENE189, 0)

        def GENE190(self):
            return self.getToken(ProteinVariantParser.GENE190, 0)

        def GENE191(self):
            return self.getToken(ProteinVariantParser.GENE191, 0)

        def GENE192(self):
            return self.getToken(ProteinVariantParser.GENE192, 0)

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
        self.enterRule(localctx, 0, self.RULE_gene)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & -128) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & -1) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & -1) != 0) or ((((_la - 192)) & ~0x3f) == 0 and ((1 << (_la - 192)) & 255) != 0)):
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
        self.enterRule(localctx, 2, self.RULE_mutation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.gene()
            self.state = 14
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 13
                self.match(ProteinVariantParser.WS)


            self.state = 16
            self.amino_acid_or_stop()
            self.state = 18
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 17
                self.match(ProteinVariantParser.WS)


            self.state = 20
            self.number_or_range()
            self.state = 22
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 21
                self.match(ProteinVariantParser.WS)


            self.state = 24
            self.amino_acid_or_stop()
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





