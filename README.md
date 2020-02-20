## Usage


### Generate csv files from prometheus metrics
```
python export_csv.py <prometheus_url> <dateStart RFC 3339> <dateEnd RFC 3339>
```

### Create e pdf with plots from csv files
```
python plot.py <csv_directory>
```
