import platform 
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

# whisper_result(): 음성을 받고 특정 키워드를 찾는 함수를 만듦.
def whisper_result():
    out = subprocess.run(
        ["whisper", "output/output.wav", "--language", "Korean","--output_format","txt","--output_dir","output","--thread",'3'], capture_output=True,
    )
    if platform.system()=="Windows":
        result = out.stdout.decode(encoding="CP949")
    else : 
        result= out.stdout.decode(encoding="utf-8")
    print(result)
    # model = whisper.load_model("base")
    # result = model.transcribe('C:/Users/seohyegyo/Desktop/upstage_python/output.wav')
    return find_keyword(result)  # {"result": "내가 말한거"}

# 문자열을 입력 받아 딕셔너리를 반환하는 find_keyword 함수 정의
# sentence라는 매개변수를 통해 find_keyword의 값이 전달
def find_keyword(sentence: str) -> dict:

    print(sentence)
    command_list = ["날씨", "뉴스","뉴스에", "뉴스를","류스","류쓰","누스","유스","니스","나이스","현지시각", "시각", "시간","요약","요약해","요약해죠","요약해줘"]

    city_list = [
        "뉴욕",
        "유용",
        "런던",
        "파리",
        "도쿄",  # 도쿄
        "동경",  # 도쿄
        "베이징",
        "홍콩",
        "LA",
        "L.A.",
        "L.A" "로스앤젤레스",  # 로스앤젤레스
        "엘에이",  # 로스앤젤레스
        "에레이",  # 로스앤젤레스
        "시카고",
        "싱가포르",  # 싱가포르
        "싱가폴",  # 싱가포르
        "워싱턴 DC",
        "워싱턴DC",
        "워싱턴 D.C.",
        "워싱턴D.C.", 
        "워싱턴디씨",  # 워싱턴DC
        "워싱턴",  # 워싱턴DC
    ]

    # 예외처리: 무음, 문장에 키워드가 없을 때.
    city_result = []
    command_result = []
    # sentence(매개변수)에 전달된 str을 공백을 기준으로 분리하여 received_sentence변수에 리스트 형태로 저장
    received_sentence = sentence.split()

    # for루프 내부에서 루프 변수는 선언되고 초기화되며 각 반복에서 새로운 값을 가지게 된다.  
    # 이러한 루프 변수를 iterator(반복자)변수라고 한다.(keyword,cityname,command)

# 도시 및 명령어 리스트에 추가할 단어 설정      
    # city_result: 도시명 추가 리스트  
    for keyword in city_list:
        if keyword in received_sentence:
            city_result.append(keyword)
    # command_result:명령어문 추가 리스트 
    for keyword in command_list:
        if keyword in received_sentence:
            command_result.append(keyword)
# 도시 이름 정제처리 
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

        if cityname in [
            "워싱턴디씨",
            "워싱턴",
            "워싱턴 DC",
            "워싱턴DC",
            "워싱턴 D.C.",
            "워싱턴D.C.",
        ]:
            city_result.remove(cityname)
            city_result.append("워싱턴DC")
# 명령어 정제처리 
    for command in command_result:
        if command in ["시간", "시각"]:
            command_result.remove(command)
            command_result.append("현지시각")
        elif command in ["요약해줘","요약해","요약해죠"]:
            command_result.remove(command)
            command_result.append("요약")
        elif command in ["류스","류쓰","누스","유스","뉴스를","니스","나이스","뉴스에"]:
            command_result.remove(command)
            command_result.append("뉴스")
    
    for command in command_result:
        if len(city_result)==0 and (command=="뉴스" or command=="요약"):
            city_result.append("서울")

    if (len(city_result) == 0) and (len(command_result) == 0):
        return {
            "result": {"city": city_result, "command": command_result},
            "error": "잘 못 알아들었어요. 다시 시도해주세요",
        }

    elif len(command_result) == 0:
        return {
            "result": {"city": city_result, "command": command_result},
            "error": "시간, 날씨, 뉴스 중 하나 말씀 주세요",
        }

    elif len(city_result) == 0:
        return {
            "result": {"city": city_result, "command": command_result},
            "error": "잘 못 알아들었습니다. 다시 시도해주세요.",
        }
    else:
        return {"result": {"city": city_result, "command": command_result}, "error": -1}
