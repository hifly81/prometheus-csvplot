FROM python:3.7
WORKDIR /app
COPY ./export_csv.py /app
COPY ./plot.py /app
COPY ./config/metrics.txt /app/config/metrics.txt
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt