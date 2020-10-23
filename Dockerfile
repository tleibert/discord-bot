FROM python:latest

WORKDIR /app

COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# install src
COPY src/ .

CMD ["python", "-u","bot.py"]
