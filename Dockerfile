from continuumio/anaconda3

RUN apt-get -y update
RUN apt-get -y install libfuse2
RUN apt-get -y install libgconf-2-4
RUN apt-get -y install libgtk2.0-0
RUN apt-get -y install xvfb
RUN apt-get -y install libnss3-dev
RUN apt-get -y install libasound2
RUN pip install plotly

RUN mkdir -p /tmp/perftest
RUN mkdir -p /tmp/perftest/config
RUN mkdir -p /tmp/perftest/csv

COPY export_csv.py /tmp/perftest
COPY plot.py /tmp/perftest

COPY config/metrics.txt /tmp/perftest/config
COPY config/namespaces.txt /tmp/perftest/config

WORKDIR /tmp
RUN wget 'https://github.com/plotly/orca/releases/download/v1.2.1/orca-1.2.1-x86_64.AppImage'
RUN chmod +x /tmp/orca-1.2.1-x86_64.AppImage
COPY orca /usr/bin/
RUN chmod +x /usr/bin/orca

WORKDIR /tmp/perftest
