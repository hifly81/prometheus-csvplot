Get metrics in a time range using Promethues API and create csv files.<br>
Create a pdf report containing graphs from the csv files.

## Usage

### Metrics config

List of promethues metrics to be collected.<br>
By default metrics are listed in file:<br>
*config/metrics.txt* <br>
If you want to use a custom metrics file, create it in config directory <br>
e.g. *config/metrics_haproxy.txt*

### Namespace config

Metrics are filtered from a list of kubernetes namespaces; namespaces must be listed into file:<br>
*config/namespace.txt*<br>
If you don't want to filter metrics per namespace, leave the file namespace.txt empty.

## Run on local machine

### Generate csv files from prometheus metrics

You need:

    1. python v3
    2. python modules: csv, requests, pandas, pillow, plotly, plotly-orca

### Generate csv files from prometheus metrics

```
python export_csv.py <prometheus_url> <dateStart RFC 3339 | unix_timestamp> <dateEnd RFC 3339 | unix_timestamp> <custom_metrics_file_name>
```

Example of usage:<br>

```
python export_csv.py http://localhost:9090 2020-02-20T10:00:00Z 2020-02-20T10:30:00Z metrics.txt
```

A new directory named *csv/performance_timestamp with the csv files will be generated.

### Create a pdf report with plots from csv files

```
python plot.py <csv_directory>
```

Example of usage:<br>

```
python plot.py csv/performance_2020-02-20_11:20:20
```

A new pdf file *report.pdf* will be generated in directory *csv/performance_timestamp

## Run as a Docker container

### Pull the Docker Docker container

```
docker pull quay.io/bridlos/prometheus-kube-csvplot
```

### Run the Docker container

```
docker run -i -t --device /dev/fuse --cap-add SYS_ADMIN quay.io/bridlos/prometheus-kube-csvplot /bin/bash
```

The workdir inside the container is: */tmp/prometheus-kube-csvplot*

### Create the Docker container

```
docker build -t prometheus-kube-csvplot .
```
