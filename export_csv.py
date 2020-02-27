import csv
import requests
import sys
import re
from datetime import datetime
from os import mkdir

# filter metrics from the config file
def get_metrics_name(url):
    response = requests.get(
        '{0}/api/v1/label/__name__/values'.format(url), verify=False)
    names = response.json()['data']
    # filter names based on input
    metrics_file = 'metrics.txt'
    if len(sys.argv) > 4:
        metrics_file = sys.argv[4]

    with open('./config/' + metrics_file) as input_metrics:
        lines = input_metrics.read().splitlines()
    new_names = list(set(names) & set(lines))
    return new_names

# collect kube namespaces from the config file
def get_namespaces():
    # filter namespace
    lines = []
    with open('./config/namespaces.txt') as input_namespace:
        lines = input_namespace.read().splitlines()
    return lines

# validate a url
def check_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)


if len(sys.argv) < 4:
    print('Invalid number of arguments, a minimum of 3 arguments: <prometheus_url> <start_date> <end_date>')
    sys.exit(1)

# validate prometheus url
prometheus_url = sys.argv[1]
if check_url(prometheus_url) is None:
    print('Error passing argument <prometheus_url>: Invalid url format')
    sys.exit(1)

metricNames = get_metrics_name(prometheus_url)
namespaces = get_namespaces()
writeHeader = True
now = datetime.now
# create performance directory with timestamp
tsTitle = now().strftime('%Y-%m-%d-%H:%M:%S')
new_folder = 'csv/performance_' + tsTitle
mkdir(new_folder)

for metricName in metricNames:
    response = requests.get('{0}/api/v1/query_range'.format(prometheus_url), params={
                            'query': metricName, 'start': sys.argv[2], 'end': sys.argv[3], 'step': '30s'}, verify=False)
    results = response.json()['data']['result']
    for result in results:
        l = []
        metric_name = result['metric'].get("__name__", '')
        namespace_name = result['metric'].get("namespace", '')
        # check if metrics is from a listed namespaces
        if len(namespaces) > 0 and namespace_name not in namespaces:
            continue
        if len(namespaces) == 0:
            namespace_name = "no_namespace"
        # create a csv file with the metric
        service_name = result['metric'].get("service", '')
        exported_namespace = result['metric'].get("exported_namespace", '')
        csv_file_name = new_folder + '/' + metric_name + '_' + namespace_name + '_' + service_name + "_" + exported_namespace + '.csv'
        with open(csv_file_name, 'w') as file:
            writer = csv.writer(file)
            if writeHeader:
                writer.writerow(['timestamp', 'value'])
                writeHeader = False
            str_new = str(result['values']).replace("[", "").replace("]", "")
            value_array = str_new.split(",")
            index = 0
            while index < len(value_array) - 1:
                subl = []
                ts_value = value_array[index]
                t = datetime.utcfromtimestamp(float(ts_value))
                metric_value = value_array[index +1].replace('\'', "").replace("u", "").strip()
                index += 2
                subl.append(t.strftime("%d/%m/%Y %H:%M:%S"))
                subl.append(metric_value)
                writer.writerow(subl)
            writeHeader = True