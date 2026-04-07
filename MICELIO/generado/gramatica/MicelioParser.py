# Generated from gramatica/Micelio.g4 by ANTLR 4.13.2
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
        4,1,62,493,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        1,0,5,0,56,8,0,10,0,12,0,59,9,0,1,0,1,0,5,0,63,8,0,10,0,12,0,66,
        9,0,5,0,68,8,0,10,0,12,0,71,9,0,1,0,1,0,1,1,1,1,3,1,77,8,1,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,89,8,2,1,3,1,3,1,3,1,3,1,3,
        1,3,3,3,97,8,3,1,4,1,4,1,4,1,4,5,4,103,8,4,10,4,12,4,106,9,4,1,4,
        1,4,1,4,1,4,5,4,112,8,4,10,4,12,4,115,9,4,3,4,117,8,4,1,5,1,5,1,
        5,1,5,1,5,1,6,1,6,1,6,1,6,1,7,1,7,3,7,130,8,7,1,8,1,8,1,9,1,9,1,
        10,1,10,1,10,1,10,3,10,140,8,10,1,11,1,11,1,11,1,12,1,12,1,12,1,
        13,1,13,1,13,1,13,1,13,5,13,153,8,13,10,13,12,13,156,9,13,1,13,1,
        13,5,13,160,8,13,10,13,12,13,163,9,13,1,13,1,13,5,13,167,8,13,10,
        13,12,13,170,9,13,1,13,3,13,173,8,13,1,14,1,14,1,14,1,14,1,14,5,
        14,180,8,14,10,14,12,14,183,9,14,1,14,1,14,5,14,187,8,14,10,14,12,
        14,190,9,14,1,14,4,14,193,8,14,11,14,12,14,194,1,14,1,14,1,15,1,
        15,1,15,1,15,5,15,203,8,15,10,15,12,15,206,9,15,1,15,1,15,5,15,210,
        8,15,10,15,12,15,213,9,15,5,15,215,8,15,10,15,12,15,218,9,15,1,15,
        1,15,1,15,5,15,223,8,15,10,15,12,15,226,9,15,1,15,1,15,5,15,230,
        8,15,10,15,12,15,233,9,15,5,15,235,8,15,10,15,12,15,238,9,15,3,15,
        240,8,15,1,16,1,16,1,16,1,16,1,16,5,16,247,8,16,10,16,12,16,250,
        9,16,1,16,1,16,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,3,17,262,
        8,17,1,17,5,17,265,8,17,10,17,12,17,268,9,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,5,17,277,8,17,10,17,12,17,280,9,17,1,17,1,17,3,17,
        284,8,17,1,18,1,18,1,18,1,18,3,18,290,8,18,1,18,1,18,5,18,294,8,
        18,10,18,12,18,297,9,18,1,18,1,18,1,19,1,19,1,19,5,19,304,8,19,10,
        19,12,19,307,9,19,1,20,1,20,1,20,1,20,1,20,3,20,314,8,20,1,21,1,
        21,5,21,318,8,21,10,21,12,21,321,9,21,1,21,1,21,5,21,325,8,21,10,
        21,12,21,328,9,21,5,21,330,8,21,10,21,12,21,333,9,21,1,21,1,21,1,
        22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,5,22,348,8,
        22,10,22,12,22,351,9,22,3,22,353,8,22,1,22,1,22,1,22,1,22,1,22,1,
        22,5,22,361,8,22,10,22,12,22,364,9,22,3,22,366,8,22,1,22,1,22,1,
        22,1,22,1,22,1,22,5,22,374,8,22,10,22,12,22,377,9,22,3,22,379,8,
        22,1,22,1,22,1,22,1,22,1,22,5,22,386,8,22,10,22,12,22,389,9,22,3,
        22,391,8,22,1,22,1,22,1,22,1,22,3,22,397,8,22,1,22,1,22,1,22,1,22,
        1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,3,22,412,8,22,1,22,
        1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,
        1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,5,22,437,8,22,10,22,
        12,22,440,9,22,1,22,1,22,5,22,444,8,22,10,22,12,22,447,9,22,1,22,
        1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,3,22,458,8,22,1,22,1,22,
        1,22,1,22,1,22,1,22,5,22,466,8,22,10,22,12,22,469,9,22,1,23,1,23,
        1,23,1,23,1,24,1,24,1,24,5,24,478,8,24,10,24,12,24,481,9,24,1,25,
        1,25,1,26,1,26,4,26,487,8,26,11,26,12,26,488,3,26,491,8,26,1,26,
        0,1,44,27,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,
        40,42,44,46,48,50,52,0,5,1,0,43,44,2,0,42,42,47,49,1,0,45,46,1,0,
        51,56,2,0,35,36,57,58,553,0,57,1,0,0,0,2,76,1,0,0,0,4,88,1,0,0,0,
        6,96,1,0,0,0,8,98,1,0,0,0,10,118,1,0,0,0,12,123,1,0,0,0,14,127,1,
        0,0,0,16,131,1,0,0,0,18,133,1,0,0,0,20,135,1,0,0,0,22,141,1,0,0,
        0,24,144,1,0,0,0,26,147,1,0,0,0,28,174,1,0,0,0,30,239,1,0,0,0,32,
        241,1,0,0,0,34,283,1,0,0,0,36,285,1,0,0,0,38,300,1,0,0,0,40,313,
        1,0,0,0,42,315,1,0,0,0,44,411,1,0,0,0,46,470,1,0,0,0,48,474,1,0,
        0,0,50,482,1,0,0,0,52,490,1,0,0,0,54,56,3,52,26,0,55,54,1,0,0,0,
        56,59,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,69,1,0,0,0,59,57,1,
        0,0,0,60,64,3,2,1,0,61,63,3,52,26,0,62,61,1,0,0,0,63,66,1,0,0,0,
        64,62,1,0,0,0,64,65,1,0,0,0,65,68,1,0,0,0,66,64,1,0,0,0,67,60,1,
        0,0,0,68,71,1,0,0,0,69,67,1,0,0,0,69,70,1,0,0,0,70,72,1,0,0,0,71,
        69,1,0,0,0,72,73,5,0,0,1,73,1,1,0,0,0,74,77,3,4,2,0,75,77,3,6,3,
        0,76,74,1,0,0,0,76,75,1,0,0,0,77,3,1,0,0,0,78,89,3,8,4,0,79,89,3,
        10,5,0,80,89,3,12,6,0,81,89,3,14,7,0,82,89,3,16,8,0,83,89,3,18,9,
        0,84,89,3,20,10,0,85,89,3,22,11,0,86,89,3,24,12,0,87,89,3,44,22,
        0,88,78,1,0,0,0,88,79,1,0,0,0,88,80,1,0,0,0,88,81,1,0,0,0,88,82,
        1,0,0,0,88,83,1,0,0,0,88,84,1,0,0,0,88,85,1,0,0,0,88,86,1,0,0,0,
        88,87,1,0,0,0,89,5,1,0,0,0,90,97,3,26,13,0,91,97,3,28,14,0,92,97,
        3,32,16,0,93,97,3,34,17,0,94,97,3,36,18,0,95,97,3,42,21,0,96,90,
        1,0,0,0,96,91,1,0,0,0,96,92,1,0,0,0,96,93,1,0,0,0,96,94,1,0,0,0,
        96,95,1,0,0,0,97,7,1,0,0,0,98,99,5,12,0,0,99,104,5,59,0,0,100,101,
        5,1,0,0,101,103,5,59,0,0,102,100,1,0,0,0,103,106,1,0,0,0,104,102,
        1,0,0,0,104,105,1,0,0,0,105,116,1,0,0,0,106,104,1,0,0,0,107,108,
        5,2,0,0,108,113,3,44,22,0,109,110,5,1,0,0,110,112,3,44,22,0,111,
        109,1,0,0,0,112,115,1,0,0,0,113,111,1,0,0,0,113,114,1,0,0,0,114,
        117,1,0,0,0,115,113,1,0,0,0,116,107,1,0,0,0,116,117,1,0,0,0,117,
        9,1,0,0,0,118,119,5,13,0,0,119,120,5,59,0,0,120,121,5,2,0,0,121,
        122,3,44,22,0,122,11,1,0,0,0,123,124,5,59,0,0,124,125,5,2,0,0,125,
        126,3,44,22,0,126,13,1,0,0,0,127,129,5,16,0,0,128,130,3,44,22,0,
        129,128,1,0,0,0,129,130,1,0,0,0,130,15,1,0,0,0,131,132,5,27,0,0,
        132,17,1,0,0,0,133,134,5,28,0,0,134,19,1,0,0,0,135,136,5,31,0,0,
        136,139,5,58,0,0,137,138,5,32,0,0,138,140,5,59,0,0,139,137,1,0,0,
        0,139,140,1,0,0,0,140,21,1,0,0,0,141,142,5,29,0,0,142,143,5,59,0,
        0,143,23,1,0,0,0,144,145,5,30,0,0,145,146,3,44,22,0,146,25,1,0,0,
        0,147,148,5,17,0,0,148,149,5,3,0,0,149,150,3,44,22,0,150,154,5,4,
        0,0,151,153,3,52,26,0,152,151,1,0,0,0,153,156,1,0,0,0,154,152,1,
        0,0,0,154,155,1,0,0,0,155,157,1,0,0,0,156,154,1,0,0,0,157,172,3,
        42,21,0,158,160,3,52,26,0,159,158,1,0,0,0,160,163,1,0,0,0,161,159,
        1,0,0,0,161,162,1,0,0,0,162,164,1,0,0,0,163,161,1,0,0,0,164,168,
        5,18,0,0,165,167,3,52,26,0,166,165,1,0,0,0,167,170,1,0,0,0,168,166,
        1,0,0,0,168,169,1,0,0,0,169,171,1,0,0,0,170,168,1,0,0,0,171,173,
        3,42,21,0,172,161,1,0,0,0,172,173,1,0,0,0,173,27,1,0,0,0,174,175,
        5,19,0,0,175,176,5,3,0,0,176,177,3,44,22,0,177,181,5,4,0,0,178,180,
        3,52,26,0,179,178,1,0,0,0,180,183,1,0,0,0,181,179,1,0,0,0,181,182,
        1,0,0,0,182,184,1,0,0,0,183,181,1,0,0,0,184,188,5,5,0,0,185,187,
        3,52,26,0,186,185,1,0,0,0,187,190,1,0,0,0,188,186,1,0,0,0,188,189,
        1,0,0,0,189,192,1,0,0,0,190,188,1,0,0,0,191,193,3,30,15,0,192,191,
        1,0,0,0,193,194,1,0,0,0,194,192,1,0,0,0,194,195,1,0,0,0,195,196,
        1,0,0,0,196,197,5,6,0,0,197,29,1,0,0,0,198,199,5,20,0,0,199,200,
        3,44,22,0,200,204,5,7,0,0,201,203,3,52,26,0,202,201,1,0,0,0,203,
        206,1,0,0,0,204,202,1,0,0,0,204,205,1,0,0,0,205,216,1,0,0,0,206,
        204,1,0,0,0,207,211,3,2,1,0,208,210,3,52,26,0,209,208,1,0,0,0,210,
        213,1,0,0,0,211,209,1,0,0,0,211,212,1,0,0,0,212,215,1,0,0,0,213,
        211,1,0,0,0,214,207,1,0,0,0,215,218,1,0,0,0,216,214,1,0,0,0,216,
        217,1,0,0,0,217,240,1,0,0,0,218,216,1,0,0,0,219,220,5,21,0,0,220,
        224,5,7,0,0,221,223,3,52,26,0,222,221,1,0,0,0,223,226,1,0,0,0,224,
        222,1,0,0,0,224,225,1,0,0,0,225,236,1,0,0,0,226,224,1,0,0,0,227,
        231,3,2,1,0,228,230,3,52,26,0,229,228,1,0,0,0,230,233,1,0,0,0,231,
        229,1,0,0,0,231,232,1,0,0,0,232,235,1,0,0,0,233,231,1,0,0,0,234,
        227,1,0,0,0,235,238,1,0,0,0,236,234,1,0,0,0,236,237,1,0,0,0,237,
        240,1,0,0,0,238,236,1,0,0,0,239,198,1,0,0,0,239,219,1,0,0,0,240,
        31,1,0,0,0,241,242,5,26,0,0,242,243,5,3,0,0,243,244,3,44,22,0,244,
        248,5,4,0,0,245,247,3,52,26,0,246,245,1,0,0,0,247,250,1,0,0,0,248,
        246,1,0,0,0,248,249,1,0,0,0,249,251,1,0,0,0,250,248,1,0,0,0,251,
        252,3,42,21,0,252,33,1,0,0,0,253,254,5,22,0,0,254,255,5,59,0,0,255,
        256,5,2,0,0,256,257,3,44,22,0,257,258,5,23,0,0,258,261,3,44,22,0,
        259,260,5,24,0,0,260,262,3,44,22,0,261,259,1,0,0,0,261,262,1,0,0,
        0,262,266,1,0,0,0,263,265,3,52,26,0,264,263,1,0,0,0,265,268,1,0,
        0,0,266,264,1,0,0,0,266,267,1,0,0,0,267,269,1,0,0,0,268,266,1,0,
        0,0,269,270,3,42,21,0,270,284,1,0,0,0,271,272,5,22,0,0,272,273,5,
        59,0,0,273,274,5,25,0,0,274,278,3,44,22,0,275,277,3,52,26,0,276,
        275,1,0,0,0,277,280,1,0,0,0,278,276,1,0,0,0,278,279,1,0,0,0,279,
        281,1,0,0,0,280,278,1,0,0,0,281,282,3,42,21,0,282,284,1,0,0,0,283,
        253,1,0,0,0,283,271,1,0,0,0,284,35,1,0,0,0,285,286,5,14,0,0,286,
        287,5,59,0,0,287,289,5,3,0,0,288,290,3,38,19,0,289,288,1,0,0,0,289,
        290,1,0,0,0,290,291,1,0,0,0,291,295,5,4,0,0,292,294,3,52,26,0,293,
        292,1,0,0,0,294,297,1,0,0,0,295,293,1,0,0,0,295,296,1,0,0,0,296,
        298,1,0,0,0,297,295,1,0,0,0,298,299,3,42,21,0,299,37,1,0,0,0,300,
        305,3,40,20,0,301,302,5,1,0,0,302,304,3,40,20,0,303,301,1,0,0,0,
        304,307,1,0,0,0,305,303,1,0,0,0,305,306,1,0,0,0,306,39,1,0,0,0,307,
        305,1,0,0,0,308,314,5,59,0,0,309,310,5,47,0,0,310,314,5,59,0,0,311,
        312,5,50,0,0,312,314,5,59,0,0,313,308,1,0,0,0,313,309,1,0,0,0,313,
        311,1,0,0,0,314,41,1,0,0,0,315,319,5,5,0,0,316,318,3,52,26,0,317,
        316,1,0,0,0,318,321,1,0,0,0,319,317,1,0,0,0,319,320,1,0,0,0,320,
        331,1,0,0,0,321,319,1,0,0,0,322,326,3,2,1,0,323,325,3,52,26,0,324,
        323,1,0,0,0,325,328,1,0,0,0,326,324,1,0,0,0,326,327,1,0,0,0,327,
        330,1,0,0,0,328,326,1,0,0,0,329,322,1,0,0,0,330,333,1,0,0,0,331,
        329,1,0,0,0,331,332,1,0,0,0,332,334,1,0,0,0,333,331,1,0,0,0,334,
        335,5,6,0,0,335,43,1,0,0,0,336,337,6,22,-1,0,337,412,3,50,25,0,338,
        412,5,59,0,0,339,340,5,3,0,0,340,341,3,44,22,0,341,342,5,4,0,0,342,
        412,1,0,0,0,343,352,5,8,0,0,344,349,3,44,22,0,345,346,5,1,0,0,346,
        348,3,44,22,0,347,345,1,0,0,0,348,351,1,0,0,0,349,347,1,0,0,0,349,
        350,1,0,0,0,350,353,1,0,0,0,351,349,1,0,0,0,352,344,1,0,0,0,352,
        353,1,0,0,0,353,354,1,0,0,0,354,412,5,9,0,0,355,356,5,33,0,0,356,
        365,5,3,0,0,357,362,3,44,22,0,358,359,5,1,0,0,359,361,3,44,22,0,
        360,358,1,0,0,0,361,364,1,0,0,0,362,360,1,0,0,0,362,363,1,0,0,0,
        363,366,1,0,0,0,364,362,1,0,0,0,365,357,1,0,0,0,365,366,1,0,0,0,
        366,367,1,0,0,0,367,412,5,4,0,0,368,369,5,34,0,0,369,378,5,3,0,0,
        370,375,3,46,23,0,371,372,5,1,0,0,372,374,3,46,23,0,373,371,1,0,
        0,0,374,377,1,0,0,0,375,373,1,0,0,0,375,376,1,0,0,0,376,379,1,0,
        0,0,377,375,1,0,0,0,378,370,1,0,0,0,378,379,1,0,0,0,379,380,1,0,
        0,0,380,412,5,4,0,0,381,390,5,5,0,0,382,387,3,46,23,0,383,384,5,
        1,0,0,384,386,3,46,23,0,385,383,1,0,0,0,386,389,1,0,0,0,387,385,
        1,0,0,0,387,388,1,0,0,0,388,391,1,0,0,0,389,387,1,0,0,0,390,382,
        1,0,0,0,390,391,1,0,0,0,391,392,1,0,0,0,392,412,5,6,0,0,393,394,
        5,14,0,0,394,396,5,3,0,0,395,397,3,38,19,0,396,395,1,0,0,0,396,397,
        1,0,0,0,397,398,1,0,0,0,398,399,5,4,0,0,399,412,3,42,21,0,400,401,
        5,15,0,0,401,402,5,3,0,0,402,403,3,44,22,0,403,404,5,4,0,0,404,412,
        1,0,0,0,405,406,7,0,0,0,406,412,3,44,22,13,407,408,5,46,0,0,408,
        412,3,44,22,11,409,410,5,39,0,0,410,412,3,44,22,10,411,336,1,0,0,
        0,411,338,1,0,0,0,411,339,1,0,0,0,411,343,1,0,0,0,411,355,1,0,0,
        0,411,368,1,0,0,0,411,381,1,0,0,0,411,393,1,0,0,0,411,400,1,0,0,
        0,411,405,1,0,0,0,411,407,1,0,0,0,411,409,1,0,0,0,412,467,1,0,0,
        0,413,414,10,9,0,0,414,415,7,1,0,0,415,466,3,44,22,10,416,417,10,
        8,0,0,417,418,7,2,0,0,418,466,3,44,22,9,419,420,10,7,0,0,420,421,
        5,50,0,0,421,466,3,44,22,8,422,423,10,6,0,0,423,424,7,3,0,0,424,
        466,3,44,22,7,425,426,10,5,0,0,426,427,5,37,0,0,427,466,3,44,22,
        6,428,429,10,4,0,0,429,430,5,38,0,0,430,466,3,44,22,5,431,432,10,
        3,0,0,432,433,5,40,0,0,433,466,3,44,22,4,434,438,10,2,0,0,435,437,
        5,61,0,0,436,435,1,0,0,0,437,440,1,0,0,0,438,436,1,0,0,0,438,439,
        1,0,0,0,439,441,1,0,0,0,440,438,1,0,0,0,441,445,5,41,0,0,442,444,
        5,61,0,0,443,442,1,0,0,0,444,447,1,0,0,0,445,443,1,0,0,0,445,446,
        1,0,0,0,446,448,1,0,0,0,447,445,1,0,0,0,448,466,3,44,22,3,449,450,
        10,15,0,0,450,451,5,8,0,0,451,452,3,44,22,0,452,453,5,9,0,0,453,
        466,1,0,0,0,454,455,10,14,0,0,455,457,5,3,0,0,456,458,3,48,24,0,
        457,456,1,0,0,0,457,458,1,0,0,0,458,459,1,0,0,0,459,466,5,4,0,0,
        460,461,10,12,0,0,461,466,7,0,0,0,462,463,10,1,0,0,463,464,5,10,
        0,0,464,466,5,59,0,0,465,413,1,0,0,0,465,416,1,0,0,0,465,419,1,0,
        0,0,465,422,1,0,0,0,465,425,1,0,0,0,465,428,1,0,0,0,465,431,1,0,
        0,0,465,434,1,0,0,0,465,449,1,0,0,0,465,454,1,0,0,0,465,460,1,0,
        0,0,465,462,1,0,0,0,466,469,1,0,0,0,467,465,1,0,0,0,467,468,1,0,
        0,0,468,45,1,0,0,0,469,467,1,0,0,0,470,471,3,44,22,0,471,472,5,7,
        0,0,472,473,3,44,22,0,473,47,1,0,0,0,474,479,3,44,22,0,475,476,5,
        1,0,0,476,478,3,44,22,0,477,475,1,0,0,0,478,481,1,0,0,0,479,477,
        1,0,0,0,479,480,1,0,0,0,480,49,1,0,0,0,481,479,1,0,0,0,482,483,7,
        4,0,0,483,51,1,0,0,0,484,491,5,11,0,0,485,487,5,61,0,0,486,485,1,
        0,0,0,487,488,1,0,0,0,488,486,1,0,0,0,488,489,1,0,0,0,489,491,1,
        0,0,0,490,484,1,0,0,0,490,486,1,0,0,0,491,53,1,0,0,0,55,57,64,69,
        76,88,96,104,113,116,129,139,154,161,168,172,181,188,194,204,211,
        216,224,231,236,239,248,261,266,278,283,289,295,305,313,319,326,
        331,349,352,362,365,375,378,387,390,396,411,438,445,457,465,467,
        479,488,490
    ]

