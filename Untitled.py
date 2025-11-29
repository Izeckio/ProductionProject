from prometheus_api_client import PrometheusConnect


prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True) #Connecting to Promotheus

cpu_usage = prom.get_current_metric_value(metric_name="container_cpu_usage_seconds_total")
print(cpu_usage) #Basic implementation to show pulling metric from Prometheus