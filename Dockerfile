FROM python:3.6-slim

RUN mkdir /app
WORKDIR /app
COPY . ./

RUN pip install pipenv
RUN pipenv install --system --ignore-pipfile

ENTRYPOINT ["python", "gordon.py"]
