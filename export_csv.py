import csv
import requests
import sys
import re
from datetime import datetime
from os import mkdir
from jproperties import Properties


# filter metrics from the config file
def get_metrics_name():
    # filter names based on input
    metrics_file = 'metrics.txt'
    if len(sys.argv) > 4:
        metrics_file = sys.argv[4]

    with open('./config/' + metrics_file) as input_metrics:
        lines = input_metrics.read().splitlines()
    new_names = list(set(lines))
    return new_names


def load_settings():
    configs = Properties()
    with open('./config/settings.properties', 'rb') as config_file:
        configs.load(config_file)
    return configs


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


# validate date input - accepts RFC 3339 or unix timestamp
def validate_date(date_string, parameter_name):
    """
    Validates date input to ensure it's either RFC 3339 format or unix timestamp.
    
    Args:
        date_string (str): The date string to validate
        parameter_name (str): Name of the parameter for error messages (e.g., 'start_date', 'end_date')
    
    Returns:
        bool: True if date is valid, False otherwise
    """
    if not date_string:
        print(f'Error: {parameter_name} cannot be empty')
        return False
    
    # Try parsing as RFC 3339 format
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        pass
    
    # Try parsing as unix timestamp
    try:
        timestamp = float(date_string)
        # Reasonable range check: between 1970 and year 2100
        if 0 <= timestamp <= 4102444800:  # Jan 1, 2100
            return True
        else:
            print(f'Error: {parameter_name} unix timestamp out of valid range (0 to 4102444800)')
            return False
    except ValueError:
        pass
    
    print(f'Error: {parameter_name} must be in RFC 3339 format (e.g., "2022-12-14T10:00:00Z") or unix timestamp (e.g., "1671012000")')
    return False


def main():
    if len(sys.argv) < 4:
        print('Invalid number of arguments, a minimum of 3 arguments: <prometheus_url> <start_date> <end_date>')
        sys.exit(1)

    # validate prometheus url
    prometheus_url = sys.argv[1]
    if check_url(prometheus_url) is None:
        print('Error passing argument <prometheus_url>: Invalid url format')
        sys.exit(1)

    # validate start_date and end_date
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    if not validate_date(start_date, 'start_date'):
        sys.exit(1)
    
    if not validate_date(end_date, 'end_date'):
        sys.exit(1)

    metric_names = get_metrics_name()
    # TODO usage of configs in settings.properties
    configs = load_settings()
    write_header = True
    now = datetime.now
    # create performance directory with timestamp
    ts_title = now().strftime('%Y-%m-%d-%H:%M:%S')
    new_folder = 'csv/metrics_' + ts_title
    mkdir(new_folder)

    for metric_name in metric_names:
        print('exported metric name:' + metric_name)
        response = requests.get('{0}/api/v1/query_range'.format(prometheus_url), params={
            'query': metric_name, 'start': sys.argv[2], 'end': sys.argv[3], 'step': '30s'}, verify=False)
        response_data = response.json()
        
        # Check if the response contains data, handle errors gracefully
        if response_data.get('status') != 'success':
            error_type = response_data.get('errorType', 'unknown')
            error_msg = response_data.get('error', 'unknown error')
            print(f'Warning: Query failed for metric "{metric_name}": {error_type} - {error_msg}')
            continue
            
        # Extract results safely
        results = response_data.get('data', {}).get('result', [])

        for result in results:
            title = metric_name
            try:
                value = result['metric']['__name__']
                title = value
            except:
                pass

            # create a csv file with the metric
            csv_file_name = new_folder + '/' + title + '.csv'
            with open(csv_file_name, 'w') as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow(['timestamp', 'value'])
                    write_header = False
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
                write_header = True


if __name__ == "__main__":
    main()
