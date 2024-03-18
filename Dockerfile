FROM python:3.9
WORKDIR /.

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./dtos ./dtos
COPY ./models ./models
COPY ./services ./services
COPY ./main.py ./main.py
COPY ./database.py ./database.py

ENTRYPOINT ["uvicorn", "main:app"]
