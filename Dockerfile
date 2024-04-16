FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev ffmpeg -y
RUN apt install unzip  
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN mkdir chrome
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code
EXPOSE 80
# 
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python","main.py"]