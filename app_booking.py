import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("../Provider Segmentation/booking_raw.csv")

df = load_data()

# App Title
st.title("BeNeat ビニート Booking Dashboard")
st.write("This is a real booking data integrated with Streamlit app layout and features.")

####################################################################################################

# Sidebar Filters
st.sidebar.header("🔎 Filters")

# Filter by Province
province_list = df["province"].dropna().unique().tolist()
selected_province = st.sidebar.multiselect("Select Province", province_list, default=province_list)

# Filter by Booking Status
status_list = df["booking_status"].dropna().unique().tolist()
selected_status = st.sidebar.multiselect("Select Booking Status", status_list, default=status_list)

# Filter by Booking Date Range
df["booking_date"] = pd.to_datetime(df["booking_date"])
min_date = df["booking_date"].min()
max_date = df["booking_date"].max()
selected_date = st.sidebar.date_input("Booking Date Range", [min_date, max_date])

# Apply filters
filtered_df = df[
    (df["province"].isin(selected_province)) &
    (df["booking_status"].isin(selected_status)) &
    (df["booking_date"].dt.date >= selected_date[0]) &
    (df["booking_date"].dt.date <= selected_date[1])
]

####################################################################################################

# === KPI Cards ===
total_bookings = len(df)
revenue = df["total_price"].sum()
avg_booking_value = df["total_price"].mean()
new_customers = df[df["is_new_customer"] == 1]["user_id"].nunique()
conversion_rate = round((df[df["booking_status"] == "เสร็จสิ้น"].shape[0] / total_bookings) * 100, 2)
repeat_customer_rate = round((df["user_id"].duplicated().sum() / df["user_id"].nunique()) * 100, 2)
cancellations = df[df["booking_status"] != "เสร็จสิ้น"].shape[0]
cancellation_reasons = df[df["cancel_reason"].notna()]["cancel_reason"].value_counts().head(3)
cancel_display = ", ".join([f"{reason} ({count})" for reason, count in cancellation_reasons.items()])
customer_ids = df["user_id"].nunique()
churn_rate = round((1 - repeat_customer_rate / 100) * 100, 2)

# Layout Cards in Columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Bookings", total_bookings)
col1.metric("Revenue (฿)", f"{revenue:,.0f}")
col1.metric("Average Booking Value (฿)", f"{avg_booking_value:,.2f}")

col2.metric("New Customers", new_customers)
col2.metric("Conversion Rate (%)", f"{conversion_rate:.2f}%")
col2.metric("Repeat Customer Rate (%)", f"{repeat_customer_rate:.2f}%")

col3.metric("Cancellations", cancellations)
col3.metric("Top Cancel Reasons", cancel_display)
col3.metric("Customer Churn (%)", f"{churn_rate:.2f}%")

####################################################################################################

# Let's add some chart!
# Bar Chart - Booking by Hour (from `booking_date`)
df["booking_date"] = pd.to_datetime(df["booking_date"])
df["booking_hour"] = df["booking_date"].dt.hour

# Bar Chart
st.subheader("📊 Bookings by Hour")
hour_counts = df["booking_hour"].value_counts().sort_index()
fig_hour = px.bar(
    x=hour_counts.index,
    y=hour_counts.values,
    labels={"x": "Hour of Day", "y": "Number of Bookings"},
    title="Bookings by Hour"
)
st.plotly_chart(fig_hour)

# Tree Map - `place_size`
st.subheader("🌲 Booking Distribution by Place Size")
place_counts = df["place_size"].value_counts().reset_index()
place_counts.columns = ["place_size", "count"]

fig_treemap = px.treemap(
    place_counts,
    path=["place_size"],
    values="count",
    title="Treemap of Place Sizes"
)
st.plotly_chart(fig_treemap)

# Pie Chart - `cancel_reason`
st.subheader("🥧 Cancellation Reasons")
cancel_reasons = df["cancel_reason"].dropna().value_counts().reset_index()
cancel_reasons.columns = ["reason", "count"]

fig_pie = px.pie(
    cancel_reasons,
    names="reason",
    values="count",
    title="Cancellation Reasons"
)
st.plotly_chart(fig_pie)

# Table - `Top Cancel Reason`
st.subheader("🛑 Top Cancel Reasons")
top_reasons_df = df["cancel_reason"].dropna().value_counts().reset_index()
top_reasons_df.columns = ["Reason", "Count"]
st.table(top_reasons_df.head(5))  # Show full text in a table


# Extract Year-Month
df["booking_date"] = pd.to_datetime(df["booking_date"])
df["year_month"] = df["booking_date"].dt.to_period("M").astype(str)

# Customer Gain per Month
monthly_new_customers = df.groupby("year_month")["is_new_customer"].sum().reset_index()

# Professional Gain per Month
monthly_new_pros = df.groupby("year_month")["is_new_professional"].sum().reset_index()

# Plotly Charts
st.subheader("📈 Monthly New Customers")
fig_customers = px.bar(monthly_new_customers, x="year_month", y="is_new_customer",
                       labels={"year_month": "Month", "is_new_customer": "New Customers"},
                       color_discrete_sequence=["#36a2eb"])
st.plotly_chart(fig_customers, use_container_width=True)

st.subheader("👷‍♂️ Monthly New Professionals")
fig_pros = px.bar(monthly_new_pros, x="year_month", y="is_new_professional",
                  labels={"year_month": "Month", "is_new_professional": "New Professionals"},
                  color_discrete_sequence=["#ff6384"])
st.plotly_chart(fig_pros, use_container_width=True)