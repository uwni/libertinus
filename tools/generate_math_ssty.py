"""Build LibertinaMath-Regular.sfd from LibertinusMath-Regular.sfd.

Single authoritative build script. Always reads the original Libertinus Math
source and writes a fresh LibertinaMath. Steps in order:

  1. Rename font metadata  (Libertinus → Libertina)
  2. Scale math italic base glyphs ×1.08 horizontally
  3. Generate .st / .sts ssty variants from the scaled base glyphs,
     deleting orphaned .ssty glyphs along the way
  4. Rewrite sources/features/ssty.fea

── Step 2: italic base scaling ─────────────────────────────────────────────────
Scaled Unicode ranges:
  U+210E–U+210F    ℎ (Planck h) and ℏ (h-bar)
  U+1D434–U+1D467  Mathematical Italic Latin (A-Z, a-z)
  U+1D468–U+1D49B  Mathematical Bold Italic Latin (A-Z, a-z)
  U+1D6A4–U+1D6A5  Mathematical Italic Dotless i and j
  U+1D6E2–U+1D71B  Mathematical Italic Greek
  U+1D71C–U+1D755  Mathematical Bold Italic Greek

Excluded (oblique — ink width matches upright):
  U+1D608–U+1D63B  Sans-Serif Italic Latin
  U+1D63C–U+1D66F  Sans-Serif Bold Italic Latin
  U+1D790–U+1D7C9  Sans-Serif Bold Italic Greek

── Step 3: ssty ────────────────────────────────────────────────────────────────
Coverage and glyph order follow NewCM Math (NEWCM_BASES, 1229 entries).

Width ratios by category (derived from NewCM ink-width statistics):
  Category           ST     STS
  math_italic      1.089  1.213
  math_bold_italic 1.094  1.223
  latin            1.086  1.219
  math_bold        1.076  1.187
  math_fraktur     1.090  1.200
  math_script      1.070  1.143
  operators        1.089  1.212
  digits_unicode   1.075  1.157
  digits_named     1.107  1.250
  greek            1.115  1.268

Height ratios via ncm_y(): rule-based from NewCM design patterns.
"""

import datetime
import os
import re
import unicodedata
from collections import defaultdict

try:
    import fontforge  # type: ignore[import]
    import psMat      # type: ignore[import]
except ImportError:
    raise SystemExit(
        "fontforge and psMat are only available inside FontForge's Python.\n"
        f"Run with:  fontforge -script {__file__}"
    )

SOURCES  = os.path.join(os.path.dirname(__file__), "..", "sources")
SFD_IN   = os.path.join(SOURCES, "LibertinusMath-Regular.sfd")
SFD_OUT  = os.path.join(SOURCES, "LibertinaMath-Regular.sfd")
SSTY_FEA = os.path.join(SOURCES, "features", "ssty.fea")

BASE_SCALE = 1.07  # italic base horizontal widening

ITALIC_RANGES = [
    (0x210E,  0x210F),
    (0x1D434, 0x1D467),
    (0x1D468, 0x1D49B),
    (0x1D6A4, 0x1D6A5),
    (0x1D6E2, 0x1D71B),
    (0x1D71C, 0x1D755),
]

SSTY_RATIOS = {
    "math_italic":      (1.089, 1.213),
    "math_bold_italic": (1.094, 1.223),
    "latin":            (1.086, 1.219),
    "math_bold":        (1.076, 1.187),
    "math_fraktur":     (1.090, 1.200),
    "math_script":      (1.070, 1.143),
    "operators":        (1.089, 1.212),
    "digits_unicode":   (1.075, 1.157),
    "digits_named":     (1.107, 1.250),
    "greek":            (1.115, 1.268),
    "default":          (1.088, 1.211),
}

DIGIT_NAMES = {
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
}

