## Usage

### Metrics config

List of metrics to be scraped must be listed into file config/metrics.txt

### Namespace config

List of namespace to be considered must be listed into file config/namespace.txt

### Generate csv files from prometheus metrics
```
python export_csv.py <prometheus_url> <dateStart RFC 3339> <dateEnd RFC 3339>
```

### Create a pdf report with plots from csv files
```
python plot.py <csv_directory>
```

### Execute as docker container
```
docker build -t perftest .
docker run -i -t --device /dev/fuse --cap-add SYS_ADMIN perftest /bin/bash
```

