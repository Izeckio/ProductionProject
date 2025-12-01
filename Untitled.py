from prometheus_api_client import PrometheusConnect

prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True) #Connecting to Promotheus

# <!--This method pulls metrics from the cluster via prometheus
#     and provides exceptions when metrics are unable to be accessed-->
def pull_metrics():
    data = {}
    try:
        cpu_usage = prom.get_current_metric_value(metric_name="container_cpu_usage_seconds_total") 
        data["cpu_usage"] = extract_values(cpu_resp)
    except Exception as e:
        print("Error collecting CPU metrics", e)
        data["cpu_usage"] = None
    try:
        mem_usage = prom.get_current_metric_value(metric_name="container_memory_usage_bytes")
        data["mem_usage"] = extract_values(mem_resp)
    except Exception as e:
        print("Error collecting memory metrics", e)
        data["memory_usage"] = None

    try:
        net_sent = prom.get_current_metric_value(metric_name="node_network_transmit_bytes_total")
        data["net_sent"] = extract_value(net_sent_resp)
    except Exception as e:
        print("Error collecting network bytes sent", e)
        data["net_sent"] = None
    
    try:
        net_received = prom.get_current_metric_value(metric_name="node_network_receive_bytes_total")
        data["network_received"] = extract_values(net_received_resp)
    except Exception as e:
        print("Error collecting network bytes received", e)
        data["net_received"] = None

    return data

def extract_values(prom_response):
    if not prom_response or not isinstance(prom_response, list):
        return None
    try:
        _, value_str = prom_response[0]["value"]
        return float(value_str)
    except:
        return None
    
if __name__ == "__main__":
    


    