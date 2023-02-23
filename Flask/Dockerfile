FROM python:3-alpine3.17

WORKDIR /Flask

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3","/src/index.py"]