# ── NewCM Math ssty data ──────────────────────────────────────────────────────
# Ordered list of base glyph names covered by NewCM's ssty feature.
# Source: AlternateSubs2 entries in NewCMMath-Regular.sfd (1229 glyphs).
NEWCM_BASES = (
    "exclam", "quotedbl", "numbersign", "dollar", "percent", "ampersand",
    "quotesingle", "plus", "comma", "hyphen", "period", "slash",
    "zero", "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "colon", "semicolon", "question", "at",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "asciicircum", "underscore", "grave",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "asciitilde", "exclamdown", "cent", "sterling", "currency", "yen",
    "brokenbar", "section", "dieresis", "copyright", "ordfeminine",
    "guillemotleft", "registered", "macron", "degree", "plusminus",
    "acute", "uni00B5", "paragraph", "cedilla", "ordmasculine",
    "guillemotright", "questiondown",
    "Agrave", "Aacute", "Acircumflex", "Atilde", "Adieresis", "Aring",
    "AE", "Ccedilla", "Egrave", "Eacute", "Ecircumflex", "Edieresis",
    "Igrave", "Iacute", "Icircumflex", "Idieresis", "Eth", "Ntilde",
    "Ograve", "Oacute", "Ocircumflex", "Otilde", "Odieresis", "multiply",
    "Oslash", "Ugrave", "Uacute", "Ucircumflex", "Udieresis", "Yacute",
    "Thorn", "germandbls",
    "agrave", "aacute", "acircumflex", "atilde", "adieresis", "aring",
    "ae", "ccedilla", "egrave", "eacute", "ecircumflex", "edieresis",
    "igrave", "iacute", "icircumflex", "idieresis", "eth", "ntilde",
    "ograve", "oacute", "ocircumflex", "otilde", "odieresis", "divide",
    "oslash", "ugrave", "uacute", "ucircumflex", "udieresis", "yacute",
    "thorn", "ydieresis",
    "Amacron", "amacron", "Abreve", "abreve", "Aogonek", "aogonek",
    "Cacute", "cacute", "Ccaron", "ccaron", "Dcaron", "dcaron", "Dcroat",
    "Emacron", "emacron", "Edotaccent", "edotaccent", "Eogonek", "eogonek",
    "Ecaron", "ecaron", "Gbreve", "gbreve", "Gcommaaccent", "gcommaaccent",
    "Itilde", "itilde", "Imacron", "imacron", "Iogonek", "iogonek",
    "Idotaccent", "dotlessi", "I_J", "i_j",
    "Kcommaaccent", "kcommaaccent", "Lacute", "lacute",
    "Lcommaaccent", "lcommaaccent", "Lcaron", "lcaron", "Lslash", "lslash",
    "Nacute", "nacute", "Ncommaaccent", "ncommaaccent", "Ncaron", "ncaron",
    "Eng", "eng", "Omacron", "omacron", "Ohungarumlaut", "ohungarumlaut",
    "OE", "oe", "Racute", "racute", "Rcommaaccent", "rcommaaccent",
    "Rcaron", "rcaron", "Sacute", "sacute", "Scedilla", "scedilla",
    "Scaron", "scaron", "Tcedilla", "tcedilla", "Tcaron", "tcaron",
    "Utilde", "utilde", "Umacron", "umacron", "Uring", "uring",
    "Uhungarumlaut", "uhungarumlaut", "Uogonek", "uogonek", "Ydieresis",
    "Zacute", "zacute", "Zdotaccent", "zdotaccent", "Zcaron", "zcaron",
    "longs", "Ohorn", "ohorn", "Uhorn", "uhorn",
    "uni0218", "uni0219", "uni021A", "uni021B",
    "dotlessj", "circumflex", "caron", "breve", "dotaccent", "ring",
    "ogonek", "tilde", "hungarumlaut",
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho",
    "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
    "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
    "uni03C2", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
    "uni03D1", "uni03D5", "uni03D6", "uni03F0", "uni03F1", "uni03F4", "uni03F5",
    "Adotbelow", "adotbelow", "Ahookabove", "ahookabove",
    "Acircumflexacute", "acircumflexacute", "Acircumflexgrave", "acircumflexgrave",
    "Acircumflexhookabove", "acircumflexhookabove",
    "Acircumflextilde", "acircumflextilde",
    "Acircumflexdotbelow", "acircumflexdotbelow",
    "Abreveacute", "abreveacute", "Abrevegrave", "abrevegrave",
    "Abrevehookabove", "abrevehookabove", "Abrevetilde", "abrevetilde",
    "Abrevedotbelow", "abrevedotbelow",
    "Edotbelow", "edotbelow", "Ehookabove", "ehookabove",
    "Etilde", "etilde",
    "Ecircumflexacute", "ecircumflexacute", "Ecircumflexgrave", "ecircumflexgrave",
    "Ecircumflexhookabove", "ecircumflexhookabove",
    "Ecircumflextilde", "ecircumflextilde",
    "Ecircumflexdotbelow", "ecircumflexdotbelow",
    "Ihookabove", "ihookabove", "Idotbelow", "idotbelow",
    "Odotbelow", "odotbelow", "Ohookabove", "ohookabove",
    "Ocircumflexacute", "ocircumflexacute", "Ocircumflexgrave", "ocircumflexgrave",
    "Ocircumflexhookabove", "ocircumflexhookabove",
    "Ocircumflextilde", "ocircumflextilde",
    "Ocircumflexdotbelow", "ocircumflexdotbelow",
    "Ohornacute", "ohornacute", "Ohorngrave", "ohorngrave",
    "Ohornhookabove", "ohornhookabove", "Ohorntilde", "ohorntilde",
    "Ohorndotbelow", "ohorndotbelow",
    "Udotbelow", "udotbelow", "Uhookabove", "uhookabove",
    "Uhornacute", "uhornacute", "Uhorngrave", "uhorngrave",
    "Uhornhookabove", "uhornhookabove", "Uhorntilde", "uhorntilde",
    "Uhorndotbelow", "uhorndotbelow",
    "Ygrave", "ygrave", "Ydotbelow", "ydotbelow",
    "Yhookabove", "yhookabove", "Ytilde", "ytilde",
    "endash", "emdash", "quoteleft", "quoteright", "quotesinglbase",
    "quotedblleft", "quotedblright", "quotedblbase",
    "dagger", "daggerdbl", "perthousand", "permyriad",
    "minute", "uni2033", "uni2034", "primereversed", "uni2036", "uni2037",
    "guilsinglleft", "guilsinglright", "referencemark", "uni203D",
    "discount", "uni2057",
    "colonmonetary", "Euro", "uni210C", "uni210E", "uni2111", "uni2113",
    "numero", "published", "uni211C", "recipe", "servicemark", "trademark",
    "uni2126", "uni2127", "uni2128", "uni212D", "estimated",
    "aleph", "uni2136", "uni2137", "uni2138",
    "partialdiff", "uni2206", "nabla", "minus", "minusplus", "uni2214",
    "uni2215", "asteriskmath", "uni2218", "proportional", "infinity",
    "uni2238", "circleplus", "uni2296", "circlemultiply", "circledivide",
    "circledot", "uni229A", "uni229B",
    "uni22C4", "uni22C5", "uni22C6", "uni22C7", "uni22D5",
    "blanksymbol", "uni2423", "musicalnote",
    "married", "divorced", "uni27C2", "uni29F5",
    "uni2A22", "uni2A23", "uni2A24", "uni2A25", "uni2A26", "uni2A27",
    "uni2A28", "uni2A29", "uni2A2A", "uni2A2B", "uni2A2C", "uni2A2D",
    "uni2A2E", "uni2A2F", "uni2A30", "uni2A31", "uni2A32", "uni2A33",
    "uni2A34", "uni2A35", "uni2A36", "uni2A37", "uni2A38", "uni2A39",
    "uni2A3A", "uni2A3B", "uni2E18",
    "f_f", "f_i", "f_l", "f_f_i", "f_f_l",
    "u1D400", "u1D401", "u1D402", "u1D403", "u1D404", "u1D405", "u1D406",
    "u1D407", "u1D408", "u1D409", "u1D40A", "u1D40B", "u1D40C", "u1D40D",
    "u1D40E", "u1D40F", "u1D410", "u1D411", "u1D412", "u1D413", "u1D414",
    "u1D415", "u1D416", "u1D417", "u1D418", "u1D419",
    "u1D41A", "u1D41B", "u1D41C", "u1D41D", "u1D41E", "u1D41F", "u1D420",
    "u1D421", "u1D422", "u1D423", "u1D424", "u1D425", "u1D426", "u1D427",
    "u1D428", "u1D429", "u1D42A", "u1D42B", "u1D42C", "u1D42D", "u1D42E",
    "u1D42F", "u1D430", "u1D431", "u1D432", "u1D433",
    "u1D434", "u1D435", "u1D436", "u1D437", "u1D438", "u1D439", "u1D43A",
    "u1D43B", "u1D43C", "u1D43D", "u1D43E", "u1D43F", "u1D440", "u1D441",
    "u1D442", "u1D443", "u1D444", "u1D445", "u1D446", "u1D447", "u1D448",
    "u1D449", "u1D44A", "u1D44B", "u1D44C", "u1D44D",
    "u1D44E", "u1D44F", "u1D450", "u1D451", "u1D452", "u1D453", "u1D454",
    "u1D456", "u1D457", "u1D458", "u1D459", "u1D45A", "u1D45B", "u1D45C",
    "u1D45D", "u1D45E", "u1D45F", "u1D460", "u1D461", "u1D462", "u1D463",
    "u1D464", "u1D465", "u1D466", "u1D467",
    "u1D468", "u1D469", "u1D46A", "u1D46B", "u1D46C", "u1D46D", "u1D46E",
    "u1D46F", "u1D470", "u1D471", "u1D472", "u1D473", "u1D474", "u1D475",
    "u1D476", "u1D477", "u1D478", "u1D479", "u1D47A", "u1D47B", "u1D47C",
    "u1D47D", "u1D47E", "u1D47F", "u1D480", "u1D481",
    "u1D482", "u1D483", "u1D484", "u1D485", "u1D486", "u1D487", "u1D488",
    "u1D489", "u1D48A", "u1D48B", "u1D48C", "u1D48D", "u1D48E", "u1D48F",
    "u1D490", "u1D491", "u1D492", "u1D493", "u1D494", "u1D495", "u1D496",
    "u1D497", "u1D498", "u1D499", "u1D49A", "u1D49B",
    "u1D504", "u1D505", "u1D507", "u1D508", "u1D509", "u1D50A", "u1D50D",
    "u1D50E", "u1D50F", "u1D510", "u1D511", "u1D512", "u1D513", "u1D514",
    "u1D516", "u1D517", "u1D518", "u1D519", "u1D51A", "u1D51B", "u1D51C",
    "u1D51E", "u1D51F", "u1D520", "u1D521", "u1D522", "u1D523", "u1D524",
    "u1D525", "u1D526", "u1D527", "u1D528", "u1D529", "u1D52A", "u1D52B",
    "u1D52C", "u1D52D", "u1D52E", "u1D52F", "u1D530", "u1D531", "u1D532",
    "u1D533", "u1D534", "u1D535", "u1D536", "u1D537",
    "u1D56C", "u1D56D", "u1D56E", "u1D56F", "u1D570", "u1D571", "u1D572",
    "u1D573", "u1D574", "u1D575", "u1D576", "u1D577", "u1D578", "u1D579",
    "u1D57A", "u1D57B", "u1D57C", "u1D57D", "u1D57E", "u1D57F", "u1D580",
    "u1D581", "u1D582", "u1D583", "u1D584", "u1D585", "u1D586", "u1D587",
    "u1D588", "u1D589", "u1D58A", "u1D58B", "u1D58C", "u1D58D", "u1D58E",
    "u1D58F", "u1D590", "u1D591", "u1D592", "u1D593", "u1D594", "u1D595",
    "u1D596", "u1D597", "u1D598", "u1D599", "u1D59A", "u1D59B", "u1D59C",
    "u1D59D", "u1D59E", "u1D59F",
    "u1D6A4", "u1D6A5",
    "u1D6A8", "u1D6A9", "u1D6AA", "u1D6AB", "u1D6AC", "u1D6AD", "u1D6AE",
    "u1D6AF", "u1D6B0", "u1D6B1", "u1D6B2", "u1D6B3", "u1D6B4", "u1D6B5",
    "u1D6B6", "u1D6B7", "u1D6B8", "u1D6B9", "u1D6BA", "u1D6BB", "u1D6BC",
    "u1D6BD", "u1D6BE", "u1D6BF", "u1D6C0", "u1D6C1", "u1D6C2", "u1D6C3",
    "u1D6C4", "u1D6C5", "u1D6C6", "u1D6C7", "u1D6C8", "u1D6C9", "u1D6CA",
    "u1D6CB", "u1D6CC", "u1D6CD", "u1D6CE", "u1D6CF", "u1D6D0", "u1D6D1",
    "u1D6D2", "u1D6D3", "u1D6D4", "u1D6D5", "u1D6D6", "u1D6D7", "u1D6D8",
    "u1D6D9", "u1D6DA", "u1D6DB", "u1D6DC", "u1D6DD", "u1D6DE", "u1D6DF",
    "u1D6E0", "u1D6E1",
    "u1D6E2", "u1D6E3", "u1D6E4", "u1D6E5", "u1D6E6", "u1D6E7", "u1D6E8",
    "u1D6E9", "u1D6EA", "u1D6EB", "u1D6EC", "u1D6ED", "u1D6EE", "u1D6EF",
    "u1D6F0", "u1D6F1", "u1D6F2", "u1D6F3", "u1D6F4", "u1D6F5", "u1D6F6",
    "u1D6F7", "u1D6F8", "u1D6F9", "u1D6FA", "u1D6FB",
    "u1D6FC", "u1D6FD", "u1D6FE", "u1D6FF", "u1D700", "u1D701", "u1D702",
    "u1D703", "u1D704", "u1D705", "u1D706", "u1D707", "u1D708", "u1D709",
    "u1D70A", "u1D70B", "u1D70C", "u1D70D", "u1D70E", "u1D70F", "u1D710",
    "u1D711", "u1D712", "u1D713", "u1D714", "u1D715", "u1D716", "u1D717",
    "u1D718", "u1D719", "u1D71A", "u1D71B",
    "u1D71C", "u1D71D", "u1D71E", "u1D71F", "u1D720", "u1D721", "u1D722",
    "u1D723", "u1D724", "u1D725", "u1D726", "u1D727", "u1D728", "u1D729",
    "u1D72A", "u1D72B", "u1D72C", "u1D72D", "u1D72E", "u1D72F", "u1D730",
    "u1D731", "u1D732", "u1D733", "u1D734", "u1D735",
    "u1D736", "u1D737", "u1D738", "u1D739", "u1D73A", "u1D73B", "u1D73C",
    "u1D73D", "u1D73E", "u1D73F", "u1D740", "u1D741", "u1D742", "u1D743",
    "u1D744", "u1D745", "u1D746", "u1D747", "u1D748", "u1D749", "u1D74A",
    "u1D74B", "u1D74C", "u1D74D", "u1D74E", "u1D74F", "u1D750", "u1D751",
    "u1D752", "u1D753", "u1D754", "u1D755",
    "u1D7CE", "u1D7CF", "u1D7D0", "u1D7D1", "u1D7D2", "u1D7D3", "u1D7D4",
    "u1D7D5", "u1D7D6", "u1D7D7",
    "star.alt", "space_uni0326", "copyleft", "space_uni030F", "died",
    "space_uni0323", "f_k", "S_S", "space_uni0309", "leaf",
    "perthousandzero", "threequartersemdash", "asciitilde.low", "emdash.alt",
    "space_uni0331",
    "dotlessi.mrmb", "dotlessj.mrmb", "dotlessi.mitb", "dotlessj.mitb",
    "dotlessi.fra", "dotlessj.fra", "dotlessi.frab", "dotlessj.frab",
    "u1D49C.alt", "uni212C.alt", "u1D49E.alt", "u1D49F.alt",
    "uni2130.alt", "uni2131.alt", "u1D4A2.alt", "uni210B.alt", "uni2110.alt",
    "u1D4A5.alt", "u1D4A6.alt", "uni2112.alt", "uni2133.alt",
    "u1D4A9.alt", "u1D4AA.alt", "u1D4AB.alt", "u1D4AC.alt", "uni211B.alt",
    "u1D4AE.alt", "u1D4AF.alt", "u1D4B0.alt", "u1D4B1.alt",
    "u1D4B2.alt", "u1D4B3.alt", "u1D4B4.alt", "u1D4B5.alt",
    "u1D4D0.alt", "u1D4D1.alt", "u1D4D2.alt", "u1D4D3.alt", "u1D4D4.alt",
    "u1D4D5.alt", "u1D4D6.alt", "u1D4D7.alt", "u1D4D8.alt", "u1D4D9.alt",
    "u1D4DA.alt", "u1D4DB.alt", "u1D4DC.alt", "u1D4DD.alt", "u1D4DE.alt",
    "u1D4DF.alt", "u1D4E0.alt", "u1D4E1.alt", "u1D4E2.alt", "u1D4E3.alt",
    "u1D4E4.alt", "u1D4E5.alt", "u1D4E6.alt", "u1D4E7.alt",
    "u1D4E8.alt", "u1D4E9.alt",
    "uni0966", "uni0967", "uni0968", "uni0969", "uni096A", "uni096B",
    "uni096C", "uni096D", "uni096E", "uni096F",
    "uni0900", "uni0901", "uni0902", "uni0903", "uni0904", "uni0905",
    "uni0906", "uni0907", "uni0908", "uni0909", "uni090A", "uni090B",
    "uni090C", "uni090D", "uni090E", "uni090F", "uni0910", "uni0911",
    "uni0912", "uni0913", "uni0914", "uni0915", "uni0916", "uni0917",
    "uni0918", "uni0919", "uni091A", "uni091B", "uni091C", "uni091D",
    "uni091E", "uni091F", "uni0920", "uni0921", "uni0922", "uni0923",
    "uni0924", "uni0925", "uni0926", "uni0927", "uni0928", "uni0929",
    "uni092A", "uni092B", "uni092C", "uni092D", "uni092E", "uni092F",
    "uni0930", "uni0931", "uni0932", "uni0933", "uni0934", "uni0935",
    "uni0936", "uni0937", "uni0938", "uni0939", "uni093A", "uni093B",
    "uni093C", "uni093D", "uni093E", "uni093F", "uni0940", "uni0941",
    "uni0942", "uni0943", "uni0944", "uni0945", "uni0946", "uni0947",
    "uni0948", "uni0949", "uni094A", "uni094B", "uni094C", "uni094D",
    "uni094E", "uni094F", "uni0950", "uni0951", "uni0952", "uni0953",
    "uni0954", "uni0955", "uni0956", "uni0957", "uni0958", "uni0959",
    "uni095A", "uni095B", "uni095C", "uni095D", "uni095E", "uni095F",
    "uni0960", "uni0961", "uni0962", "uni0963", "uni0964", "uni0965",
    "uni0970", "uni0971", "uni0972", "uni0973", "uni0974", "uni0975",
    "uni0976", "uni0977", "uni0978", "uni0979", "uni097A", "uni097B",
    "uni097C", "uni097D", "uni097E", "uni097F",
    "uniE036", "uni0030.alt",
    "u1D4D0", "u1D4D1", "u1D4D2", "u1D4D3", "u1D4D4", "u1D4D5", "u1D4D6",
    "u1D4D7", "u1D4D8", "u1D4D9", "u1D4DA", "u1D4DB", "u1D4DC", "u1D4DD",
    "u1D4DE", "u1D4DF", "u1D4E0", "u1D4E1", "u1D4E2", "u1D4E3", "u1D4E4",
    "u1D4E5", "u1D4E6", "u1D4E7", "u1D4E8", "u1D4E9",
    "u1D49C", "u1D49E", "u1D49F", "u1D4A2", "u1D4A5", "u1D4A6",
    "u1D4A9", "u1D4AA", "u1D4AB", "u1D4AC", "u1D4AE", "u1D4AF",
    "u1D4B0", "u1D4B1", "u1D4B2", "u1D4B3", "u1D4B4", "u1D4B5",
    "uni210B", "uni2110", "uni2112", "uni212C", "uni2130", "uni2131",
    "uni2133", "uni211B",
)

