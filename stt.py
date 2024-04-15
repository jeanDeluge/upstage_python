import whisper
import subprocess

# model = whisper.load_model("base")
# result = model.transcribe("output.m4a")
# print(result["text"])

# 속도가 느림 -> 직접 명령어 입력 형태로 바꿈


# def whisper_result():
#     with open("out.txt", "wb") as f:
#         out = subprocess.run(
#             ["whisper", "output.wav", "--language", "Korean"], capture_output=True
#         )
#         f.write(out.stdout)


def whisper_result():
    print("들어왔음")
    out = subprocess.run(
        ["whisper", "output.wav", "--language", "Korean"], capture_output=True
    )
    print("실행은 되었음")
    result = out.stdout.decode(encoding="utf-8")
    # model = whisper.load_model("base")
    # result = model.transcribe('C:/Users/seohyegyo/Desktop/upstage_python/output.wav')
    print(result)
    return find_keyword(result) #{"result": "내가 말한거"}


def find_keyword(sentence: str) -> dict:
    citys=['뉴욕','런던','파리','도쿄','베이징','홍콩','로스앤젤레스','시카고','싱가포르','워싱턴DC']

    command_list = [
        "날씨",
        "뉴스",
        "현지시각"
    ]

    city_list = [
        "뉴욕",
        "유용",
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
    city_result = []
    command_result= []
    received_sentence = sentence.split()
    for keyword in city_list:
        if keyword in received_sentence: 
            city_result.append(keyword)

    for keyword in command_list:
        if keyword in received_sentence:
            command_result.append(keyword)


    for cityname in city_result:
        
        if cityname == "유용":
            city_result.remove("유용")
            city_result.append("뉴욕")
            
        if cityname == "동경":
            city_result.remove("동경")
            city_result.append("도쿄")
        
        if cityname in ["엘에이", "에레이", "L.A.", "LA", "L.A"]:
            city_result.remove(cityname)
            city_result.append("로스앤젤레스")
        if cityname == "싱가폴":
            city_result.remove(cityname)
            city_result.append("싱가포르")
        if cityname in ["워싱턴디씨", "워싱턴", "워싱턴 DC", "워싱턴DC", "워싱턴 D.C.", "워싱턴D.C."]:
            city_result.remove(cityname)
            city_result.append("워싱턴DC")



    if len(city_result) == 0 or len(command_result) == 0:
        print(city_result, command_result)
        return {"result": {"city": city_result, "command": command_result} , "error": "잘 못 알아들었어요. 다시 시도해주세요" }

    elif len(city_result) != 0 and city_result[0] not in city_list:
            print(city_result, command_result)

            return {"result": {"city": city_result, "command": command_result}  , "error": "시간, 날씨, 뉴스 중 하나 말씀 주세요" }
    elif len(command_result) != 0 and command_result[0] not in command_result:
            print(city_result, command_result)

            return {"result": {"city": city_result, "command": command_result} , "error": "잘 못 알아들었습니다. 글로벌 도시 이름 하나 말씀 주세요."}
    
    print(city_result)
    return {"result": {"city": city_result, "command": command_result}, "error": -1}
