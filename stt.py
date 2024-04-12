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


def find_keyword(sentence: str) -> dict:
# citys=['뉴욕','런던','파리','도쿄','베이징','홍콩','로스앤젤레스','시카고','싱가포르','워싱턴DC']

    command_list = [
        "시간",
        "날씨",
        "뉴스"
    ]

    city_list = [
        "뉴욕",
        "런던",
        "파리",
        "도쿄", # 도쿄
        "동경", # 도쿄
        "베이징",
        "홍콩",
        "LA",
        "L.A.",
        "L.A"
        "로스앤젤레스", #로스앤젤레스
        "엘에이", #로스앤젤레스
        "에레이", #로스앤젤레스
        "시카고",
        "싱가포르", #싱가포르
        "싱가폴", #싱가포르
        "워싱턴 DC",
        "워싱턴DC",
        "워싱턴 D.C.",
        "워싱턴D.C."
        "워싱턴디씨", #워싱턴DC
        "워싱턴", # 워싱턴DC
    ]

    # 엘에이
    # 예외처리: 무음, 문장에 키워드가 없을 때.
    keyword_list = command_list.copy()
    keyword_list.extend(city_list)
    result_list = []
    for keyword in keyword_list:
        if keyword in sentence.split(): 
            result_list.append(keyword)


    for cityname in result_list:
        if cityname == "동경":
            result_list.remove("동경")
            result_list.append("도쿄")
        
        if cityname in ["엘에이", "에레이", "L.A.", "LA", "L.A"]:
            result_list.remove(cityname)
            result_list.append("로스앤젤레스")
        if cityname == "싱가폴":
            result_list.remove(cityname)
            result_list.append("싱가포르")
        if cityname in ["워싱턴디씨", "워싱턴", "워싱턴 DC", "워싱턴DC", "워싱턴 D.C.", "워싱턴D.C."]:
            result_list.remove(cityname)
            result_list.append("워싱턴DC")



    if len(result_list) == 0: # result_list == []
        return {"result": result_list , "error": "잘 못 알아들었어요. 다시 시도해주세요" }

    for result in result_list:
        if result not in ["시간", "날씨", "뉴스"]:
            return {"result": result_list , "error": "시간, 날씨, 뉴스 중 하나 말씀 주세요" }
        if result not in city_list:
            return {"result": result_list , "error": "잘 못 알아들었습니다. 글로벌 도시 이름 하나 말씀 주세요."}

    return {"result": result_list}
