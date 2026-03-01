import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ------------------ Page Configuration ------------------
# ตั้งค่าหน้าเว็บ เช่น ชื่อหน้า ไอคอน และ layout แบบกว้าง
st.set_page_config(page_title="Sales Dashboard", page_icon="💰", layout="wide")

# หัวข้อหลักของหน้าเว็บ
st.title("💰 Sales Dashboard")

# คำอธิบายสั้น ๆ ใต้หัวข้อ
st.markdown(
    "Interactive dashboard for analyzing sales performance by year and category."
)


# ------------------ Dataset Creation Function ------------------
# ฟังก์ชันนี้มีหน้าที่สร้าง dataset จำลอง
# แยกออกมาเพื่อให้โค้ดเป็นระเบียบและแก้ไขง่าย
def create_dataset():

    # กำหนดค่าปี เดือน และหมวดหมู่สินค้า
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

    # กำหนด seed เพื่อให้ random เหมือนเดิมทุกครั้งที่รัน
    np.random.seed(42)

    # วนลูปสร้างข้อมูลยอดขาย
    for year in years:
        for month in months:
            for cat in categories:
                sales = np.random.randint(1000, 10000)
                data.append([year, month, cat, sales])

    # สร้าง DataFrame จากข้อมูลที่ได้
    df = pd.DataFrame(data, columns=["Year", "Month", "Category", "Sales"])

    # return ทั้ง df และ months เพื่อใช้จัดเรียงเดือน
    return df, months


# เรียกใช้ฟังก์ชันสร้าง dataset
df, months = create_dataset()


# ------------------ Sidebar Filters ------------------
# สร้างเมนูด้านข้างสำหรับเลือกปีและหมวดหมู่
st.sidebar.header("🔎 Filter Options")

# Dropdown เลือกปี
selected_year = st.sidebar.selectbox("Select Year", df["Year"].unique())

# Dropdown เลือกหมวดหมู่สินค้า
selected_category = st.sidebar.selectbox("Select Category", df["Category"].unique())


# ------------------ Data Filtering ------------------
# กรองข้อมูลตามปีที่เลือก
filtered_df = df[df["Year"] == selected_year]

# กรองข้อมูลตามปี + หมวดหมู่ที่เลือก
# ใช้ .copy() เพื่อป้องกัน SettingWithCopyWarning
filtered_cat = df[
    (df["Year"] == selected_year) & (df["Category"] == selected_category)
].copy()


# ------------------ Fix Month Order ------------------
# แปลง Month ให้เป็น Categorical เพื่อเรียง Jan → Dec ถูกต้อง
filtered_cat["Month"] = pd.Categorical(
    filtered_cat["Month"], categories=months, ordered=True
)

# เรียงข้อมูลตามเดือน
filtered_cat = filtered_cat.sort_values("Month")


# ------------------ Summary Metrics ------------------
# คำนวณค่าทางสถิติพื้นฐาน
total_sales = filtered_cat["Sales"].sum()
avg_sales = filtered_cat["Sales"].mean()
max_sales = filtered_cat["Sales"].max()

# แบ่งหน้าจอเป็น 3 คอลัมน์
col1, col2, col3 = st.columns(3)

# แสดงตัวเลขสรุป
col1.metric("💰 Total Sales", f"฿{total_sales:,}")
col2.metric("📊 Average Sales", f"{avg_sales:,.0f}")
col3.metric("🚀 Highest Month Sales", f"฿{max_sales:,}")

st.divider()


# ------------------ Highlight Best Month ------------------
# หาเดือนที่มียอดขายสูงสุด
top_month = filtered_cat.loc[filtered_cat["Sales"].idxmax(), "Month"]

st.info(f"🏆 Best Selling Month: {top_month}")


# ------------------ Download Button ------------------
# ปุ่มดาวน์โหลดข้อมูลที่ถูกกรองแล้วเป็น CSV
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_cat.to_csv(index=False),
    file_name="filtered_sales.csv",
    mime="text/csv",
)


# ------------------ Charts Section ------------------

# กราฟเส้นแสดงยอดขายรายเดือนของหมวดหมู่ที่เลือก
st.subheader("📈 Monthly Sales (Selected Category)")
fig_line = px.line(filtered_cat, x="Month", y="Sales", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# แบ่งหน้าจอเป็น 2 คอลัมน์สำหรับกราฟเพิ่มเติม
colA, colB = st.columns(2)

with colA:
    # กราฟแท่งยอดขายรวมแยกตามหมวดหมู่
    st.subheader("📊 Sales by Category")
    category_sum = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_bar = px.bar(category_sum, x="Category", y="Sales")
    st.plotly_chart(fig_bar, use_container_width=True)

with colB:
    # กราฟวงกลมสัดส่วนยอดขายแต่ละหมวดหมู่
    st.subheader("🥧 Category Distribution")
    fig_pie = px.pie(category_sum, names="Category", values="Sales")
    st.plotly_chart(fig_pie, use_container_width=True)


# ------------------ Yearly Comparison ------------------
# เปรียบเทียบยอดขายรวมแต่ละปี
st.subheader("📊 Yearly Sales Comparison")
yearly_sales = df.groupby("Year")["Sales"].sum().reset_index()
fig_year = px.bar(yearly_sales, x="Year", y="Sales")
st.plotly_chart(fig_year, use_container_width=True)


# ------------------ Footer ------------------
st.markdown("---")
st.markdown("Created for Dashboard Assignment 🚀")
