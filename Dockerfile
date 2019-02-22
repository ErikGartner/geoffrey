FROM python:3.6-slim

RUN mkdir /app
WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "gordon.py"]
