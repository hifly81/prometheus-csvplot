# Prometheus CSV Plot

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-v3.7-blue.svg)](https://www.python.org/downloads/)

A Python tool to quickly run queries on Prometheus, export results as CSV files, and generate PDF reports with visualized plots.

## Features

- 🔍 **Query Prometheus metrics** with configurable time ranges
- 📊 **Export data to CSV** format for analysis
- 📈 **Generate PDF reports** with automated plots and visualizations
- 🐳 **Docker support** for easy deployment
- ⚙️ **Flexible configuration** with custom metrics files
- 🕐 **Multiple date formats** support (RFC 3339 and Unix timestamps)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Starting Prometheus](#starting-prometheus)
  - [Exporting CSV Data](#exporting-csv-data)
  - [Generating PDF Reports](#generating-pdf-reports)
- [Examples](#examples)
- [Docker Usage](#docker-usage)
- [Teardown](#teardown)
- [License](#license)

## Prerequisites

- **Python 3.7+**
- **Prometheus instance** (can be started using the provided Docker Compose)
- Required Python packages (see [Installation](#installation))

## Installation

### Using pip

Install the required Python dependencies:

```bash
pip3 install jproperties requests pandas pillow plotly kaleido
```

### Using requirements.txt

```bash
pip3 install -r requirements.txt
```

### Using Docker

Build the Docker image:

```bash
docker build -t prometheus-csvplot .
```

## Configuration

### Metrics Configuration

A configuration file is required with a list of Prometheus metrics to be collected.

**Default metrics file:** `config/metrics.txt`

**Custom metrics file:** Place your custom metrics file in the `config/` directory  
Example: `config/metrics_haproxy.txt`

### Example Metrics Configuration

Create or edit `config/metrics.txt`:

```promql
rate(go_gc_duration_seconds[5m])
scrape_duration_seconds
prometheus_http_request_duration_seconds_bucket{handler="/api/v1/query_range", instance="localhost:9090", job="prometheus", le="0.1"}
sum(rate(http_server_requests_seconds_count{instance="application:8080", status!~"5.*"}[5m]))
```

## Usage

### Starting Prometheus

Use the provided Docker Compose file to start a Prometheus instance with Node Exporter:

```bash
docker-compose up -d
```

This will start:
- **Prometheus** on port `9090`
- **Node Exporter** for system metrics

### Exporting CSV Data

Generate CSV files from Prometheus metrics:

```bash
python3 export_csv.py <prometheus_url> <start_date> <end_date> [custom_metrics_file]
```

**Parameters:**
- `prometheus_url`: URL of your Prometheus instance
- `start_date`: Start date in RFC 3339 format or Unix timestamp
- `end_date`: End date in RFC 3339 format or Unix timestamp  
- `custom_metrics_file`: (Optional) Custom metrics file name

**Output:** A new directory `csv/metrics_YYYY-MM-DD-HH:MM:SS` containing CSV files

### Generating PDF Reports

Create a PDF report with plots from CSV files:

```bash
python3 plot.py <csv_directory>
```

**Parameters:**
- `csv_directory`: Path to the directory containing CSV files

**Output:** A `report.pdf` file in the specified CSV directory

## Examples

### Basic Usage

```bash
# Export metrics for the last hour
python3 export_csv.py http://localhost:9090 2023-12-14T10:00:00Z 2023-12-14T11:00:00Z

# Generate PDF report from exported data
python3 plot.py csv/metrics_2023-12-14-11:20:20
```

### Using Custom Metrics

```bash
# Export with custom metrics file
python3 export_csv.py http://localhost:9090 2023-12-14T10:00:00Z 2023-12-14T11:00:00Z metrics_haproxy.txt
```

### Using Unix Timestamps

```bash
# Using Unix timestamps instead of RFC 3339
python3 export_csv.py http://localhost:9090 1702554000 1702557600 metrics.txt
```

## Docker Usage

### Building and Running

```bash
# Build the image
docker build -t prometheus-csvplot .

# Run with Docker Compose
docker-compose up -d

# Run the export script
docker run --rm -v $(pwd)/csv:/app/csv prometheus-csvplot python3 export_csv.py http://prometheus:9090 2023-12-14T10:00:00Z 2023-12-14T11:00:00Z
```

## Teardown

Stop and remove all containers and volumes:

```bash
docker-compose down --volumes
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
