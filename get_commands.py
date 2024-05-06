import platform 
import subprocess

class InputFromUser:
    def __init__(self, filename):
        self.filename = filename
        self.input_voice_sentence = "뉴욕날씨, 뉴욕시간"
        self.result = {}

    def __enter__(self):
        # self.whisper_result() 
        self.result = self.find_keyword()
        return self.result

    def __exit__(self, type, value, trackback):
        pass


    def whisper_result(self):
        out = subprocess.run(
            ["whisper", self.filename, "--language", "Korean","--output_format","txt","--output_dir", self.filename, "--thread",'3'], capture_output=True,
        )
        if platform.system()=="Windows":
            result = out.stdout.decode(encoding="CP949")
        else : 
            result= out.stdout.decode(encoding="utf-8")
        # model = whisper.load_model("base")
        # result = model.transcribe('C:/Users/seohyegyo/Desktop/upstage_python/output.wav')
        self.input_voice_sentence = result  # {"result": "내가 말한거"}
        
    def find_keyword(self):
        wanted_city = self.get_city()
        commands = self.get_command_keyword()

        if not wanted_city and not commands:
           return { "error": "잘 못 알아들었습니다. 다시 시도해주세요.",}
        # 현지시각, 날씨 => city 필요해요

        elif not wanted_city and ("현지시각" in commands or "날씨" in commands):
            return {"error": "글로벌 도시 중 하나 말씀해주세요. 예시는 뉴욕, 워싱턴DC, LA, 도쿄, 베이징, 홍콩, 시카고, 파리, 싱가포르"}
        
        elif not wanted_city and "뉴스" in commands:
            wanted_city.append("서울")
            return {"result": {"city": wanted_city, "command": commands}, "error": -1}

        elif not wanted_city and "요약" in commands:
            wanted_city.append("서울")
            return {"result": {"city": wanted_city, "command": commands}, "error": -1}
        elif not commands: 
            return { "error": "시간, 날씨, 뉴스 중 하나 말씀 주세요"}
        
        elif len(wanted_city) > 1:
            return { "error": "한 도시만 말씀 주세요"}
        
        elif len(commands) > 1:
            return { "error" : "시간, 날씨, 뉴스 중 하나의 명령만 주세요"}
        else:
            return {"result": {"city": wanted_city, "command": commands}, "error": -1}
        
    def get_command_keyword(self):
        command_list = ["날씨", "뉴스","류스","류쓰","누스","유스","니스","나이스","현지시각", "시각", "시간","요약"]
        commands = [] #날씨, 시각
        received_sentence = self.input_voice_sentence # "뉴욕날씨알려줘"

        # commands:명령어문 추가 리스트 
        for keyword in command_list:
            if keyword in received_sentence:
                commands.append(keyword)

        for command in commands:
            if command in ["시간", "시각"]:
                commands.remove(command)
                commands.append("현지시각")
            elif command in ["류스","류쓰","누스","유스","뉴스","니스","나이스","뉴스"]:
                commands.remove(command)
                commands.append("뉴스")

        return commands
    
    def get_city(self):
        received_sentence = self.input_voice_sentence
        city_list = [
            "뉴욕", "유용",
            "런던",
            "파리",
            "도쿄", "동경",  # 도쿄
            "베이징",
            "홍콩",
            "LA","L.A.","L.A", "로스앤젤레스","엘에이","에레이",  # 로스앤젤레스
            "시카고",
            "싱가포르", "싱가폴",  # 싱가포르
            "워싱턴 DC","워싱턴DC","워싱턴 D.C.","워싱턴D.C.", "워싱턴디씨","워싱턴",  # 워싱턴DC
        ]
        wanted_city = []

        for city in city_list:
            if city in received_sentence:
                wanted_city.append(city)

        for cityname in wanted_city:

            if cityname == "유용":
                wanted_city.remove("유용")
                wanted_city.append("뉴욕")

            if cityname == "동경":
                wanted_city.remove("동경")
                wanted_city.append("도쿄")

            if cityname in ["엘에이", "에레이", "L.A.", "LA", "L.A"]:
                wanted_city.remove(cityname)
                wanted_city.append("로스앤젤레스")

            if cityname == "싱가폴":
                wanted_city.remove(cityname)
                wanted_city.append("싱가포르")

            if cityname in ["워싱턴디씨","워싱턴","워싱턴 DC","워싱턴DC","워싱턴 D.C.","워싱턴D.C.",]:
                wanted_city.remove(cityname)
                wanted_city.append("워싱턴DC")

        return wanted_city
    