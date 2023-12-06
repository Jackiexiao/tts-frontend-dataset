import json
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

polyphones = []

prosody_sens = []
g2p_sens = []


def split_by(text, symbol="。"):  # 这里的"下划"线是一个特殊的,罕见符号
    text = text.replace(symbol, f"{symbol}▁")
    parts = text.split("▁")
    return [x.strip() for x in parts if len(x.strip()) > 0]


def process_json_file(json_file):
    with open(json_file, "r") as f:
        result = json.load(f)
        data = json.loads(result["addition"]["description"])

        with open("test_desc.json", "w") as wf:
            json.dump(data, wf, indent=4, ensure_ascii=False)

        f_data = json.loads(result["addition"]["frontend"])
        with open("test_frontend.json", "w") as wf:
            json.dump(f_data, wf, indent=4, ensure_ascii=False)

        d = data[0]

        g2p_sen = []
        unit_sen = []
        for u in d["unitTson"]["unit"]:
            word_phones = [label["phone"] for label in u["label"]]
            word_tones = [label["tone"] for label in u["label"]]

            pinyin = ""
            for phone in word_phones:
                if phone.startswith("C0"):
                    pinyin += phone[2:]
            pinyin += word_tones[-1]
            g2p_sen.append(pinyin)
            unit_sen.append(u["word"])

        g2p_sens.append(d["pinline"].split())
        g2p_sens.append(g2p_sen)
        g2p_sens.append(unit_sen)

        prosody_sens.extend(split_by(data[0]["psdline"]))


with ThreadPoolExecutor(max_workers=10) as executor:
    list(
        tqdm(
            executor.map(process_json_file, list(Path("output/").glob("**/*.json"))),
            total=len(list(Path("output/").glob("**/*.json"))),
        )
    )

with open("prosody.txt", "w", encoding="utf8") as wf:
    for sen in prosody_sens:
        wf.write(sen + "\n")


with open("g2p.json", "w") as f:
    json.dump(g2p_sens, f, indent=4, ensure_ascii=False)
