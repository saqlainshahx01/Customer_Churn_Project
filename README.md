# Customer Churn Prediction & Customer Segmentation System

##  Project Overview

**Customer Churn AI** is a complete, end-to-end machine learning based customer analytics system. It analyzes customer purchasing behavior to:

- Segment customers into meaningful groups (Unsupervised Learning)
- Predict which customers are likely to churn (Supervised Learning)
- Serve predictions and insights through a full web application (FastAPI + Streamlit)

The project combines **Unsupervised Learning** (customer segmentation) with **Supervised Learning** (churn prediction), making it more useful than a simple churn classifier — it answers both:

> "What type of customer is this?"
> "Is this customer likely to churn?"

---

## Problem Statement

Businesses usually have large amounts of raw transaction data, but transaction-level data alone does not answer questions like:

- Which customers are valuable?
- Which customers purchase frequently?
- Which customers have become inactive?
- Which customers are likely to leave?
- Which customers need special attention?
- How can customers be grouped into meaningful segments?

This project solves these problems by converting transaction-level retail data into **customer-level data**, then applying clustering and classification models to generate actionable insights.

---

##  Objectives

- Clean and preprocess retail transaction data
- Convert transaction-level data into customer-level data
- Engineer meaningful customer behavior features
- Segment customers using clustering algorithms
- Compare different clustering approaches
- Create a churn target for supervised learning
- Train and compare multiple classification models
- Select and save a final churn model
- Build a FastAPI backend with JWT authentication
- Add database integration and CRUD operations
- Build a Streamlit frontend with dashboard, prediction, and reporting features

---

## Dataset

