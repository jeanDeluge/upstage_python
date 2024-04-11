import whisper
import subprocess

# model = whisper.load_model("base")
# result = model.transcribe("audio.m4a")
# print(result["text"])

# 속도가 느림 -> 직접 명령어 입력 형태로 바꿈


# def whisper_result():
#     with open("out.txt", "wb") as f:
#         out = subprocess.run(
#             ["whisper", "output.wav", "--language", "Korean"], capture_output=True
#         )
#         f.write(out.stdout)


def whisper_result():
    out = subprocess.run(
        ["whisper", "output.wav", "--language", "Korean"], capture_output=True
    )
    result = out.stdout.decode(encoding="utf-8")
    find_keyword(result)


def find_keyword(sentence):

    keyword_list = [
        "시간",
        "날씨",
        "뉴스",
        "뉴욕",
        "런던",
        "파리",
        "도쿄",
        "동경",
        "베이징",
        "홍콩",
        "로스앤젤레스",
        "엘에이",
        "에레이",
        "시카고",
        "싱가포르",
        "싱가폴",
        "워싱턴디씨",
        "워싱턴",
    ]

    # 엘에이
    # 예외처리: 무음, 문장에 키워드가 없을 때.

    result_list = []
    for keyword in keyword_list:
        if keyword in sentence:
            result_list.append(keyword)

    print(result_list)

    return result_list