class MicelioParser ( Parser ):

    grammarFileName = "Micelio.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "'='", "'('", "')'", "'{'", "'}'", 
                     "':'", "'['", "']'", "'.'", "';'", "'var'", "'const'", 
                     "'funcion'", "'matriz'", "'regresa'", "'si'", "'sino'", 
                     "'segun'", "'caso'", "'defecto'", "'para'", "'hasta'", 
                     "'inc'", "'en'", "'mientras'", "'romper'", "'continuar'", 
                     "'leer'", "'imp'", "'importar'", "'como'", "'set'", 
                     "'dict'", "<INVALID>", "'nulo'", "'y'", "'o'", "'no'", 
                     "'in'", "'|>'", "'.*'", "'++'", "'--'", "'+'", "'-'", 
                     "'*'", "'/'", "'%'", "'**'", "'=='", "'!='", "'<'", 
                     "'<='", "'>'", "'>='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "VAR", "CONST", "FUNCION", "MATRIZ", "REGRESA", "SI", 
                      "SINO", "SEGUN", "CASO", "DEFECTO", "PARA", "HASTA", 
                      "INC", "EN", "MIENTRAS", "ROMPER", "CONTINUAR", "LEER", 
                      "IMP", "IMPORTAR", "COMO", "SET", "DICT", "BOOL", 
                      "NULL", "Y", "O", "NO", "IN", "PIPE", "DOTMUL", "INC_OP", 
                      "DEC_OP", "PLUS", "MINUS", "MUL", "DIV", "MOD", "POW", 
                      "EQ", "NE", "LT", "LE", "GT", "GE", "NUMBER", "STRING", 
                      "ID", "COMMENT", "NEWLINE", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_simple_stmt = 2
    RULE_compound_stmt = 3
    RULE_var_decl = 4
    RULE_const_decl = 5
    RULE_assignment = 6
    RULE_return_stmt = 7
    RULE_break_stmt = 8
    RULE_continue_stmt = 9
    RULE_import_stmt = 10
    RULE_leer_stmt = 11
    RULE_imp_stmt = 12
    RULE_if_stmt = 13
    RULE_switch_stmt = 14
    RULE_case_block = 15
    RULE_while_stmt = 16
    RULE_for_stmt = 17
    RULE_func_def = 18
    RULE_param_list = 19
    RULE_param_item = 20
    RULE_block = 21
    RULE_expr = 22
    RULE_keyValue = 23
    RULE_exprList = 24
    RULE_literal = 25
    RULE_sep = 26

    ruleNames =  [ "program", "statement", "simple_stmt", "compound_stmt", 
                   "var_decl", "const_decl", "assignment", "return_stmt", 
                   "break_stmt", "continue_stmt", "import_stmt", "leer_stmt", 
                   "imp_stmt", "if_stmt", "switch_stmt", "case_block", "while_stmt", 
                   "for_stmt", "func_def", "param_list", "param_item", "block", 
                   "expr", "keyValue", "exprList", "literal", "sep" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    VAR=12
    CONST=13
    FUNCION=14
    MATRIZ=15
    REGRESA=16
    SI=17
    SINO=18
    SEGUN=19
    CASO=20
    DEFECTO=21
    PARA=22
    HASTA=23
    INC=24
    EN=25
    MIENTRAS=26
    ROMPER=27
    CONTINUAR=28
    LEER=29
    IMP=30
    IMPORTAR=31
    COMO=32
    SET=33
    DICT=34
    BOOL=35
    NULL=36
    Y=37
    O=38
    NO=39
    IN=40
    PIPE=41
    DOTMUL=42
    INC_OP=43
    DEC_OP=44
    PLUS=45
    MINUS=46
    MUL=47
    DIV=48
    MOD=49
    POW=50
    EQ=51
    NE=52
    LT=53
    LE=54
    GT=55
    GE=56
    NUMBER=57
    STRING=58
    ID=59
    COMMENT=60
    NEWLINE=61
    WS=62

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(MicelioParser.EOF, 0)

        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.StatementContext)
            else:
                return self.getTypedRuleContext(MicelioParser.StatementContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = MicelioParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==61:
                self.state = 54
                self.sep()
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903756391903528) != 0):
                self.state = 60
                self.statement()
                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 61
                    self.sep()
                    self.state = 66
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 72
            self.match(MicelioParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Simple_stmtContext,0)


        def compound_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Compound_stmtContext,0)


        def getRuleIndex(self):
            return MicelioParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = MicelioParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 76
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 74
                self.simple_stmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 75
                self.compound_stmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Simple_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var_decl(self):
            return self.getTypedRuleContext(MicelioParser.Var_declContext,0)


        def const_decl(self):
            return self.getTypedRuleContext(MicelioParser.Const_declContext,0)


        def assignment(self):
            return self.getTypedRuleContext(MicelioParser.AssignmentContext,0)


        def return_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Return_stmtContext,0)


        def break_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Break_stmtContext,0)


        def continue_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Continue_stmtContext,0)


        def import_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Import_stmtContext,0)


        def leer_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Leer_stmtContext,0)


        def imp_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Imp_stmtContext,0)


        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def getRuleIndex(self):
            return MicelioParser.RULE_simple_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimple_stmt" ):
                listener.enterSimple_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimple_stmt" ):
                listener.exitSimple_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimple_stmt" ):
                return visitor.visitSimple_stmt(self)
            else:
                return visitor.visitChildren(self)




    def simple_stmt(self):

        localctx = MicelioParser.Simple_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_simple_stmt)
        try:
            self.state = 88
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 78
                self.var_decl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 79
                self.const_decl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 80
                self.assignment()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 81
                self.return_stmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 82
                self.break_stmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 83
                self.continue_stmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 84
                self.import_stmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 85
                self.leer_stmt()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 86
                self.imp_stmt()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 87
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Compound_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def if_stmt(self):
            return self.getTypedRuleContext(MicelioParser.If_stmtContext,0)


        def switch_stmt(self):
            return self.getTypedRuleContext(MicelioParser.Switch_stmtContext,0)


        def while_stmt(self):
            return self.getTypedRuleContext(MicelioParser.While_stmtContext,0)


        def for_stmt(self):
            return self.getTypedRuleContext(MicelioParser.For_stmtContext,0)


        def func_def(self):
            return self.getTypedRuleContext(MicelioParser.Func_defContext,0)


        def block(self):
            return self.getTypedRuleContext(MicelioParser.BlockContext,0)


        def getRuleIndex(self):
            return MicelioParser.RULE_compound_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_stmt" ):
                listener.enterCompound_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_stmt" ):
                listener.exitCompound_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_stmt" ):
                return visitor.visitCompound_stmt(self)
            else:
                return visitor.visitChildren(self)




    def compound_stmt(self):

        localctx = MicelioParser.Compound_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_compound_stmt)
        try:
            self.state = 96
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 90
                self.if_stmt()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 91
                self.switch_stmt()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 3)
                self.state = 92
                self.while_stmt()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 4)
                self.state = 93
                self.for_stmt()
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 5)
                self.state = 94
                self.func_def()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 6)
                self.state = 95
                self.block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Var_declContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(MicelioParser.VAR, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(MicelioParser.ID)
            else:
                return self.getToken(MicelioParser.ID, i)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_var_decl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar_decl" ):
                listener.enterVar_decl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar_decl" ):
                listener.exitVar_decl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVar_decl" ):
                return visitor.visitVar_decl(self)
            else:
                return visitor.visitChildren(self)




    def var_decl(self):

        localctx = MicelioParser.Var_declContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_var_decl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self.match(MicelioParser.VAR)
            self.state = 99
            self.match(MicelioParser.ID)
            self.state = 104
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 100
                self.match(MicelioParser.T__0)
                self.state = 101
                self.match(MicelioParser.ID)
                self.state = 106
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 107
                self.match(MicelioParser.T__1)
                self.state = 108
                self.expr(0)
                self.state = 113
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==1:
                    self.state = 109
                    self.match(MicelioParser.T__0)
                    self.state = 110
                    self.expr(0)
                    self.state = 115
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Const_declContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(MicelioParser.CONST, 0)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def getRuleIndex(self):
            return MicelioParser.RULE_const_decl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConst_decl" ):
                listener.enterConst_decl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConst_decl" ):
                listener.exitConst_decl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConst_decl" ):
                return visitor.visitConst_decl(self)
            else:
                return visitor.visitChildren(self)




    def const_decl(self):

        localctx = MicelioParser.Const_declContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_const_decl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(MicelioParser.CONST)
            self.state = 119
            self.match(MicelioParser.ID)
            self.state = 120
            self.match(MicelioParser.T__1)
            self.state = 121
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def getRuleIndex(self):
            return MicelioParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = MicelioParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(MicelioParser.ID)
            self.state = 124
            self.match(MicelioParser.T__1)
            self.state = 125
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Return_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REGRESA(self):
            return self.getToken(MicelioParser.REGRESA, 0)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def getRuleIndex(self):
            return MicelioParser.RULE_return_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturn_stmt" ):
                listener.enterReturn_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturn_stmt" ):
                listener.exitReturn_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn_stmt" ):
                return visitor.visitReturn_stmt(self)
            else:
                return visitor.visitChildren(self)




    def return_stmt(self):

        localctx = MicelioParser.Return_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_return_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(MicelioParser.REGRESA)
            self.state = 129
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 128
                self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Break_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ROMPER(self):
            return self.getToken(MicelioParser.ROMPER, 0)

        def getRuleIndex(self):
            return MicelioParser.RULE_break_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreak_stmt" ):
                listener.enterBreak_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreak_stmt" ):
                listener.exitBreak_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreak_stmt" ):
                return visitor.visitBreak_stmt(self)
            else:
                return visitor.visitChildren(self)




    def break_stmt(self):

        localctx = MicelioParser.Break_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_break_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(MicelioParser.ROMPER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Continue_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTINUAR(self):
            return self.getToken(MicelioParser.CONTINUAR, 0)

        def getRuleIndex(self):
            return MicelioParser.RULE_continue_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinue_stmt" ):
                listener.enterContinue_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinue_stmt" ):
                listener.exitContinue_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinue_stmt" ):
                return visitor.visitContinue_stmt(self)
            else:
                return visitor.visitChildren(self)




    def continue_stmt(self):

        localctx = MicelioParser.Continue_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_continue_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self.match(MicelioParser.CONTINUAR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMPORTAR(self):
            return self.getToken(MicelioParser.IMPORTAR, 0)

        def STRING(self):
            return self.getToken(MicelioParser.STRING, 0)

        def COMO(self):
            return self.getToken(MicelioParser.COMO, 0)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def getRuleIndex(self):
            return MicelioParser.RULE_import_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_stmt" ):
                listener.enterImport_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_stmt" ):
                listener.exitImport_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImport_stmt" ):
                return visitor.visitImport_stmt(self)
            else:
                return visitor.visitChildren(self)




    def import_stmt(self):

        localctx = MicelioParser.Import_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_import_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            self.match(MicelioParser.IMPORTAR)
            self.state = 136
            self.match(MicelioParser.STRING)
            self.state = 139
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==32:
                self.state = 137
                self.match(MicelioParser.COMO)
                self.state = 138
                self.match(MicelioParser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Leer_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LEER(self):
            return self.getToken(MicelioParser.LEER, 0)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def getRuleIndex(self):
            return MicelioParser.RULE_leer_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLeer_stmt" ):
                listener.enterLeer_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLeer_stmt" ):
                listener.exitLeer_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLeer_stmt" ):
                return visitor.visitLeer_stmt(self)
            else:
                return visitor.visitChildren(self)




    def leer_stmt(self):

        localctx = MicelioParser.Leer_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_leer_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.match(MicelioParser.LEER)
            self.state = 142
            self.match(MicelioParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Imp_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMP(self):
            return self.getToken(MicelioParser.IMP, 0)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def getRuleIndex(self):
            return MicelioParser.RULE_imp_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImp_stmt" ):
                listener.enterImp_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImp_stmt" ):
                listener.exitImp_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImp_stmt" ):
                return visitor.visitImp_stmt(self)
            else:
                return visitor.visitChildren(self)




    def imp_stmt(self):

        localctx = MicelioParser.Imp_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_imp_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self.match(MicelioParser.IMP)
            self.state = 145
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class If_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SI(self):
            return self.getToken(MicelioParser.SI, 0)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.BlockContext)
            else:
                return self.getTypedRuleContext(MicelioParser.BlockContext,i)


        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)


        def SINO(self):
            return self.getToken(MicelioParser.SINO, 0)

        def getRuleIndex(self):
            return MicelioParser.RULE_if_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIf_stmt" ):
                listener.enterIf_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIf_stmt" ):
                listener.exitIf_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIf_stmt" ):
                return visitor.visitIf_stmt(self)
            else:
                return visitor.visitChildren(self)




    def if_stmt(self):

        localctx = MicelioParser.If_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_if_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.match(MicelioParser.SI)
            self.state = 148
            self.match(MicelioParser.T__2)
            self.state = 149
            self.expr(0)
            self.state = 150
            self.match(MicelioParser.T__3)
            self.state = 154
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==61:
                self.state = 151
                self.sep()
                self.state = 156
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 157
            self.block()
            self.state = 172
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.state = 161
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 158
                    self.sep()
                    self.state = 163
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 164
                self.match(MicelioParser.SINO)
                self.state = 168
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 165
                    self.sep()
                    self.state = 170
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 171
                self.block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Switch_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEGUN(self):
            return self.getToken(MicelioParser.SEGUN, 0)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)


        def case_block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.Case_blockContext)
            else:
                return self.getTypedRuleContext(MicelioParser.Case_blockContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_switch_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSwitch_stmt" ):
                listener.enterSwitch_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSwitch_stmt" ):
                listener.exitSwitch_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSwitch_stmt" ):
                return visitor.visitSwitch_stmt(self)
            else:
                return visitor.visitChildren(self)




    def switch_stmt(self):

        localctx = MicelioParser.Switch_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_switch_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.match(MicelioParser.SEGUN)
            self.state = 175
            self.match(MicelioParser.T__2)
            self.state = 176
            self.expr(0)
            self.state = 177
            self.match(MicelioParser.T__3)
            self.state = 181
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==61:
                self.state = 178
                self.sep()
                self.state = 183
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 184
            self.match(MicelioParser.T__4)
            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==61:
                self.state = 185
                self.sep()
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 192 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 191
                self.case_block()
                self.state = 194 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==20 or _la==21):
                    break

            self.state = 196
            self.match(MicelioParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Case_blockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MicelioParser.RULE_case_block

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DefaultClauseContext(Case_blockContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.Case_blockContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DEFECTO(self):
            return self.getToken(MicelioParser.DEFECTO, 0)
        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.StatementContext)
            else:
                return self.getTypedRuleContext(MicelioParser.StatementContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefaultClause" ):
                listener.enterDefaultClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefaultClause" ):
                listener.exitDefaultClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefaultClause" ):
                return visitor.visitDefaultClause(self)
            else:
                return visitor.visitChildren(self)


    class CaseClauseContext(Case_blockContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.Case_blockContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CASO(self):
            return self.getToken(MicelioParser.CASO, 0)
        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)

        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.StatementContext)
            else:
                return self.getTypedRuleContext(MicelioParser.StatementContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseClause" ):
                listener.enterCaseClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseClause" ):
                listener.exitCaseClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseClause" ):
                return visitor.visitCaseClause(self)
            else:
                return visitor.visitChildren(self)



    def case_block(self):

        localctx = MicelioParser.Case_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_case_block)
        self._la = 0 # Token type
        try:
            self.state = 239
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                localctx = MicelioParser.CaseClauseContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 198
                self.match(MicelioParser.CASO)
                self.state = 199
                self.expr(0)
                self.state = 200
                self.match(MicelioParser.T__6)
                self.state = 204
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 201
                    self.sep()
                    self.state = 206
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 216
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903756391903528) != 0):
                    self.state = 207
                    self.statement()
                    self.state = 211
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==11 or _la==61:
                        self.state = 208
                        self.sep()
                        self.state = 213
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 218
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [21]:
                localctx = MicelioParser.DefaultClauseContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 219
                self.match(MicelioParser.DEFECTO)
                self.state = 220
                self.match(MicelioParser.T__6)
                self.state = 224
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 221
                    self.sep()
                    self.state = 226
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 236
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903756391903528) != 0):
                    self.state = 227
                    self.statement()
                    self.state = 231
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==11 or _la==61:
                        self.state = 228
                        self.sep()
                        self.state = 233
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 238
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class While_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MIENTRAS(self):
            return self.getToken(MicelioParser.MIENTRAS, 0)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def block(self):
            return self.getTypedRuleContext(MicelioParser.BlockContext,0)


        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_while_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhile_stmt" ):
                listener.enterWhile_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhile_stmt" ):
                listener.exitWhile_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhile_stmt" ):
                return visitor.visitWhile_stmt(self)
            else:
                return visitor.visitChildren(self)




    def while_stmt(self):

        localctx = MicelioParser.While_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_while_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 241
            self.match(MicelioParser.MIENTRAS)
            self.state = 242
            self.match(MicelioParser.T__2)
            self.state = 243
            self.expr(0)
            self.state = 244
            self.match(MicelioParser.T__3)
            self.state = 248
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==61:
                self.state = 245
                self.sep()
                self.state = 250
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 251
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class For_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PARA(self):
            return self.getToken(MicelioParser.PARA, 0)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)


        def HASTA(self):
            return self.getToken(MicelioParser.HASTA, 0)

        def block(self):
            return self.getTypedRuleContext(MicelioParser.BlockContext,0)


        def INC(self):
            return self.getToken(MicelioParser.INC, 0)

        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)


        def EN(self):
            return self.getToken(MicelioParser.EN, 0)

        def getRuleIndex(self):
            return MicelioParser.RULE_for_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFor_stmt" ):
                listener.enterFor_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFor_stmt" ):
                listener.exitFor_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFor_stmt" ):
                return visitor.visitFor_stmt(self)
            else:
                return visitor.visitChildren(self)




    def for_stmt(self):

        localctx = MicelioParser.For_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_for_stmt)
        self._la = 0 # Token type
        try:
            self.state = 283
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 253
                self.match(MicelioParser.PARA)
                self.state = 254
                self.match(MicelioParser.ID)
                self.state = 255
                self.match(MicelioParser.T__1)
                self.state = 256
                self.expr(0)
                self.state = 257
                self.match(MicelioParser.HASTA)
                self.state = 258
                self.expr(0)
                self.state = 261
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==24:
                    self.state = 259
                    self.match(MicelioParser.INC)
                    self.state = 260
                    self.expr(0)


                self.state = 266
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 263
                    self.sep()
                    self.state = 268
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 269
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 271
                self.match(MicelioParser.PARA)
                self.state = 272
                self.match(MicelioParser.ID)
                self.state = 273
                self.match(MicelioParser.EN)
                self.state = 274
                self.expr(0)
                self.state = 278
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 275
                    self.sep()
                    self.state = 280
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 281
                self.block()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Func_defContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCION(self):
            return self.getToken(MicelioParser.FUNCION, 0)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def block(self):
            return self.getTypedRuleContext(MicelioParser.BlockContext,0)


        def param_list(self):
            return self.getTypedRuleContext(MicelioParser.Param_listContext,0)


        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_func_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunc_def" ):
                listener.enterFunc_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunc_def" ):
                listener.exitFunc_def(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunc_def" ):
                return visitor.visitFunc_def(self)
            else:
                return visitor.visitChildren(self)




    def func_def(self):

        localctx = MicelioParser.Func_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_func_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 285
            self.match(MicelioParser.FUNCION)
            self.state = 286
            self.match(MicelioParser.ID)
            self.state = 287
            self.match(MicelioParser.T__2)
            self.state = 289
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 577727389698621440) != 0):
                self.state = 288
                self.param_list()


            self.state = 291
            self.match(MicelioParser.T__3)
            self.state = 295
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==61:
                self.state = 292
                self.sep()
                self.state = 297
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 298
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Param_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.Param_itemContext)
            else:
                return self.getTypedRuleContext(MicelioParser.Param_itemContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_param_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam_list" ):
                listener.enterParam_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam_list" ):
                listener.exitParam_list(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam_list" ):
                return visitor.visitParam_list(self)
            else:
                return visitor.visitChildren(self)




    def param_list(self):

        localctx = MicelioParser.Param_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_param_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 300
            self.param_item()
            self.state = 305
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 301
                self.match(MicelioParser.T__0)
                self.state = 302
                self.param_item()
                self.state = 307
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Param_itemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MicelioParser.RULE_param_item

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ParamNormalContext(Param_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.Param_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamNormal" ):
                listener.enterParamNormal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamNormal" ):
                listener.exitParamNormal(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamNormal" ):
                return visitor.visitParamNormal(self)
            else:
                return visitor.visitChildren(self)


    class ParamArgsContext(Param_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.Param_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MUL(self):
            return self.getToken(MicelioParser.MUL, 0)
        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamArgs" ):
                listener.enterParamArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamArgs" ):
                listener.exitParamArgs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamArgs" ):
                return visitor.visitParamArgs(self)
            else:
                return visitor.visitChildren(self)


    class ParamKwargsContext(Param_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.Param_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def POW(self):
            return self.getToken(MicelioParser.POW, 0)
        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamKwargs" ):
                listener.enterParamKwargs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamKwargs" ):
                listener.exitParamKwargs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamKwargs" ):
                return visitor.visitParamKwargs(self)
            else:
                return visitor.visitChildren(self)



    def param_item(self):

        localctx = MicelioParser.Param_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_param_item)
        try:
            self.state = 313
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [59]:
                localctx = MicelioParser.ParamNormalContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 308
                self.match(MicelioParser.ID)
                pass
            elif token in [47]:
                localctx = MicelioParser.ParamArgsContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 309
                self.match(MicelioParser.MUL)
                self.state = 310
                self.match(MicelioParser.ID)
                pass
            elif token in [50]:
                localctx = MicelioParser.ParamKwargsContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 311
                self.match(MicelioParser.POW)
                self.state = 312
                self.match(MicelioParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.SepContext)
            else:
                return self.getTypedRuleContext(MicelioParser.SepContext,i)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.StatementContext)
            else:
                return self.getTypedRuleContext(MicelioParser.StatementContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = MicelioParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 315
            self.match(MicelioParser.T__4)
            self.state = 319
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==61:
                self.state = 316
                self.sep()
                self.state = 321
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 331
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903756391903528) != 0):
                self.state = 322
                self.statement()
                self.state = 326
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11 or _la==61:
                    self.state = 323
                    self.sep()
                    self.state = 328
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 333
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 334
            self.match(MicelioParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MicelioParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class MulDivModContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def MUL(self):
            return self.getToken(MicelioParser.MUL, 0)
        def DIV(self):
            return self.getToken(MicelioParser.DIV, 0)
        def MOD(self):
            return self.getToken(MicelioParser.MOD, 0)
        def DOTMUL(self):
            return self.getToken(MicelioParser.DOTMUL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDivMod" ):
                listener.enterMulDivMod(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDivMod" ):
                listener.exitMulDivMod(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulDivMod" ):
                return visitor.visitMulDivMod(self)
            else:
                return visitor.visitChildren(self)


    class MemberAccessContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemberAccess" ):
                listener.enterMemberAccess(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemberAccess" ):
                listener.exitMemberAccess(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMemberAccess" ):
                return visitor.visitMemberAccess(self)
            else:
                return visitor.visitChildren(self)


    class PipeExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def PIPE(self):
            return self.getToken(MicelioParser.PIPE, 0)
        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(MicelioParser.NEWLINE)
            else:
                return self.getToken(MicelioParser.NEWLINE, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipeExpr" ):
                listener.enterPipeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipeExpr" ):
                listener.exitPipeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPipeExpr" ):
                return visitor.visitPipeExpr(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def EQ(self):
            return self.getToken(MicelioParser.EQ, 0)
        def NE(self):
            return self.getToken(MicelioParser.NE, 0)
        def LT(self):
            return self.getToken(MicelioParser.LT, 0)
        def LE(self):
            return self.getToken(MicelioParser.LE, 0)
        def GT(self):
            return self.getToken(MicelioParser.GT, 0)
        def GE(self):
            return self.getToken(MicelioParser.GE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison" ):
                listener.enterComparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison" ):
                listener.exitComparison(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)


    class InExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def IN(self):
            return self.getToken(MicelioParser.IN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInExpr" ):
                listener.enterInExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInExpr" ):
                listener.exitInExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInExpr" ):
                return visitor.visitInExpr(self)
            else:
                return visitor.visitChildren(self)


    class OrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def O(self):
            return self.getToken(MicelioParser.O, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpr" ):
                listener.enterOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpr" ):
                listener.exitOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)


    class AddSubContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def PLUS(self):
            return self.getToken(MicelioParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(MicelioParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSub" ):
                listener.enterAddSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSub" ):
                listener.exitAddSub(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddSub" ):
                return visitor.visitAddSub(self)
            else:
                return visitor.visitChildren(self)


    class AnonFuncExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FUNCION(self):
            return self.getToken(MicelioParser.FUNCION, 0)
        def block(self):
            return self.getTypedRuleContext(MicelioParser.BlockContext,0)

        def param_list(self):
            return self.getTypedRuleContext(MicelioParser.Param_listContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnonFuncExpr" ):
                listener.enterAnonFuncExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnonFuncExpr" ):
                listener.exitAnonFuncExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnonFuncExpr" ):
                return visitor.visitAnonFuncExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class IndexExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndexExpr" ):
                listener.enterIndexExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndexExpr" ):
                listener.exitIndexExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndexExpr" ):
                return visitor.visitIndexExpr(self)
            else:
                return visitor.visitChildren(self)


    class PostIncDecContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)

        def INC_OP(self):
            return self.getToken(MicelioParser.INC_OP, 0)
        def DEC_OP(self):
            return self.getToken(MicelioParser.DEC_OP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostIncDec" ):
                listener.enterPostIncDec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostIncDec" ):
                listener.exitPostIncDec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostIncDec" ):
                return visitor.visitPostIncDec(self)
            else:
                return visitor.visitChildren(self)


    class NotExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NO(self):
            return self.getToken(MicelioParser.NO, 0)
        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotExpr" ):
                listener.enterNotExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotExpr" ):
                listener.exitNotExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpr" ):
                return visitor.visitNotExpr(self)
            else:
                return visitor.visitChildren(self)


    class LiteralExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(MicelioParser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralExpr" ):
                listener.enterLiteralExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralExpr" ):
                listener.exitLiteralExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralExpr" ):
                return visitor.visitLiteralExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnaryMinusContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MINUS(self):
            return self.getToken(MicelioParser.MINUS, 0)
        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryMinus" ):
                listener.enterUnaryMinus(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryMinus" ):
                listener.exitUnaryMinus(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryMinus" ):
                return visitor.visitUnaryMinus(self)
            else:
                return visitor.visitChildren(self)


    class DictExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DICT(self):
            return self.getToken(MicelioParser.DICT, 0)
        def keyValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.KeyValueContext)
            else:
                return self.getTypedRuleContext(MicelioParser.KeyValueContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictExpr" ):
                listener.enterDictExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictExpr" ):
                listener.exitDictExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictExpr" ):
                return visitor.visitDictExpr(self)
            else:
                return visitor.visitChildren(self)


    class MapLiteralContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def keyValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.KeyValueContext)
            else:
                return self.getTypedRuleContext(MicelioParser.KeyValueContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMapLiteral" ):
                listener.enterMapLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMapLiteral" ):
                listener.exitMapLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMapLiteral" ):
                return visitor.visitMapLiteral(self)
            else:
                return visitor.visitChildren(self)


    class PowExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def POW(self):
            return self.getToken(MicelioParser.POW, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPowExpr" ):
                listener.enterPowExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPowExpr" ):
                listener.exitPowExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPowExpr" ):
                return visitor.visitPowExpr(self)
            else:
                return visitor.visitChildren(self)


    class CallExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)

        def exprList(self):
            return self.getTypedRuleContext(MicelioParser.ExprListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallExpr" ):
                listener.enterCallExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallExpr" ):
                listener.exitCallExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCallExpr" ):
                return visitor.visitCallExpr(self)
            else:
                return visitor.visitChildren(self)


    class ListExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListExpr" ):
                listener.enterListExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListExpr" ):
                listener.exitListExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListExpr" ):
                return visitor.visitListExpr(self)
            else:
                return visitor.visitChildren(self)


    class SetExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SET(self):
            return self.getToken(MicelioParser.SET, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetExpr" ):
                listener.enterSetExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetExpr" ):
                listener.exitSetExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetExpr" ):
                return visitor.visitSetExpr(self)
            else:
                return visitor.visitChildren(self)


    class PreIncDecContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)

        def INC_OP(self):
            return self.getToken(MicelioParser.INC_OP, 0)
        def DEC_OP(self):
            return self.getToken(MicelioParser.DEC_OP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreIncDec" ):
                listener.enterPreIncDec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreIncDec" ):
                listener.exitPreIncDec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPreIncDec" ):
                return visitor.visitPreIncDec(self)
            else:
                return visitor.visitChildren(self)


    class IdExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(MicelioParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdExpr" ):
                listener.enterIdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdExpr" ):
                listener.exitIdExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdExpr" ):
                return visitor.visitIdExpr(self)
            else:
                return visitor.visitChildren(self)


    class MatrizExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MATRIZ(self):
            return self.getToken(MicelioParser.MATRIZ, 0)
        def expr(self):
            return self.getTypedRuleContext(MicelioParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMatrizExpr" ):
                listener.enterMatrizExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMatrizExpr" ):
                listener.exitMatrizExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMatrizExpr" ):
                return visitor.visitMatrizExpr(self)
            else:
                return visitor.visitChildren(self)


    class AndExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MicelioParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)

        def Y(self):
            return self.getToken(MicelioParser.Y, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpr" ):
                listener.enterAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpr" ):
                listener.exitAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MicelioParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 44
        self.enterRecursionRule(localctx, 44, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 411
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [35, 36, 57, 58]:
                localctx = MicelioParser.LiteralExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 337
                self.literal()
                pass
            elif token in [59]:
                localctx = MicelioParser.IdExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 338
                self.match(MicelioParser.ID)
                pass
            elif token in [3]:
                localctx = MicelioParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 339
                self.match(MicelioParser.T__2)
                self.state = 340
                self.expr(0)
                self.state = 341
                self.match(MicelioParser.T__3)
                pass
            elif token in [8]:
                localctx = MicelioParser.ListExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 343
                self.match(MicelioParser.T__7)
                self.state = 352
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903752159117608) != 0):
                    self.state = 344
                    self.expr(0)
                    self.state = 349
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==1:
                        self.state = 345
                        self.match(MicelioParser.T__0)
                        self.state = 346
                        self.expr(0)
                        self.state = 351
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 354
                self.match(MicelioParser.T__8)
                pass
            elif token in [33]:
                localctx = MicelioParser.SetExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 355
                self.match(MicelioParser.SET)
                self.state = 356
                self.match(MicelioParser.T__2)
                self.state = 365
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903752159117608) != 0):
                    self.state = 357
                    self.expr(0)
                    self.state = 362
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==1:
                        self.state = 358
                        self.match(MicelioParser.T__0)
                        self.state = 359
                        self.expr(0)
                        self.state = 364
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 367
                self.match(MicelioParser.T__3)
                pass
            elif token in [34]:
                localctx = MicelioParser.DictExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 368
                self.match(MicelioParser.DICT)
                self.state = 369
                self.match(MicelioParser.T__2)
                self.state = 378
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903752159117608) != 0):
                    self.state = 370
                    self.keyValue()
                    self.state = 375
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==1:
                        self.state = 371
                        self.match(MicelioParser.T__0)
                        self.state = 372
                        self.keyValue()
                        self.state = 377
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 380
                self.match(MicelioParser.T__3)
                pass
            elif token in [5]:
                localctx = MicelioParser.MapLiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 381
                self.match(MicelioParser.T__4)
                self.state = 390
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903752159117608) != 0):
                    self.state = 382
                    self.keyValue()
                    self.state = 387
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==1:
                        self.state = 383
                        self.match(MicelioParser.T__0)
                        self.state = 384
                        self.keyValue()
                        self.state = 389
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 392
                self.match(MicelioParser.T__5)
                pass
            elif token in [14]:
                localctx = MicelioParser.AnonFuncExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 393
                self.match(MicelioParser.FUNCION)
                self.state = 394
                self.match(MicelioParser.T__2)
                self.state = 396
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 577727389698621440) != 0):
                    self.state = 395
                    self.param_list()


                self.state = 398
                self.match(MicelioParser.T__3)
                self.state = 399
                self.block()
                pass
            elif token in [15]:
                localctx = MicelioParser.MatrizExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 400
                self.match(MicelioParser.MATRIZ)
                self.state = 401
                self.match(MicelioParser.T__2)
                self.state = 402
                self.expr(0)
                self.state = 403
                self.match(MicelioParser.T__3)
                pass
            elif token in [43, 44]:
                localctx = MicelioParser.PreIncDecContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 405
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==43 or _la==44):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 406
                self.expr(13)
                pass
            elif token in [46]:
                localctx = MicelioParser.UnaryMinusContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 407
                self.match(MicelioParser.MINUS)
                self.state = 408
                self.expr(11)
                pass
            elif token in [39]:
                localctx = MicelioParser.NotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 409
                self.match(MicelioParser.NO)
                self.state = 410
                self.expr(10)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 467
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,51,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 465
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,50,self._ctx)
                    if la_ == 1:
                        localctx = MicelioParser.MulDivModContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 413
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 414
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 989560464998400) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 415
                        self.expr(10)
                        pass

                    elif la_ == 2:
                        localctx = MicelioParser.AddSubContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 416
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 417
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==45 or _la==46):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 418
                        self.expr(9)
                        pass

                    elif la_ == 3:
                        localctx = MicelioParser.PowExprContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 419
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 420
                        localctx.op = self.match(MicelioParser.POW)
                        self.state = 421
                        self.expr(8)
                        pass

                    elif la_ == 4:
                        localctx = MicelioParser.ComparisonContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 422
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 423
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 141863388262170624) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 424
                        self.expr(7)
                        pass

                    elif la_ == 5:
                        localctx = MicelioParser.AndExprContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 425
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 426
                        self.match(MicelioParser.Y)
                        self.state = 427
                        self.expr(6)
                        pass

                    elif la_ == 6:
                        localctx = MicelioParser.OrExprContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 428
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 429
                        self.match(MicelioParser.O)
                        self.state = 430
                        self.expr(5)
                        pass

                    elif la_ == 7:
                        localctx = MicelioParser.InExprContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 431
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 432
                        self.match(MicelioParser.IN)
                        self.state = 433
                        self.expr(4)
                        pass

                    elif la_ == 8:
                        localctx = MicelioParser.PipeExprContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 434
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 438
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==61:
                            self.state = 435
                            self.match(MicelioParser.NEWLINE)
                            self.state = 440
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 441
                        self.match(MicelioParser.PIPE)
                        self.state = 445
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==61:
                            self.state = 442
                            self.match(MicelioParser.NEWLINE)
                            self.state = 447
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 448
                        self.expr(3)
                        pass

                    elif la_ == 9:
                        localctx = MicelioParser.IndexExprContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 449
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 450
                        self.match(MicelioParser.T__7)
                        self.state = 451
                        self.expr(0)
                        self.state = 452
                        self.match(MicelioParser.T__8)
                        pass

                    elif la_ == 10:
                        localctx = MicelioParser.CallExprContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 454
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 455
                        self.match(MicelioParser.T__2)
                        self.state = 457
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008903752159117608) != 0):
                            self.state = 456
                            self.exprList()


                        self.state = 459
                        self.match(MicelioParser.T__3)
                        pass

                    elif la_ == 11:
                        localctx = MicelioParser.PostIncDecContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 460
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 461
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==43 or _la==44):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

                    elif la_ == 12:
                        localctx = MicelioParser.MemberAccessContext(self, MicelioParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 462
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 463
                        self.match(MicelioParser.T__9)
                        self.state = 464
                        self.match(MicelioParser.ID)
                        pass

             
                self.state = 469
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,51,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class KeyValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_keyValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeyValue" ):
                listener.enterKeyValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeyValue" ):
                listener.exitKeyValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeyValue" ):
                return visitor.visitKeyValue(self)
            else:
                return visitor.visitChildren(self)




    def keyValue(self):

        localctx = MicelioParser.KeyValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_keyValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 470
            self.expr(0)
            self.state = 471
            self.match(MicelioParser.T__6)
            self.state = 472
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MicelioParser.ExprContext)
            else:
                return self.getTypedRuleContext(MicelioParser.ExprContext,i)


        def getRuleIndex(self):
            return MicelioParser.RULE_exprList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprList" ):
                listener.enterExprList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprList" ):
                listener.exitExprList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprList" ):
                return visitor.visitExprList(self)
            else:
                return visitor.visitChildren(self)




    def exprList(self):

        localctx = MicelioParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_exprList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 474
            self.expr(0)
            self.state = 479
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 475
                self.match(MicelioParser.T__0)
                self.state = 476
                self.expr(0)
                self.state = 481
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(MicelioParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(MicelioParser.STRING, 0)

        def BOOL(self):
            return self.getToken(MicelioParser.BOOL, 0)

        def NULL(self):
            return self.getToken(MicelioParser.NULL, 0)

        def getRuleIndex(self):
            return MicelioParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = MicelioParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 482
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 432345667306782720) != 0)):
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


    class SepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(MicelioParser.NEWLINE)
            else:
                return self.getToken(MicelioParser.NEWLINE, i)

        def getRuleIndex(self):
            return MicelioParser.RULE_sep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSep" ):
                listener.enterSep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSep" ):
                listener.exitSep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSep" ):
                return visitor.visitSep(self)
            else:
                return visitor.visitChildren(self)




    def sep(self):

        localctx = MicelioParser.SepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_sep)
        try:
            self.state = 490
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 484
                self.match(MicelioParser.T__10)
                pass
            elif token in [61]:
                self.enterOuterAlt(localctx, 2)
                self.state = 486 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 485
                        self.match(MicelioParser.NEWLINE)

                    else:
                        raise NoViableAltException(self)
                    self.state = 488 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,53,self._ctx)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[22] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 1)
         




