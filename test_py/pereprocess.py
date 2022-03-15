import homoglyphs as hg
import re


punct = {
    "end": hg.Homoglyphs().get_combinations(':'),
    "dot": hg.Homoglyphs().get_combinations('.'),
    "hyphen": hg.Homoglyphs().get_combinations('-'),
    "large_hypen": hg.Homoglyphs().get_combinations('–'),
    "larger_hypen": hg.Homoglyphs().get_combinations('—'),
    "comma": hg.Homoglyphs().get_combinations(','),
    "apostrophe": hg.Homoglyphs().get_combinations('ՙ'),
    "exclamation": hg.Homoglyphs().get_combinations('՜'),
    "accents": hg.Homoglyphs().get_combinations('՛'),
    "emphasis": hg.Homoglyphs().get_combinations('՝')
    }


def preprocess_text(text):
    for elem in text:
        if elem in punct["end"]:
            text = text.replace(elem, ":")
        if elem in punct["dot"]:
            text = text.replace(elem, ".")
        if elem in punct["hyphen"]:
            text = text.replace(elem, "-")
        if elem in punct["comma"]:
            text = text.replace(elem, ",")
        if elem in punct["large_hypen"]:
            text = text.replace(elem, "-")
        if elem in punct["larger_hypen"]:
            text = text.replace(elem, "-")
        if elem in punct["apostrophe"]:
            text = text.replace(elem, "’")
        if elem in punct["exclamation"]:
            text = text.replace(elem, "՜")
        if elem in punct["accents"]:
            text = text.replace(elem, "՛")
        if elem in punct["emphasis"]:
            text = text.replace(elem, "՝")

    text = text.replace('\n', ' ')
    regex = r'[Ա-Ֆա-ֆև]+ը[բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*-'
    for match in re.findall(regex, text):
        if len(match) > 3:
           text = text.replace(match, match[:-3] + match[-2:])
        else:
           text = text.replace(match, match[-3] + match[-1])
    text = text.replace('-\n', '')
    text = text.replace('\n', ' ')

    return text
