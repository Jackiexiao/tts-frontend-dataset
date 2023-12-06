import json

with open("bd_example/test.json", "r") as f:
    result = json.load(f)
    data = json.loads(result["addition"]["description"])
    # print(data)
    with open("test_desc.json", "w") as wf:
        json.dump(data, wf, indent=4, ensure_ascii=False)

    f_data = json.loads(result["addition"]["frontend"])
    with open("test_frontend.json", "w") as wf:
        json.dump(f_data, wf, indent=4, ensure_ascii=False)

    phones = []
    words = []
    prosodys = []
    tones = []
    jpauses = []
    jpaccents = []

    for d in data:
        for u in d["unitTson"]["unit"]:
            phones.extend([label["phone"] for label in u["label"]])
            words.extend([u["word"]])
            prosodys.extend([label["prosody"] for label in u["label"]])
            tones.extend([label["tone"] for label in u["label"]])
            jpaccents.extend([label["jpaccent"] for label in u["label"]])

    print(f"phones: {' '.join(phones)}")
    print(f"prosodys: {prosodys}")
    print(f"tones: {tones}")

    print(f"words: {' '.join(words)}")
    print(f"jpaccent: {jpaccents}")
