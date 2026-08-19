import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Customer Churn AI",
    page_icon="📊",
    layout="wide"
)

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

def safe_json(response):
    try:
        return response.json()
    except Exception:
        return response.text

def auth_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }

def require_login():
    if not st.session_state.token:
        st.warning("Please login first.")
        st.stop()

if not st.session_state.token and st.session_state.show_signup:
    st.title("🤖 Customer Churn AI")
    st.subheader("📝 Create New Account")
    st.write("Create an account to access the Customer Churn System.")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account", use_container_width=True):
        if not username or not email or not password:
            st.warning("Please fill all fields.")
        else:
            response = requests.post(
                f"{BASE_URL}/auth/signup",
                json={
                    "username": username,
                    "email": email,
                    "password": password
                }
            )
            data = safe_json(response)

            if response.status_code == 200:
                st.success("Account created successfully!")
                st.info("Please login with your new account.")
                st.session_state.show_signup = False
                st.rerun()
            else:
                if isinstance(data, dict):
                    st.error(data.get("detail", "Signup failed"))
                else:
                    st.error(data)

    st.divider()

    if st.button("← Back to Login", use_container_width=True):
        st.session_state.show_signup = False
        st.rerun()

    st.stop()

if not st.session_state.token:
    st.title("🤖 Customer Churn AI")
    st.subheader("🔐 Login")
    st.write("Login to access your Customer Churn Dashboard.")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", use_container_width=True):
        if not username or not password:
            st.warning("Please enter username and password.")
        else:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "username": username,
                    "password": password
                }
            )
            data = safe_json(response)

            if response.status_code == 200:
                st.session_state.token = data["access_token"]
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                if isinstance(data, dict):
                    st.error(data.get("detail", "Invalid username or password"))
                else:
                    st.error(data)

    st.divider()
    st.write("Don't have an account?")

    if st.button("📝 Create New Account", use_container_width=True):
        st.session_state.show_signup = True
        st.rerun()

    st.stop()

st.sidebar.title("📊 Customer Churn AI")
st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👥 Customers",
        "➕ Add Customer",
        "✏️ Update Customer",
        "🗑️ Delete Customer",
        "🤖 Customer Prediction",
        "📄 Reports"
    ]
)

st.sidebar.divider()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.token = None
    st.session_state.username = None
    st.rerun()

