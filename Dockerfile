FROM denoland/deno:latest AS deno

FROM python:3.14

COPY --from=deno . .

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
COPY src .

CMD ["python3", "main.py"]
