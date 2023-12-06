import base64
import json
import uuid
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the variables
appid = os.getenv("APP_ID")
access_token = os.getenv("ACCESS_TOKEN")
cluster = os.getenv("CLUSTER")


voice_type = "BV001_streaming"

# text = "感觉今天天气真不错." * 34  # 1024 字节, 折算就是最大 341 个字
text = "你好世界。hello world."
host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"

header = {"Authorization": f"Bearer;{access_token}"}

request_json = {
    "app": {"appid": appid, "token": "access_token", "cluster": cluster},
    "user": {"uid": "388808087185088"},
    "audio": {
        "voice_type": voice_type,
        "encoding": "mp3",
        "speed_ratio": 1.0,
        "volume_ratio": 1.0,
        "pitch_ratio": 1.0,
    },
    "request": {
        "reqid": str(uuid.uuid4()),
        "text": text,
        "text_type": "plain",
        "operation": "query",
        "with_frontend": 1,
        "frontend_type": "unitTson",
    },
}

# response_json 格式, ps: 不会进行分句

"""
{
    "reqid": "7cd35c91-4203-46f4-a9a5-2ef1862be559",
    "code": 3000,
    "operation": "query",
    "message": "Success",
    "sequence": -1,
    "addition": {
        "description": # 下面是解析后的结果, 原始是一个 json 字符串
            [
                {
                    "duration": 2195,
                    "pinline": "ni6 hao3 shi4 jie4 / HH AH0 . L OW1  / W ER1 L D ",
                    "posline": "你好/VV 世界/NN ！ hello/JJ world/NN .",
                    "psdline": "你好#1世界#4！hello#1 world#4.",
                    "ssml_json": null,
                    "style_name": "neutral",
                    "tn_line": "input text:你好世界！ hello world.<split>high pripority rule result:你好世界！ hello world.<split>nntn result:你好世界！ hello world.<split>low pripority rule result:你好世界！ hello world.",
                    "unitTson": {
                        "origin_text": "你好世界! hello world.",
                        "text": "你好世界！hello world.",
                        "unit": [
                            { # 这里一个 word 可以对应多个音素
                                "word": "sil", # 汉字, 英文, 标点 或 sil
                                "label": [
                                    {
                                    "accentType": "0",
                                    "boundaryTone": "0",
                                    "duration_ratio": 1.0,
                                    "energy": 0.0,
                                    "focus": "0",
                                    "index": -1,
                                    "intonation": "0",
                                    "isLiandiaoBoundary": "1",
                                    "jpaccent": "0",
                                    "language": "none",
                                    "liandiaoType": "None",
                                    "phone": "sil",
                                    "phoneEnd": 25,
                                    "phoneStart": 0,
                                    "phraseAccent": "0",
                                    "pitchMean": 0.0,
                                    "pitchVar": 0.0,
                                    "prosody": "0",
                                    "speed": 0.0,
                                    "syllable_boundary_level": 0,
                                    "tone": "0",
                                    "unitType": "sil",
                                    "word": "sil",
                                    "wordCategory": "S"
                                }
                            ],
                        }
                    ]
                },
            ]
        "duration": "2195",
        "first_pkg": "73",
        "frontend": # 下面是解析后的结果, 原始是一个 json 字符串
            {
                "words": [
                    {
                        "word": "你",
                        "start_time": 0.025,
                        "end_time": 0.165,
                        "unit_type": "text"
                    },
                ],
                "phonemes": [
                    {
                        "phone": "C0n",
                        "start_time": 0.025,
                        "end_time": 0.085
                    },
                ]
            }
        }
    }
}
"""

if __name__ == "__main__":
    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        result = resp.json()
        print(result)
        if "data" in result:
            data = result["data"]
            file_to_save = open("test_submit.mp3", "wb")
            file_to_save.write(base64.b64decode(data))

            del result["data"]
            with open("test.json", "w") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
    except Exception as e:
        e.with_traceback()
    print("See test_submit.mp3, test.json")
