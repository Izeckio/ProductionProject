from prometheus_api_client import PrometheusConnect



prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True) #Connecting to Promotheus

# <!--This method pulls metrics from the cluster via prometheus
#     and provides exceptions when metrics are unable to be accessed-->
def pull_metrics():
    try:
        cpu_usage = prom.get_current_metric_value(metric_name="container_cpu_usage_seconds_total") 
        print("CPU Usage:", cpu_usage)
    except Exception as e:
        print("Error collecting CPU metrics", e)

    try:
        mem_usage = prom.get_current_metric_value(metric_name="container_memory_usage_bytes")
        print("Memory Usage:", mem_usage)
    except Exception as e:
        print("Error collecting memory metrics", e)

    try:
        net_sent = prom.get_current_metric_value(metric_name="node_network_receive_bytes_total")
        print("Network bytes sent:",net_sent)
    except Exception as e:
        print("Error collecting network bytes sent", e)
    
    try:
        net_received = prom.get_current_metric_value(metric_name="node_network_transmit_bytes_total")
        print("Network bytes received:",net_received)
    except Exception as e:
        print("Error collecting network bytes received", e)



if __name__ == "__main__":
    pull_metrics()


    