# coding=utf-8
"""
requires Python 3.6 or later
pip install requests
"""
import os
import base64
import json
import uuid
import requests
import argparse
import threading
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the variables
appid = os.getenv("APP_ID")
access_token = os.getenv("ACCESS_TOKEN")
cluster = os.getenv("CLUSTER")

host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"
header = {"Authorization": f"Bearer;{access_token}"}


def synthesize(text, speaker, emotion, output_dir, text_index, lang, encoding="wav"):
    id = f"{speaker}_{lang}_{text_index}_{emotion}"
    try:
        speaker_dir = Path(output_dir) / speaker
        speaker_dir.mkdir(exist_ok=True, parents=True)
        audio_file = speaker_dir / f"{id}.wav"

        if audio_file.exists():
            print(f"Already exist! Skip: {text}, {id}")
            return

        request_json = {
            "app": {"appid": appid, "token": "access_token", "cluster": cluster},
            "user": {"uid": "388808087185088"},
            "audio": {
                "voice_type": speaker,
                "encoding": encoding,
                "speed_ratio": 1.0,
                "volume_ratio": 1.0,
                "pitch_ratio": 1.0,
                "emotion": emotion,
                # "emotion": None,
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

        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        result = resp.json()

        if "data" in result:
            audio_data = base64.b64decode(result["data"])
            with open(audio_file, "wb") as f:
                f.write(audio_data)
            print(audio_file)

            del result["data"]
            json_file = speaker_dir / f"{id}.json"
            with open(json_file, "w") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
        else:
            print(f"Error at : {text}, {id}")
            print(result)
    except Exception as e:
        # e.with_traceback()
        print(e)
        print(f"Error at : {text}, {id}")


def main(args):
    text_files = {
        "zh": "zh.txt",
        # "zh": "test.txt",
        # "en": "en.txt",
    }

    threads = []

    for lang, file in text_files.items():
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            while len(threading.enumerate()) >= args.num_thread:
                pass  # Wait until a thread is available

            for speaker in args.speakers:
                t = threading.Thread(
                    target=synthesize,
                    args=(
                        line.strip(),
                        speaker,
                        args.emotion,
                        args.output_dir,
                        idx,
                        lang,
                    ),
                )
                t.start()
                threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TTS Synthesis Script")
    parser.add_argument(
        "-n", "--num_thread", type=int, default=2, help="Number of synthesis threads"
    )
    parser.add_argument(
        "-o", "--output_dir", type=str, default="./output", help="Output directory"
    )
    parser.add_argument(
        "-s",
        "--speakers",
        type=str,
        nargs="+",
        default=["BV001_streaming"],
        help="Speaker voice types, see: https://www.volcengine.com/docs/6561/97465",
    )
    parser.add_argument(
        "-e",
        "--emotion",
        type=str,
        default="narrator",
        help="Emotion type",
        choices=[
            "happy",
            "sad",
            "angry",
            "scare",
            "hate",
            "surprise",
            "novel_dialog",
            "narrator",
        ],
    )
    args = parser.parse_args()

    main(args)
