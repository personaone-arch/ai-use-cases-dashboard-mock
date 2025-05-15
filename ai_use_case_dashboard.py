import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("ai_use_cases.xlsx", skiprows=3)
    df.columns = [col.strip() for col in df.columns]
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Use Cases")
business_units = st.sidebar.multiselect("Select Business Unit(s)", df["Business Unit"].unique())
statuses = st.sidebar.multiselect("Select Status(es)", df["Current status"].unique())

filtered_df = df.copy()
if business_units:
    filtered_df = filtered_df[filtered_df["Business Unit"].isin(business_units)]
if statuses:
    filtered_df = filtered_df[filtered_df["Current status"].isin(statuses)]

# KPIs
st.title("AI Use Case Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Use Cases", len(filtered_df))
col2.metric("Total Expected Value", f"${filtered_df['Expected value'].sum():,.0f}")
col3.metric("Actual Value Realized", f"${filtered_df['Actual value realized'].sum():,.0f}")

st.markdown("---")

# Stage-wise Distribution
stage_count = filtered_df["Current status"].value_counts().reset_index()
stage_count.columns = ["Stage", "Count"]
fig_stage = px.bar(stage_count, x="Stage", y="Count", color="Stage", title="Use Cases by Stage")
st.plotly_chart(fig_stage, use_container_width=True)

# Pie Chart for RYG Status
fig_ryg = px.pie(filtered_df, names="Overall RYG status", title="Overall RYG Status Distribution")
st.plotly_chart(fig_ryg, use_container_width=True)

# Table of Filtered Use Cases
st.subheader("Filtered Use Cases")
st.dataframe(filtered_df)
