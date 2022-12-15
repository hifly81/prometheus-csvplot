FROM continuumio/anaconda3

# Add additional modules on debian
RUN apt-get -y update
RUN apt-get -y install libfuse2
RUN apt-get -y install libgconf-2-4
RUN apt-get -y install libgtk2.0-0
RUN apt-get -y install xvfb
RUN apt-get -y install libnss3-dev
RUN apt-get -y install libasound2

# Add additional libs for python
RUN pip install plotly

# Add orca in PATH
WORKDIR /tmp
RUN wget 'https://github.com/plotly/orca/releases/download/v1.2.1/orca-1.2.1-x86_64.AppImage'
RUN chmod +x /tmp/orca-1.2.1-x86_64.AppImage
COPY files/orca /usr/bin/
RUN chmod +x /usr/bin/orca

# Create folder for prometheus-kube-csvplot application
RUN mkdir -p /tmp/prometheus-kube-csvplot
RUN mkdir -p /tmp/prometheus-kube-csvplot/config
RUN mkdir -p /tmp/prometheus-kube-csvplot/csv

COPY export_csv.py /tmp/prometheus-kube-csvplot
COPY plot.py /tmp/prometheus-kube-csvplot

COPY config/metrics.txt /tmp/prometheus-kube-csvplot/config

COPY csv/ /tmp/prometheus-kube-csvplot/csv/

WORKDIR /tmp/prometheus-kube-csvplot
