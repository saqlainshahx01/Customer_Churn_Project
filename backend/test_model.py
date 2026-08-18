import joblib

# Load clustering scaler
cluster_scaler = joblib.load(
    "models/cluster_scaler.pkl"
)

# Load K-Means model
kmeans = joblib.load(
    "models/kmeans_final.pkl"
)

# Load churn scaler
churn_scaler = joblib.load(
    "models/churn_scaler.pkl"
)

# Load churn model
churn_model = joblib.load(
    "models/churn_model.pkl"
)

print("Cluster scaler loaded successfully!")
print("K-Means loaded successfully!")
print("Churn scaler loaded successfully!")
print("Churn model loaded successfully!")