# ── NewCM height-ratio rules ─────────────────────────────────────────────────
# Derived from NewCMMath bounding-box measurements. Rules are expressed as
# glyph-class patterns rather than per-glyph entries.

# Latin uppercase: letters deviating from the default (1.0, 1.0)
_UPP_ST  = dict.fromkeys("CGOS",  0.9945)   | {"A": 0.99581} | \
           dict.fromkeys("JRUVW", 0.9972)   | dict.fromkeys("EF", 0.99853) | \
           {"T": 0.99852, "Q": 0.99778}
_UPP_STS = dict.fromkeys("EF", 0.99853) | {"T": 0.99705}

# Latin lowercase: by height role
_LOW_ST  = dict.fromkeys("acemnorsuxz", 0.99558) | \
           dict.fromkeys("bdkl",        0.99858) | \
           dict.fromkeys("gy",          0.99691) | \
           dict.fromkeys("pq",          0.99843) | \
           {"f": 0.9978, "t": 0.99686,
            "v": 0.99779, "w": 0.99779,
            "i": 1.00149, "j": 1.00115}
_LOW_STS = {"b": 0.99908, "d": 0.99908, "k": 0.99908, "l": 0.99908,
            "v": 1.00221, "w": 1.00221,
            "i": 1.00893, "j": 1.00693}

