FROM python:3.11.4-bullseye

COPY requirements.txt /app/
WORKDIR /app/
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY /cogs/ .
COPY /docker-compose.yml .
COPY /Dockerfile .
COPY /ifunny_watermark.jpg .
COPY /logging.conf .
COPY /main.py .
COPY /requirements.txt .

CMD [ "python3", "main.py" ] ["sudo", "/sbin/ldconfig -v"]