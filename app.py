import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("💰 Sales Dashboard")

# ----- สร้างข้อมูล -----
years = [2022, 2023, 2024]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
categories = ["Electronics", "Clothing", "Food"]

data = []

np.random.seed(42)

for year in years:
    for month in months:
        for cat in categories:
            sales = np.random.randint(1000, 10000)
            data.append([year, month, cat, sales])

df = pd.DataFrame(data, columns=["Year", "Month", "Category", "Sales"])

# ----- Interactive -----
selected_year = st.selectbox("Select Year", df["Year"].unique())
selected_category = st.selectbox("Select Category", df["Category"].unique())

filtered_df = df[df["Year"] == selected_year]
filtered_cat = df[(df["Year"] == selected_year) & (df["Category"] == selected_category)]

# ----- Summary Metrics -----
total_sales = filtered_cat["Sales"].sum()
avg_sales = filtered_cat["Sales"].mean()
max_sales = filtered_cat["Sales"].max()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"{total_sales:,}")
col2.metric("📊 Average Sales", f"{avg_sales:,.0f}")
col3.metric("🚀 Highest Month", f"{max_sales:,}")

# ----- Charts Layout -----

st.subheader("📈 Monthly Sales (Selected Category)")
fig_line = px.line(filtered_cat, x="Month", y="Sales", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

colA, colB = st.columns(2)

with colA:
    st.subheader("📊 Sales by Category")
    category_sum = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_bar = px.bar(category_sum, x="Category", y="Sales")
    st.plotly_chart(fig_bar, use_container_width=True)

with colB:
    st.subheader("🥧 Category Distribution")
    fig_pie = px.pie(category_sum, names="Category", values="Sales")
    st.plotly_chart(fig_pie, use_container_width=True)
