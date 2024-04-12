import sys
import pyaudio
import wave
from stt import whisper_result

"""
(1) 음성 입력 장치(마이크)를 통해 사용자 음성 수신
 - PyAudio 이용
   : Cross-platform audio I/O with PortAudio
     (https://pypi.org/project/PyAudio/)
 - PyAudio 기본 소스코드는 아래를 참고하여 작성
   : PyAudio 기본 사용 방법, 김논리 
     (https://ungodly-hour.tistory.com/35)
     
(2) 사용자 음성에서 키워드 추출
 - OpenAI Whisper API 이용
"""

# Recorder
# - 5초 동안 음성 입력을 받습니다. -> wav 파일로 저장
# PyAudio 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# PyAudio 객체를 생성합니다.
p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("Start to record the audio.")

# 사용자의 음성을 수신을 시작합니다. (읽습니다.)
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording is finished.")

# 사용자의 음성 수신을 중지합니다.
stream.stop_stream()
stream.close()

# PyAudio 객체를 종료합니다.
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()

# # Player
# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

# wf = wave.open(sys.argv[1], "rb")

# p = pyaudio.PyAudio()

# stream = p.open(
#     format=p.get_format_from_width(wf.getsampwidth()),
#     channels=wf.getnchannels(),
#     rate=wf.getframerate(),
#     output=True,
# )

# data = wf.readframes(CHUNK)

# while data:
#     stream.write(data)
#     data = wf.readframes(CHUNK)

# stream.stop_stream()
# stream.close()

# p.terminate()

#
whisper_result()
