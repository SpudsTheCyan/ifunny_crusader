FROM python:3.11.4-bullseye

COPY requirements.txt /app/
WORKDIR /app/
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY /cogs/ /app/cogs/
COPY docker-compose.yml /app/
COPY Dockerfile /app/
COPY ifunny_watermark.jpg /app/
COPY logging.conf /app/
COPY main.py /app/
COPY requirements.txt /app/

CMD [ "python3", "main.py" ] ["sudo", "/sbin/ldconfig -v"]