# Operators/symbols with significant non-unity ratios (|ratio-1| > 0.01)
_OP_Y = {
    "hyphen":              (1.17241, 1.32759),
    "endash":              (1.27273, 1.5),
    "emdash":              (1.27273, 1.5),
    "emdash.alt":          (1.27273, 1.54545),
    "threequartersemdash": (1.27273, 1.5),
    "macron":              (1.22581, 1.41935),
    "underscore":          (1.2,     1.4),
    "minus":               (1.15,    1.3),
    "degree":              (1.1083,  1.25271),
    "currency":            (1.1102,  1.25592),
    "referencemark":       (1.1102,  1.25635),
    "dieresis":            (1.09474, 1.15789),
    "dotaccent":           (1.08491, 1.15094),
    "period":              (1.08491, 1.15094),
    "uni22C5":             (1.08491, 1.15094),
    "tilde":               (1.07527, 1.12903),
    "ogonek":              (1.10185, 1.16204),
    "cent":                (1.03455, 1.08061),
    "leaf":                (1.04523, 1.1093),
    "minute":              (1.42453, 1.69811),
    "primereversed":       (1.42453, 1.69811),
    "uni2033":             (1.42453, 1.69811),
    "uni2034":             (1.42453, 1.69811),
    "uni2036":             (1.42453, 1.69811),
    "uni2037":             (1.42453, 1.69811),
    "uni2057":             (1.42453, 1.69811),
}


