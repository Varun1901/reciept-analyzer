import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Receipt Analyzer", layout="wide")
st.title("📊 Receipt Analyzer Dashboard")

# ✅ Helper to fetch receipts
def get_receipts():
    res = requests.get(f"{API_URL}/receipts/")
    return pd.DataFrame(res.json()) if res.status_code == 200 else pd.DataFrame()

# ✅ Helper to fetch summary
def get_summary():
    res = requests.get(f"{API_URL}/receipts/summary")
    return res.json() if res.status_code == 200 else {}

# ✅ Upload new receipt
st.sidebar.header("📤 Upload New Receipt")
uploaded_file = st.sidebar.file_uploader("Choose a receipt", type=["jpg", "png", "pdf", "txt"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    res = requests.post(f"{API_URL}/upload/", files=files)
    if res.status_code == 200:
        st.sidebar.success("✅ Uploaded & saved!")
        st.sidebar.json(res.json()["extracted_fields"])
        st.rerun()
    else:
        st.sidebar.error("❌ Upload failed!")

# ✅ Load data
df = get_receipts()
summary = get_summary()

if not df.empty:
    # --- Summary Cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Spent", f"${summary['total_spent']:.2f}")
    col2.metric("📄 Total Receipts", summary['total_receipts'])
    col3.metric("📈 Avg Receipt", f"${summary['average_spent']:.2f}")
    
    st.subheader("📄 All Receipts")
    st.dataframe(df)

    # --- Vendor Distribution ---
    st.subheader("🏪 Vendor Distribution")
    vendor_counts = df['vendor'].value_counts().reset_index()
    vendor_counts.columns = ["Vendor", "Count"]
    fig_vendor = px.bar(vendor_counts, x="Vendor", y="Count", color="Vendor", title="Receipts per Vendor")
    st.plotly_chart(fig_vendor)

    # --- Spending Trend ---
    st.subheader("📆 Monthly Spending Trend")
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        trend = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        trend['date'] = trend['date'].astype(str)
        fig_trend = px.line(trend, x="date", y="amount", title="Monthly Spend Trend")
        st.plotly_chart(fig_trend)

    # --- Edit Mode ---
    st.subheader("✏️ Edit a Receipt")
    selected_id = st.selectbox("Select Receipt ID to Edit", df["id"])
    if selected_id:
        row = df[df["id"] == selected_id].iloc[0]
        new_vendor = st.text_input("Vendor", row["vendor"])
        new_date = st.text_input("Date", row["date"])
        new_amount = st.number_input("Amount", value=float(row["amount"]))

        if st.button("Update Receipt"):
            update_payload = {
                "vendor": new_vendor,
                "date": new_date,
                "amount": new_amount
            }
            res = requests.put(f"{API_URL}/receipts/{selected_id}", params=update_payload)
            if res.status_code == 200:
                st.success("✅ Receipt updated!")
                st.rerun()
            else:
                st.error("❌ Update failed!")

    # --- Export Data ---
    st.subheader("⬇️ Export Receipts")
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "receipts.csv", "text/csv")

    json_data = df.to_json(orient="records")
    st.download_button("Download JSON", json_data, "receipts.json", "application/json")

else:
    st.warning("⚠️ No receipts found! Upload one to start analysis.")