if menu == "🏠 Dashboard":
    require_login()
    st.title("📊 Customer Churn Dashboard")

    response = requests.get(
        f"{BASE_URL}/customers",
        headers=auth_headers()
    )
    data = safe_json(response)

    if response.status_code != 200:
        st.error(
            data.get("detail", "Unable to load customers")
            if isinstance(data, dict)
            else data
        )
        st.stop()

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No customers found in database.")
        st.stop()

    st.metric("👥 Total Customers", len(df))
    st.divider()
    st.subheader("Customer Overview")

    st.dataframe(
        df[
            [
                "customer_id",
                "recency",
                "frequency",
                "monetary",
                "country"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("📈 Quick Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Recency",
            f"{df['recency'].mean():.2f}"
        )

    with col2:
        st.metric(
            "Average Frequency",
            f"{df['frequency'].mean():.2f}"
        )

    with col3:
        st.metric(
            "Average Monetary",
            f"{df['monetary'].mean():.2f}"
        )

elif menu == "👥 Customers":
    require_login()
    st.title("👥 Customers")

    response = requests.get(
        f"{BASE_URL}/customers",
        headers=auth_headers()
    )
    data = safe_json(response)

    if response.status_code != 200:
        st.error(data)
        st.stop()

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No customers found.")
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

elif menu == "➕ Add Customer":
    require_login()
    st.title("➕ Add Customer")
    st.write("Enter the customer's purchase information.")

    with st.form("add_customer_form"):
        customer_id = st.text_input("Customer ID")

        st.caption("Days since last purchase")
        recency = st.number_input(
            "Recency",
            min_value=0.0,
            step=1.0
        )

        st.caption("Total number of purchases")
        frequency = st.number_input(
            "Frequency",
            min_value=0.0,
            step=1.0
        )

        st.caption("Total amount spent")
        monetary = st.number_input(
            "Monetary",
            min_value=0.0,
            step=10.0
        )

        st.caption("Total items purchased")
        total_quantity = st.number_input(
            "Total Quantity",
            min_value=0.0,
            step=1.0
        )

        st.caption("Different products purchased")
        unique_products = st.number_input(
            "Unique Products",
            min_value=0.0,
            step=1.0
        )

        country = st.text_input("Country")

        submit = st.form_submit_button(
            "➕ Add Customer",
            use_container_width=True
        )

    if submit:
        if not customer_id:
            st.warning("Customer ID is required.")
        else:
            response = requests.post(
                f"{BASE_URL}/customers",
                headers=auth_headers(),
                json={
                    "customer_id": customer_id,
                    "recency": recency,
                    "frequency": frequency,
                    "monetary": monetary,
                    "total_quantity": total_quantity,
                    "unique_products": unique_products,
                    "country": country
                }
            )

            data = safe_json(response)

            if response.status_code == 200:
                st.success("Customer added successfully!")
            else:
                st.error(
                    data.get(
                        "detail",
                        "Failed to add customer"
                    )
                    if isinstance(data, dict)
                    else data
                )

elif menu == "✏️ Update Customer":
    require_login()
    st.title("✏️ Update Customer")

    customer_id = st.text_input("Enter Customer ID")

    if st.button("Load Customer"):
        response = requests.get(
            f"{BASE_URL}/customers/{customer_id}",
            headers=auth_headers()
        )
        data = safe_json(response)

        if response.status_code != 200:
            st.error(
                data.get(
                    "detail",
                    "Customer not found"
                )
                if isinstance(data, dict)
                else data
            )
        else:
            st.session_state.update_customer = data
            st.success("Customer loaded.")

    if "update_customer" in st.session_state:
        customer = st.session_state.update_customer

        st.divider()
        st.subheader("Update Customer Information")

        with st.form("update_customer_form"):
            st.write(
                f"Customer ID: **{customer['customer_id']}**"
            )

            recency = st.number_input(
                "Recency",
                min_value=0.0,
                value=float(customer["recency"])
            )

            frequency = st.number_input(
                "Frequency",
                min_value=0.0,
                value=float(customer["frequency"])
            )

            monetary = st.number_input(
                "Monetary",
                min_value=0.0,
                value=float(customer["monetary"])
            )

            total_quantity = st.number_input(
                "Total Quantity",
                min_value=0.0,
                value=float(customer["total_quantity"])
            )

            unique_products = st.number_input(
                "Unique Products",
                min_value=0.0,
                value=float(customer["unique_products"])
            )

            country = st.text_input(
                "Country",
                value=customer.get("country") or ""
            )

            update_button = st.form_submit_button(
                "💾 Update Customer",
                use_container_width=True
            )

        if update_button:
            response = requests.put(
                f"{BASE_URL}/customers/{customer['customer_id']}",
                headers=auth_headers(),
                json={
                    "customer_id": customer["customer_id"],
                    "recency": recency,
                    "frequency": frequency,
                    "monetary": monetary,
                    "total_quantity": total_quantity,
                    "unique_products": unique_products,
                    "country": country
                }
            )

            data = safe_json(response)

            if response.status_code == 200:
                st.success("Customer updated successfully!")
                del st.session_state["update_customer"]
                st.rerun()
            else:
                st.error(
                    data.get(
                        "detail",
                        "Update failed"
                    )
                    if isinstance(data, dict)
                    else data
                )

elif menu == "🗑️ Delete Customer":
    require_login()
    st.title("🗑️ Delete Customer")

    customer_id = st.text_input("Enter Customer ID")

    if st.button("Find Customer"):
        response = requests.get(
            f"{BASE_URL}/customers/{customer_id}",
            headers=auth_headers()
        )
        data = safe_json(response)

        if response.status_code != 200:
            st.error(
                data.get(
                    "detail",
                    "Customer not found"
                )
                if isinstance(data, dict)
                else data
            )
        else:
            st.session_state.delete_customer = data
            st.success("Customer found.")

    if "delete_customer" in st.session_state:
        customer = st.session_state.delete_customer

        st.warning(
            f"You are going to delete customer "
            f"**{customer['customer_id']}**."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this customer."
        )

        if confirm:
            if st.button(
                "🗑️ Confirm Delete",
                use_container_width=True
            ):
                response = requests.delete(
                    f"{BASE_URL}/customers/{customer['customer_id']}",
                    headers=auth_headers()
                )

                data = safe_json(response)

                if response.status_code == 200:
                    st.success(
                        "Customer deleted successfully!"
                    )
                    del st.session_state["delete_customer"]
                    st.rerun()
                else:
                    st.error(
                        data.get(
                            "detail",
                            "Delete failed"
                        )
                        if isinstance(data, dict)
                        else data
                    )

elif menu == "🤖 Customer Prediction":
    require_login()
    st.title("🤖 Customer Prediction")

    prediction_type = st.radio(
        "Select Prediction Type",
        [
            "New Customer",
            "Existing Customer"
        ]
    )

    if prediction_type == "New Customer":
        st.subheader("New Customer Prediction")
        st.write(
            "Enter the customer's purchase information."
        )

        with st.form("prediction_form"):
            st.caption("Days since last purchase")
            recency = st.number_input(
                "Recency",
                min_value=0.0,
                step=1.0
            )

            st.caption("Total number of purchases")
            frequency = st.number_input(
                "Frequency",
                min_value=0.0,
                step=1.0
            )

            st.caption("Total amount spent")
            monetary = st.number_input(
                "Monetary",
                min_value=0.0,
                step=10.0
            )

            st.caption("Total items purchased")
            total_quantity = st.number_input(
                "Total Quantity",
                min_value=0.0,
                step=1.0
            )

            st.caption("Different products purchased")
            unique_products = st.number_input(
                "Unique Products",
                min_value=0.0,
                step=1.0
            )

            predict_button = st.form_submit_button(
                "🔮 Predict Customer",
                use_container_width=True
            )

        if predict_button:
            response = requests.post(
                f"{BASE_URL}/predict",
                headers=auth_headers(),
                json={
                    "recency": recency,
                    "frequency": frequency,
                    "monetary": monetary,
                    "total_quantity": total_quantity,
                    "unique_products": unique_products
                }
            )

            data = safe_json(response)

            if response.status_code != 200:
                st.error(
                    data.get(
                        "detail",
                        "Prediction failed"
                    )
                    if isinstance(data, dict)
                    else data
                )
            else:
                st.success("Prediction completed!")
                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Customer Segment",
                        data["segment"]
                    )
                    st.metric(
                        "Cluster",
                        data["cluster"]
                    )

                with col2:
                    if data["churn_prediction"] == 1:
                        st.metric(
                            "Churn Status",
                            "⚠️ High Risk"
                        )
                    else:
                        st.metric(
                            "Churn Status",
                            "✅ Not Churn"
                        )

                    st.metric(
                        "Churn Probability",
                        f"{data['churn_probability'] * 100:.2f}%"
                    )

    else:
        st.subheader("Existing Customer Prediction")
        st.write(
            "Enter the Customer ID to generate a prediction."
        )

        customer_id = st.text_input("Customer ID")

        if st.button(
            "🔮 Predict Existing Customer",
            use_container_width=True
        ):
            if not customer_id:
                st.warning("Please enter Customer ID.")
            else:
                response = requests.get(
                    f"{BASE_URL}/customers/"
                    f"{customer_id}/predict",
                    headers=auth_headers()
                )

                data = safe_json(response)

                if response.status_code != 200:
                    st.error(
                        data.get(
                            "detail",
                            "Customer not found"
                        )
                        if isinstance(data, dict)
                        else data
                    )
                else:
                    st.success("Prediction completed!")
                    st.divider()

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Customer Segment",
                            data["segment"]
                        )
                        st.metric(
                            "Cluster",
                            data["cluster"]
                        )

                    with col2:
                        if data["churn_prediction"] == 1:
                            st.metric(
                                "Churn Status",
                                "⚠️ High Risk"
                            )
                        else:
                            st.metric(
                                "Churn Status",
                                "✅ Not Churn"
                            )

                        st.metric(
                            "Churn Probability",
                            f"{data['churn_probability'] * 100:.2f}%"
                        )

elif menu == "📄 Reports":
    require_login()
    st.title("📄 Customer Reports")

    response = requests.get(
        f"{BASE_URL}/customers",
        headers=auth_headers()
    )

    data = safe_json(response)

    if response.status_code != 200:
        st.error(data)
        st.stop()

    df = pd.DataFrame(data)

    if df.empty:
        st.info("No customer data available.")
    else:
        st.subheader("Customer Report")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_data,
            file_name="customer_report.csv",
            mime="text/csv",
            use_container_width=True
        )