def _letter_from_name(name):
    """Return base ASCII letter from a glyph name, e.g. 'Aacute'→'A', 'b'→'b'."""
    if len(name) == 1:
        return name
    if name[0].isupper() and (len(name) == 1 or not name[1].isupper()):
        return name[0]
    if name[0].islower() and len(name) > 1:
        return name[0]
    return None


def _math_letter(cp):
    """Return (is_upper, letter) for math alphanumeric Unicode codepoints."""
    import unicodedata as _ud
    try:
        w = _ud.name(chr(cp)).split()[-1]
        if len(w) == 1:
            return w.isupper(), w.upper() if w.isupper() else w.lower()
    except (ValueError, KeyError):
        pass
    return None, None


def ncm_y(name):
    """Return (st_y, sts_y) height ratio for ssty variants, per NewCM data.

    Encodes NewCM's design patterns:
      - Latin caps: 4 height groups (round-heavy, apex, medium, flat/special)
      - Latin lower: 5 height roles (x-height, ascender, descender-group, ij, vw)
      - Bold italic lower: st_y always 1.0, sts_y ≈ 1.009 for x-height
      - Greek italic: same grouping as corresponding Latin classes
      - Operators: small hardcoded table for significant deviations (>1%)
    """
    # Named operator/symbol
    if name in _OP_Y:
        return _OP_Y[name]

    # Single-char Latin base
    if len(name) == 1:
        if name.isupper():
            return (_UPP_ST.get(name, 1.0), _UPP_STS.get(name, 1.0))
        if name.islower():
            return (_LOW_ST.get(name, 1.0), _LOW_STS.get(name, 1.0))

    # Math Unicode alphanumerics
    base = name.split(".")[0]
    for pre, skip in [("uni", 3), ("u", 1)]:
        if base.lower().startswith(pre):
            try:
                cp = int(base[skip:], 16)
            except ValueError:
                break
            is_upper, letter = _math_letter(cp)
            if letter is None:
                break

            # Bold italic LOWERCASE: st stays at base height, sts grows slightly
            if 0x1D482 <= cp <= 0x1D49B or 0x1D736 <= cp <= 0x1D755:
                sts = _LOW_STS.get(letter, 1.0087 if letter in "acefgmnorstuvwxyz" else 1.003)
                return (1.0, sts)

            if is_upper:
                return (_UPP_ST.get(letter, 1.0), _UPP_STS.get(letter, 1.0))
            else:
                return (_LOW_ST.get(letter, 1.0), _LOW_STS.get(letter, 1.0))

    # Accented Latin letters: use the base letter's ratio
    letter = _letter_from_name(name)
    if letter and letter.isupper():
        return (_UPP_ST.get(letter, 1.0), _UPP_STS.get(letter, 1.0))
    if letter and letter.islower():
        return (_LOW_ST.get(letter, 1.0), _LOW_STS.get(letter, 1.0))

    return (1.0, 1.0)


