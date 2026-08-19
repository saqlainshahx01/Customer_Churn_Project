import os
import joblib
import numpy as np
import pandas as pd
# model path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR,"models")

#loads the model
cluster_scaler = joblib.load(os.path.join(MODEL_DIR,"cluster_scaler.pkl"))
kmeans_model = joblib.load(os.path.join(MODEL_DIR,"kmeans_final.pkl"))
churn_scaler = joblib.load(os.path.join(MODEL_DIR,"churn_scaler.pkl"))
churn_model = joblib.load(os.path.join(MODEL_DIR,"churn_model.pkl"))

#feature names
FEATURES = [
    "Recency",
    "Frequency",
    "Monetary",
    "TotalQuantity",
    "UniqueProducts"
]

#segmentation
def predict_segment(
    recency,
    frequency,
    monetary,
    total_quantity,
    unique_products
):
    data = pd.DataFrame([[
    recency,
    frequency,
    monetary,
    total_quantity,
    unique_products
]], columns=FEATURES)
    scaled_data = cluster_scaler.transform(data)
    cluster = int(kmeans_model.predict(scaled_data)[0])

    segment_names = {
        0: "Inactive Customer",
        1: "VIP Customer",
        2: "Regular Customer"
    }

    return {
        "cluster": cluster,
        "segment": segment_names[cluster]
    }

#CHURN PREDICTION
def predict_churn(
    recency,
    frequency,
    monetary,
    total_quantity,
    unique_products
):
    data = pd.DataFrame([[
    recency,
    frequency,
    monetary,
    total_quantity,
    unique_products
]], columns=FEATURES)
    scaled_data = churn_scaler.transform(data)
    prediction = churn_model.predict(scaled_data)[0]
    probability = churn_model.predict_proba(scaled_data)[0][1]
    return {
        "prediction": int(prediction),
        "probability": float(probability)}

# complete segmentation and churn prediction
def predict_customer(
    recency,
    frequency,
    monetary,
    total_quantity,
    unique_products
):

    segment = predict_segment(
        recency,
        frequency,
        monetary,
        total_quantity,
        unique_products
    )

    churn = predict_churn(
        recency,
        frequency,
        monetary,
        total_quantity,
        unique_products
    )

    return {
        "cluster": segment["cluster"],
        "segment": segment["segment"],
        "churn_prediction": churn["prediction"],
        "churn_probability": churn["probability"]
    }