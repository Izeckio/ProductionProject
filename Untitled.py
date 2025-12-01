import pandas as pd
from prometheus_api_client import PrometheusConnect
import time
from datetime import datetime, timezone

prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True) #Connecting to Promotheus

# <!--This method pulls metrics from the cluster via prometheus
#     and provides exceptions when metrics are unable to be accessed-->
def pull_metrics():
    data = {"timestamp": datetime.now(timezone.utc)}
    
    metrics = {
        "cpu_usage": "container_cpu_usage_seconds_total",
        "mem_usage": "container_memory_usage_bytes",
        "net_sent": "node_network_transmit_bytes_total",
        "net_received": "node_network_receive_bytes_total"
    }
    for key, metric_name in metrics.items():
        try:
            resp = prom.get_current_metric_value(metric_name=metric_name)
            value = extract_values(resp)
            data[key] = value
            if value is None:
                print(f"{metric_name} returned no data")
        except Exception as e:
            print(f"Error collecting {metric_name}: {e}")
            data[key] = None

    return data
           

# <!-- Takes the numerical value of prometheus responses -->
def extract_values(prom_response):
    if not prom_response or not isinstance(prom_response, list) or len(prom_response) == 0:
        return None
    try:
        _, value_str = prom_response[0]["value"]
        return float(value_str)
    except Exception:
        return None

# <!-- Main function that writes the pulled metrics every 5 seconds to a csv file
def main():
    output_file = "metrics.csv"
    print(f"Collecting metrics... Writing to {output_file}")

    try:
        pd.read_csv(output_file)
        append_header = False
    except FileNotFoundError:
        append_header = True

    while True:
        try:
            row = pull_metrics()
            df = pd.DataFrame([row])
            with open(output_file, "a", newline="") as f:
                df.to_csv(f, header=append_header, index=False)
                f.flush()  
            append_header = False
        except Exception as e:
            print("Error in main loop:", e)

        time.sleep(5)

if __name__ == "__main__":
    main()


    