# ── helpers ───────────────────────────────────────────────────────────────────

def in_italic_range(cp):
    return any(lo <= cp <= hi for lo, hi in ITALIC_RANGES)


def in_italic_range(cp):
    return any(lo <= cp <= hi for lo, hi in ITALIC_RANGES)


def parse_cp(name):
    """Extract Unicode codepoint from a glyph name like u1D434 or uni210E."""
    base = name.split(".")[0]
    for prefix, skip in [("uni", 3), ("u", 1)]:
        if base.lower().startswith(prefix):
            try:
                return int(base[skip:], 16)
            except ValueError:
                pass
    return -1


def is_italic_base(glyph):
    """True if this glyph is an italic base that should be scaled ×1.08."""
    cp = glyph.unicode
    return cp >= 0 and in_italic_range(cp)


def classify(name):
    """Return ssty_category string for a glyph name."""
    if re.match(r"^[a-z]$", name):
        return "latin"
    if re.match(r"^[A-Z]$", name):
        return "latin"
    if name in DIGIT_NAMES:
        return "digits_named"

    cp = parse_cp(name)
    if cp < 0:
        return "operators"

    try:
        uname = unicodedata.name(chr(cp))
    except (ValueError, KeyError):
        return "default"

    if "MATHEMATICAL BOLD ITALIC" in uname: return "math_bold_italic"
    if "MATHEMATICAL ITALIC"      in uname: return "math_italic"
    if "MATHEMATICAL BOLD"        in uname: return "math_bold"
    if "MATHEMATICAL SCRIPT"      in uname: return "math_script"
    if "MATHEMATICAL FRAKTUR"     in uname: return "math_fraktur"
    if "DIGIT"                    in uname: return "digits_unicode"
    if "GREEK"                    in uname: return "greek"
    return "operators"