**Source:** [Online Retail II – UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

The dataset contains approximately **1 million retail transactions** from an online retail store, including:

| Column | Description |
|---|---|
| Invoice | Invoice number |
| Stock Code | Product code |
| Description | Product description |
| Quantity | Units purchased |
| Invoice Date | Date of transaction |
| Price | Unit price |
| Customer ID | Unique customer identifier |
| Country | Customer's country |

---

## Data Preprocessing

- Loaded using Pandas (`pd.read_excel`)
- Removed duplicate transactions
- Removed cancelled invoices (Invoice numbers starting with `"C"`)
- Removed rows with missing Customer IDs
- Checked and handled invalid/zero quantities and prices
- Created a new feature: `TotalAmount = Quantity × Price`

---

## Exploratory Data Analysis (EDA)

Performed using **Matplotlib** and **Seaborn** to understand:

- Quantity distribution
- Price distribution
- Transaction amount distribution
- Recency distribution
- Frequency distribution
- Frequency vs Monetary relationship
- Feature correlation heatmap

---

## Customer-Level Feature Engineering

Transaction-level data was aggregated into **customer-level features** using a cutoff date, converting many transactions per customer into a single customer record.

| Feature | Description |
|---|---|
| **Recency** | Days since the customer's last purchase |
| **Frequency** | Number of unique purchases/invoices |
| **Monetary** | Total amount spent by the customer |
| **Total Quantity** | Total number of items purchased |
| **Unique Products** | Number of distinct products purchased |

Features were scaled using **StandardScaler** before clustering, since algorithms like K-Means are sensitive to feature scale.

---

## Customer Segmentation (Unsupervised Learning)

Two clustering algorithms were tested and compared:

### K-Means Clustering
- Optimal cluster count determined using the **Elbow Method** and **Silhouette Score**
- Final model: **K-Means with K = 3**
- Clusters were profiled using Recency, Frequency, Monetary, Total Quantity, and Unique Products
- Clusters mapped to meaningful business segments:
  - VIP / High-Value Customer
  - Regular / Active Customer
  - Inactive / Low-Value Customer

### DBSCAN
- Tested as an alternative density-based clustering method
- Useful for identifying dense customer groups and outliers/noise
- Multiple `eps` values tested (0.3, 0.5, 0.7, 1.0, 1.2)
- Compared against K-Means using cluster count, noise points, and Silhouette Score

### PCA (Principal Component Analysis)
- Used to reduce the 5 customer features into 2 principal components
- Primarily used for 2D visualization of customer clusters

---

## Customer Churn Prediction (Supervised Learning)

### Churn Target Creation
- Data split into a **historical period** (for features) and a **future period** (to check return activity)
- Customers with no purchase in the future period were labeled as churned (`Churn = 1`); others as active (`Churn = 0`)

### Train-Test Split
- 80/20 split using `train_test_split` with `stratify=y` to preserve class balance

### Models Trained
- **Logistic Regression** – simple, interpretable baseline with churn probability output
- **Decision Tree** – captures nonlinear rules, depth limited to reduce overfitting
- **Random Forest** – ensemble of decision trees; selected as the **final churn model**, with probability calibration (`CalibratedClassifierCV`, sigmoid method) applied for more reliable churn probabilities

### Evaluation Metrics
- Accuracy, Precision, Recall, F1 Score
- Confusion Matrix & Classification Report
- Recall and F1 Score were prioritized, since missing an about-to-churn customer is costly

### Additional Analysis
- **Threshold Analysis** across probability cutoffs (0.3, 0.5, 0.7, 0.9)
- **Overfitting Analysis** via training vs. testing accuracy gap
- **5-Fold Cross-Validation** using F1 Score across all three models

---

##  Machine Learning Pipeline

```
Raw Data → Data Cleaning → Feature Engineering → Customer Features → EDA
  → Customer Segmentation (K-Means / DBSCAN + PCA)
  → Churn Target Creation → Model Training → Model Evaluation → Final Model
```

---

## Model Deployment

Trained models and preprocessing objects were saved using **Joblib** so the backend can load them without retraining:

- `cluster_scaler.pkl`
- `kmeans_final.pkl`
- `churn_scaler.pkl`
- `churn_model.pkl`

---

## Backend (FastAPI)

The backend handles authentication, customer management, database communication, and ML predictions.

**Features:**
- User Signup & Login
- JWT-based Authentication (Bearer token)
- Customer CRUD (Create, Read, Update, Delete)
- New Customer Prediction
- Existing Customer Prediction
- Customer Reports & CSV Export
- Interactive API docs via Swagger

**Database:**
- **Users** — user ID, username, email, hashed password
- **Customers** — customer ID, Recency, Frequency, Monetary, Total Quantity, Unique Products, Country

---

## Frontend (Streamlit)

A simple, non-technical-friendly interface with the following sections:

- Login / Signup
- Dashboard (Total Customers, Avg. Recency/Frequency/Monetary)
- Customer List
- Add / Update / Delete Customer
- New Customer Prediction
- Existing Customer Prediction
- Reports (view + CSV download)
- Logout

---

## Prediction System

### New Customer Prediction
User manually enters Recency, Frequency, Monetary, Total Quantity, and Unique Products → system returns:
- Customer Cluster & Segment
- Churn Status
- Churn Probability

### Existing Customer Prediction
User enters an existing Customer ID → system retrieves stored data and returns the same outputs.

---

##  Project Architecture

```
Machine Learning  →  FastAPI Backend  →  Streamlit Frontend
```

- **ML Layer** — prepares data and trains/saves models
- **Backend Layer** — provides APIs for auth, customer management, prediction, and reports
- **Frontend Layer** — user-friendly interface for interacting with the system

---

## Project Structure

```
Customer_Churn_Project/
│
├── backend/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── database/
│
├── frontend/
│   └── app.py
│
├── models/
│   ├── cluster_scaler.pkl
│   ├── kmeans_final.pkl
│   ├── churn_scaler.pkl
│   └── churn_model.pkl
│
├── data/
│   └── online_retail_II.xlsx
│
├── customers_for_db.csv
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Technology Stack

| Category | Tools |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Clustering | K-Means, DBSCAN |
| Dimensionality Reduction | PCA |
| Classification | Logistic Regression, Decision Tree, Random Forest |
| Model Saving | Joblib |
| Backend | FastAPI, Uvicorn, Pydantic |
| Authentication | JWT, Passlib |
| Database | SQL-based database |
| Frontend | Streamlit |
| Data Formats | Excel, CSV |

---

## Requirements

```
pandas
numpy
openpyxl
matplotlib
seaborn
scikit-learn
joblib
fastapi
uvicorn
pydantic
python-jose
passlib
streamlit
requests
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Sensitive configuration is stored in a `.env` file (excluded from Git via `.gitignore`):

```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

---

## Running the Project

### Start the Backend

```bash
uvicorn backend.main:app --reload
```

API available at: `http://127.0.0.1:8000`
Interactive docs available via Swagger UI at `/docs`.

### Start the Frontend

```bash
python -m streamlit run frontend/app.py
```

The Streamlit app will open automatically in your browser.

---

## Security

- Password hashing (never stored in plain text)
- JWT-based authentication
- Protected API endpoints
- Environment variables for secrets
- `.env` excluded from version control
- Input validation via Pydantic

---

## Key Features

- User Signup & Login with JWT Authentication
- Customer Dashboard
- Customer CRUD (Add, View, Update, Delete)
- New & Existing Customer Prediction
- Customer Segmentation
- Churn Prediction with Probability Scores
- CSV Report Export
- Database Storage
- REST APIs
- Streamlit UI

---

## Why This Project Is Different

Most churn projects only perform classification. This project combines:

**Unsupervised Learning (customer segmentation) + Supervised Learning (churn prediction)**

This allows the system to answer both "what kind of customer is this?" and "is this customer likely to churn?" — making it a more complete customer analytics solution rather than a single-purpose model.

---

## Future Improvements

- Real-time customer prediction and model retraining
- Automated email alerts for high-risk customers
- Advanced customer segmentation
- Hyperparameter optimization
- XGBoost / LightGBM model comparison
- More advanced churn definitions
- Time-series customer behavior analysis
- Interactive charts and dashboards
- Role-based access control
- Cloud deployment
- Automated model performance monitoring
- Explainable AI using SHAP
- Customer retention recommendation system

---

## Conclusion

The **Customer Churn AI & Customer Segmentation System** is a complete end-to-end machine learning application that combines Data Science, Machine Learning, FastAPI, Database Management, Authentication, and Streamlit into a single practical customer analytics platform — transforming raw retail transaction data into meaningful customer insights and deployable predictions.
