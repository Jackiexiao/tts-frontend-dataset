import re


def split_by(text, symbol="。"):
    text = text.replace(symbol, f"{symbol}<split>")
    parts = text.split("<split>")
    return [x.strip() for x in parts if len(x.strip()) > 0]


def split_text(sentence):
    """按大标点符号切分句子"""
    cn_puncs = "？，。！：；"  # 顿号不分句，如果遇到超长的 含顿号
    for cn_punc in cn_puncs:
        sentence = sentence.replace(cn_punc, cn_punc + "*")
    split_sens = sentence.split("*")

    return split_sens


all_allow_char = (
    r"[^ _ \t\r\n\u4e00-\u9fa5\u0391-\u03A1\u03A3-\u03A9\u03B1-\u03C1\u03C3-\u03C9\u2460-\u249B\u2160-\u216B\u2170-\u217B\u2776-\u277F\u3220-\u3229"
    r"0-9a-zA-Z|–－&\^\\─~—﹒．：―“”／，∶＋━＝×*＊\'∙•・･。？！、；‘’﹃﹄﹁﹂（）［］〔〕【】…\-～·《》〈〉￥¥$﹏＿.@「」:/,()<>!?;\[\]"
    r"\"{}αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩµ%‰℃℉′°º〃″"
    r"]"
)

def delete_strange_char(text: str):
    return re.sub(all_allow_char, "", text)
