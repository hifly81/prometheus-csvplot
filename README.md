Quickly run queries on prometheus and view results on csv and pdf reports with plots.

## Usage

### Metrics config

This file contains a list of Prometheus metrics to be collected.

By default, metrics are listed in file: _config/metrics.txt_

If you want to use a custom metrics file, place it in config directory:
e.g. _config/metrics_haproxy.txt_


## Run on local machine

Run prometheus and node exporter with _docker-compose_:
```
docker-compose up -d 
```

### Generate csv files from prometheus metrics

Prerequisites:

 - python v3 
 - python modules: _jproperties, requests, pandas, pillow, plotly, kaleido_

you can install those with _pip3_:

```
pip3 install jproperties requests pandas pillow plotly kaleido
```

### Generate csv files from prometheus metrics

```
python3 export_csv.py <prometheus_url> <dateStart RFC 3339 | unix_timestamp> <dateEnd RFC 3339 | unix_timestamp> <custom_metrics_file_name>
```

Example of usage:

```
python3 export_csv.py http://localhost:9090 2022-12-14T10:00:00Z 2022-12-14T11:30:00Z metrics.txt
```

A new directory named csv/metrics_%Y-%m-%d-%H:%M:%S with the csv files will be generated.

### Create a pdf report with plots from csv files

```
python3 plot.py <csv_directory>
```

Example of usage:

```
python3 plot.py csv/metrics_2022-12-14_11:20:20
```

A new pdf file *report.pdf* will be generated in directory csv/metrics_%Y-%m-%d-%H:%M:%S

## Teardown

```
docker-compose down --volumes
```