def glyph_display_char(font, name):
    """Return a displayable Unicode character for a glyph, or empty string."""
    cp = font[name].unicode if name in font else parse_cp(name.split(".")[0])
    if cp > 0:
        try:
            return chr(cp)
        except (ValueError, OverflowError):
            pass
    return ""


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    log_path = os.path.join(SOURCES, "LibertinaMath-build.log")
    log = []

    def L(line=""):
        print(line)
        log.append(line)

    L(f"=== LibertinaMath build log  {datetime.datetime.now():%Y-%m-%d %H:%M:%S} ===")
    L(f"IN:  {SFD_IN}")
    L(f"OUT: {SFD_OUT}")
    L()

    # ── Step 1: open original, rename metadata ────────────────────────────────
    L("── Step 1: rename metadata")
    f = fontforge.open(SFD_IN)
    f.familyname = f.familyname.replace("Libertinus", "Libertina")
    f.fullname   = f.fullname.replace("Libertinus", "Libertina")
    f.fontname   = f.fontname.replace("Libertinus", "Libertina")
    old_designer = next(
        (v for _, n, v in f.sfnt_names if n == "Designer"), "")
    f.appendSFNTName("English (US)", "Designer",
                     f"uwni, {old_designer}" if old_designer else "uwni")
    f.appendSFNTName("English (US)", "Vendor URL",
                     "https://github.com/uwni/libertina")
    L(f"  familyname → {f.familyname}")
    L(f"  fullname   → {f.fullname}")
    L(f"  fontname   → {f.fontname}")
    L()

    # ── Step 2: scale italic base glyphs ×1.08 ───────────────────────────────
    L(f"── Step 2: scale italic base glyphs ×{BASE_SCALE}")
    base_matrix = psMat.scale(BASE_SCALE, 1.0)
    for g in [g for g in f.glyphs() if is_italic_base(g)]:
        w_before = g.width
        g.transform(base_matrix)
        ch = glyph_display_char(f, g.glyphname)
        L(f"  {ch:2}  {g.glyphname:30}  adv {w_before} → {g.width}")
    L()

    # ── Step 3: ssty variants (NewCM coverage) ───────────────────────────────
    L(f"── Step 3: generate ssty  ({len(NEWCM_BASES)} NewCM bases)")

    present = {g.glyphname for g in f.glyphs()}
    targets = [b for b in NEWCM_BASES if b in present]
    skipped = [b for b in NEWCM_BASES if b not in present]
    L(f"  Present in LibertinaMath: {len(targets)}")
    L(f"  Skipped (not in font):    {len(skipped)}")
    if skipped:
        L("  Skipped glyphs:")
        for b in skipped:
            L(f"    {b}")
    L()

    # Delete orphaned .ssty / .ssty1 / .ssty2 for target bases
    orphans = [b + sfx
               for b in targets
               for sfx in (".ssty", ".ssty1", ".ssty2")
               if (b + sfx) in present]
    for name in orphans:
        f.removeGlyph(f[name])
    L(f"  Deleted {len(orphans)} orphaned .ssty glyphs:")
    for name in orphans:
        L(f"    {name}")
    L()

    # Create .st / .sts variants
    L("  Created ssty variants:")
    cat_counts = defaultdict(int)
    for base in targets:
        cat = classify(base)
        st_w, sts_w = SSTY_RATIOS.get(cat, SSTY_RATIOS["default"])
        st_y, sts_y = ncm_y(base)
        cat_counts[cat] += 1
        src = f[base]

        for suffix, w, y in [(".st", st_w, st_y), (".sts", sts_w, sts_y)]:
            new_name = base + suffix
            if new_name in f:
                f.removeGlyph(f[new_name])
            f.createChar(-1, new_name)
            dest = f[new_name]
            # NOTE: del pen resets advance width to 1000 (FontForge default);
            # width and math metrics must be restored after del pen.
            pen = dest.glyphPen()
            src.draw(pen)
            del pen
            dest.width            = src.width
            dest.italicCorrection = src.italicCorrection
            dest.topaccent        = src.topaccent
            # transform() scales width, ItalicCorrection, and TopAccentHorizontal.
            dest.transform(psMat.scale(w, y))

        ch = glyph_display_char(f, base)
        has_y = ncm_y(base) != (1.0, 1.0)
        L(f"    {ch:2}  {base:30}  [{cat}]"
          f"  adv {src.width}"
          f"  → .st {f[base+'.st'].width}"
          f"  .sts {f[base+'.sts'].width}"
          + (f"  y=({st_y:.5f},{sts_y:.5f})" if has_y else ""))

    L()
    L("  Per-category summary:")
    for cat, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
        st_w, sts_w = SSTY_RATIOS.get(cat, SSTY_RATIOS["default"])
        L(f"    {cat:25} {n:4d}  st×{st_w:.3f}  sts×{sts_w:.3f}")
    L(f"  Total created: {len(targets)*2} glyphs")
    L()

    # ── Save SFD ──────────────────────────────────────────────────────────────
    f.save(SFD_OUT)
    f.close()
    L(f"── Saved {SFD_OUT}")

    # ── Rewrite ssty.fea ──────────────────────────────────────────────────────
    with open(SSTY_FEA) as fh:
        old_prime_subs = re.findall(r"  sub \S+ by \S+;", fh.read())
    with open(SFD_OUT, encoding="latin-1") as fh:
        sfd_text = fh.read()
    existing = {m.group(1) for m in re.finditer(r"^StartChar: (\S+)$", sfd_text, re.M)}
    prime_subs = [
        line for line in old_prime_subs
        if (ref := re.search(r"by (\S+);", line)) and ref.group(1) in existing
    ]

    fea_lines = ["feature ssty {"]
    if prime_subs:
        fea_lines += ["  # Prime symbols (single substitution)"] + prime_subs + [""]
    fea_lines += ["  # Math letters, digits, operators: level 1 = .st, level 2 = .sts"]
    for base in targets:
        fea_lines.append(f"  sub {base} from [{base}.st {base}.sts];")
    fea_lines += ["} ssty;", ""]
    with open(SSTY_FEA, "w") as fea:
        fea.write("\n".join(fea_lines))
    L(f"── Rewrote {SSTY_FEA}  ({len(targets)} alternate + {len(prime_subs)} single substitutions)")
    L()
    L("=== done ===")

    with open(log_path, "w") as lf:
        lf.write("\n".join(log) + "\n")
    print(f"\nLog written to {log_path}")


main()
