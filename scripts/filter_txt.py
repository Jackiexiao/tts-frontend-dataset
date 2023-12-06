import json
import re
from pathlib import Path
import random

txt_file = (
    "./raw_data/wiki_zh/AA/wiki_00"
)

txt_files = list(Path("raw_data/wiki_zh").glob("**/wiki*"))

random.shuffle(txt_files)

min_len = 100
max_len = 300
max_sens = 200 * 1000

sens = []

num = 0
for txt_file in txt_files:
    print(txt_file)
    if num > max_sens:
        break
    with open(txt_file, "r", encoding="utf8") as f:
        for line in f.readlines():
            data = json.loads(line)
            text = data["text"].strip()
            if len(text) < max_len and len(text) > min_len:
                text = re.sub(r"\n+", "\n", text)
                sub_sens = text.split("\n")
                sub_sens = [x.strip() for x in sub_sens if len(x.strip()) > 0]
                sens.extend(sub_sens)
                num += len(sub_sens)
                print(num)

# Drop duplicates in sens
sens = list(set(sens))

max_final_sens = 20 * 1000

concat_sens = []

# Concatenate text into approximately 300-character length text with periods as separators to save money....
current_text = ""
for sen in sens:
    if len(current_text) + len(sen) + 1 <= 300:
        current_text += sen + "。"
    else:
        concat_sens.append(current_text.strip().replace("。。", "。"))
        current_text = sen + "。"

with open("zh.txt", "w", encoding="utf8") as wf:
    for sen in concat_sens:
        wf.write(sen + "\n")
