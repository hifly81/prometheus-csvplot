## Usage


### Generate csv files from prometheus metrics
```
python export_csv.py <prometheus_url> <dateStart RFC 3339> <dateEnd RFC 3339>
```

### Create e pdf with plots from csv files
```
python plot.py <csv_directory>
```

### Execute as docker conatienr
```
docker build -t perftest .
docker run -i -t --device /dev/fuse --cap-add SYS_ADMIN perftest /bin/bash
```

