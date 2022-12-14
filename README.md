Get metrics in a time range using Prometheus API and create csv files.<br>
Create a pdf report containing graphs from the csv files.

## Usage

### Metrics config

This file contains a list of Prometheus metrics to be collected.

By default, metrics are listed in file: _config/metrics.txt_

If you want to use a custom metrics file, place it in config directory:
e.g. _config/metrics_haproxy.txt_


## Run on local machine

### Generate csv files from prometheus metrics

Prerequisites:

    1. python v3
    2. python modules: csv, requests, pandas, pillow, plotly, plotly-orca, kaleido

### Generate csv files from prometheus metrics

```
python export_csv.py <prometheus_url> <dateStart RFC 3339 | unix_timestamp> <dateEnd RFC 3339 | unix_timestamp> <custom_metrics_file_name>
```

Example of usage:

```
python export_csv.py http://localhost:9090 2020-02-20T10:00:00Z 2020-02-20T10:30:00Z metrics.txt
```

A new directory named *csv/performance_timestamp with the csv files will be generated.

### Create a pdf report with plots from csv files

```
python plot.py <csv_directory>
```

Example of usage:

```
python plot.py csv/performance_2020-02-20_11:20:20
```

A new pdf file *report.pdf* will be generated in directory *csv/performance_timestamp

