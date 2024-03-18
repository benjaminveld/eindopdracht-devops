FROM python:3.9-slim
WORKDIR /.

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./dtos ./dtos
COPY ./models ./models
COPY ./services ./services
COPY ./main.py ./main.py
COPY ./database.py ./database.py

ARG DB_CONNECTION_STRING
ARG LIVECOINWATCH_API_KEY
ENV DB_CONNECTION_STRING=${DB_CONNECTION_STRING}
ENV LIVECOINWATCH_API_KEY=${LIVECOINWATCH_API_KEY}

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
