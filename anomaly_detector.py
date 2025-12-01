import pandas as pd
from sklearn.ensemble import IsolationForest


#<!-- Load the dataset that holds the captured metrics, fill na values when necessary -->
def prep_features(file_path="metrics.csv"):
    features=["cpu_usage", "mem_usage", "net_sent", "net_received"]

    df = pd.read_csv(file_path)
    df = df.fillna(0)

    X = df[features]
    return df, X

#<!-- Train the model on a dataset that is collected from an ambient system -->
def train_model(X, n_estimators=100, contamination=0.01, random_state=42):
    model = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=random_state)
    model.fit(X)
    return model

#<!-- Predict anomalies based on training and then report 
#     At this stage not very useful, as we haven't got a dataset with simulated anomalies

def predict_anomalies(df, model, X, output_file="metrics_with_anomalies.csv"):
    """Predict anomalies, add to DataFrame, print anomalies, and save results."""
    df["anomaly"] = model.predict(X)
    anomalies = df[df["anomaly"] == -1]
    print(f"Detected {len(anomalies)} anomalies out of {len(df)} rows")
    print(anomalies)
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")



#<!--Main execution -->

def main():
    df, X = prep_features()
    model = train_model(X)
    predict_anomalies(df, model, X)

if __name__ == "__main__":
    main()