import json
import re
from utils import split_text

with open("g2p.json", "r") as f:
    g2p_sens = json.load(f)


ori_pinyin_lines = g2p_sens[::3]
pinyin_lines = g2p_sens[1::3]
word_lines = g2p_sens[2::3]

phoneme2pinyin = {}

for ori, new in zip(ori_pinyin_lines, pinyin_lines):
    xs = [i for i in ori if i != "sp"]
    ys = [i for i in new if i != "0"]

    if len(xs) == len(ys):
        for i, j in zip(xs, ys):
            if i[-1].isdigit() and j[-1].isdigit():
                ix = i[:-1]
                jx = j[:-1]
                if ix != jx:
                    phoneme2pinyin[jx] = ix
print(phoneme2pinyin)

with open("phoneme2pinyin.json", "w") as f:
    json.dump(phoneme2pinyin, f, indent=4, ensure_ascii=False)


########### step2: get word2pinyin and polyphone map ###########

word_pinyin_map = {}
word_pinyin_freq_map = {}

for word_line, pinyin_line in zip(word_lines, pinyin_lines):
    for word, pinyin in zip(word_line, pinyin_line):
        pinyin = pinyin.replace("6", "3")
        if pinyin[:-1] in phoneme2pinyin:
            std_pinyin = phoneme2pinyin[pinyin[:-1]] + pinyin[-1]
        else:
            std_pinyin = pinyin

        if word not in word_pinyin_map:
            word_pinyin_map[word] = [std_pinyin]
            word_pinyin_freq_map[word] = {std_pinyin: 1}
        else:
            if std_pinyin not in word_pinyin_map[word]:
                word_pinyin_map[word].append(std_pinyin)
                word_pinyin_freq_map[word][std_pinyin] = 1
            else:
                word_pinyin_freq_map[word][std_pinyin] += 1


print(word_pinyin_map)
with open("word_pinyin_map.json", "w") as f:
    json.dump(word_pinyin_map, f, indent=4, ensure_ascii=False)

polyphone_map = {}
for word, pinyins in word_pinyin_map.items():
    if len(pinyins) > 1 and re.search(r"[a-z]+[1-5]", "".join(pinyins)):
        polyphone_map[word] = pinyins

# Remove sil and sp, 不属于多音字
if "sp" in polyphone_map:
    del polyphone_map["sp"]

# 可选: 去除轻声多音字
remove_words = []
for word, pinyins in polyphone_map.items():
    if len(pinyins) == 2 and word != "得":  # 得: de5 de2 明显不同
        p1 = pinyins[0]
        p2 = pinyins[1]
        if p1[-1] == "5" or p2[-1] == "5":
            if p1[:-1] == p2[:-1]:
                print("Del 轻声多音字:", word, pinyins)
                remove_words.append(word)


for word in remove_words:
    del polyphone_map[word]

with open("polyphone_map.json", "w") as f:
    json.dump(polyphone_map, f, indent=4, ensure_ascii=False)

polyphone_map_freq = {}
for word in polyphone_map:
    polyphone_map_freq[word] = word_pinyin_freq_map[word]

with open("polyphone_map_freq.json", "w") as f:
    json.dump(polyphone_map_freq, f, indent=4, ensure_ascii=False)

print(f"总共有{len(polyphone_map)}个多音字")

########## step 3: get final g2p data

g2p_lines = []
for word_line, pinyin_line in zip(word_lines, pinyin_lines):
    g2p_line = ""
    for word, pinyin in zip(word_line, pinyin_line):
        pinyin = pinyin.replace("6", "3")
        if pinyin[:-1] in phoneme2pinyin:
            std_pinyin = phoneme2pinyin[pinyin[:-1]] + pinyin[-1]
        else:
            std_pinyin = pinyin

        if word in polyphone_map:
            g2p_line += word + f"▁{std_pinyin}▁"
        else:
            if word not in ["sil", "sp"]:
                g2p_line += word
    g2p_lines.append(g2p_line)


with open("g2p.txt", "w") as wf:
    for g2p_line in g2p_lines:
        for sen in split_text(g2p_line):
            if "▁" in sen:
                wf.write(sen + "\n")
