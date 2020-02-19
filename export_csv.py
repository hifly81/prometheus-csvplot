import csv
import requests
import sys
from datetime import datetime


def GetMetricsNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url), verify=False)
    names = response.json()['data']
    # filter names based on input
    with open('./metrics.txt') as input_metrics:
        lines = input_metrics.read().splitlines()
    new_names = list(set(names) & set(lines))
    return new_names


def GetNamespace():
    # filter namespace
    lines = []
    with open('./namespaces.txt') as input_namespace:
        lines = input_namespace.read().splitlines()
    return lines


if len(sys.argv) != 4:
    print('Invalid number of parameters')
    sys.exit(1)

metricNames = GetMetricsNames(sys.argv[1])
namespaces = GetNamespace()
writeHeader = True
for metricName in metricNames:
    response = requests.get('{0}/api/v1/query_range'.format(sys.argv[1]), params={'query': metricName, 'start': sys.argv[2], 'end': sys.argv[3], 'step': '5s'}, verify=False)
    results = response.json()['data']['result']
    for result in results:
        l=[]
        metric_name = result['metric'].get("__name__", '')
	namespace_name = result['metric'].get("namespace", '')
	if namespace_name not in namespaces:
            continue
	service_name = result['metric'].get("service", '')
	quantile_name = result['metric'].get("quantile", '')
        with open('csv/' + metric_name + '_' + namespace_name + '_' + service_name + '_' + quantile_name + "_" + '.csv', 'w') as file:
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
                metric_value = value_array[index + 1].replace('\'', "").strip()
                index += 2
                subl.append(t.strftime("%d/%m/%Y %H:%M:%S"))
                subl.append(metric_value)
                writer.writerow(subl)
            writeHeader = True
