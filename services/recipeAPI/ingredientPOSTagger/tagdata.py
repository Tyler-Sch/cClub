import numpy as np
import re

def tokenize(s):
    """
    Tokenize on parenthesis, punctuation, spaces and American units followed by a slash.

    We sometimes give American units and metric units for baking recipes. For example:
        * 2 tablespoons/30 mililiters milk or cream
        * 2 1/2 cups/300 grams all-purpose flour

    The recipe database only allows for one unit, and we want to use the American one.
    But we must split the text on "cups/" etc. in order to pick it up.
    """
    s = s.lower()
    s = cleanUnicodeFractions(s)
    american_units = ['cup', 'tablespoon', 'teaspoon', 'pound', 'ounce', 'quart', 'pint']
    for unit in american_units:
        s = s.replace(unit + '/', unit + ' ')
        s = s.replace(unit + 's/', unit + 's ')

    return filter(None, re.split(r'([,\(\)-\.])?\s*', clumpFractions(s)))

def joinLine(columns):
    return "\t".join(columns)

def clumpFractions(s):
    """
    Replaces the whitespace between the integer and fractional part of a quantity
    with a dollar sign, so it's interpreted as a single token. The rest of the
    string is left alone.

        clumpFractions("aaa 1 2/3 bbb")
        # => "aaa 1$2/3 bbb"
    """
    return re.sub(r'(\d+)\s+(\d)/(\d)', r'\1$\2/\3', s)

def cleanUnicodeFractions(s):
    """
    Replace unicode fractions with ascii representation, preceded by a
    space.

    "1\x215e" => "1 7/8"
    """

    fractions = {
        u'\x215b': '1/8',
        u'\x215c': '3/8',
        u'\x215d': '5/8',
        u'\x215e': '7/8',
        u'\x2159': '1/6',
        u'\x215a': '5/6',
        u'\x2155': '1/5',
        u'\x2156': '2/5',
        u'\x2157': '3/5',
        u'\x2158': '4/5',
        u'\xbc': ' 1/4',
        u'\xbe': '3/4',
        u'\x2153': '1/3',
        u'\x2154': '2/3',
        u'\xbd': '1/2',
    }

    for f_unicode, f_ascii in fractions.items():
        s = s.replace(f_unicode, ' ' + f_ascii)

    return s

def unclump(s):
    """
    Replacess $'s with spaces. The reverse of clumpFractions.
    """
    return re.sub(r'\$', " ", s)
