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
use_case_names = st.sidebar.multiselect("AI Use Case Name", df["AI Use Case Name"].dropna().unique())
business_units = st.sidebar.multiselect("Business Unit", df["Business Unit"].dropna().unique())
champions = st.sidebar.multiselect("Relevant champion stakeholder", df["Relevant champion stakeholder"].dropna().unique())
statuses = st.sidebar.multiselect("Current Status", df["Current status"].dropna().unique())
ryg_statuses = st.sidebar.multiselect("Overall RYG Status", df["Overall RYG status"].dropna().unique())

filtered_df = df.copy()
if use_case_names:
    filtered_df = filtered_df[filtered_df["AI Use Case Name"].isin(use_case_names)]
if business_units:
    filtered_df = filtered_df[filtered_df["Business Unit"].isin(business_units)]
if champions:
    filtered_df = filtered_df[filtered_df["Relevant champion stakeholder"].isin(champions)]
if statuses:
    filtered_df = filtered_df[filtered_df["Current status"].isin(statuses)]
if ryg_statuses:
    filtered_df = filtered_df[filtered_df["Overall RYG status"].isin(ryg_statuses)]

# KPI Strip
st.title("AI Use Case Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Use Cases (ID)", len(filtered_df))
col2.metric("Total Expected Value", f"${filtered_df['Expected value'].sum():,.0f}")
col3.metric("Actual Value Realized", f"${filtered_df['Actual value realized'].sum():,.0f}")

st.markdown("---")

# Visual 1: AI Use Cases by Business Unit & Status
st.subheader("AI Use Cases by Business Unit & Status")
status_filtered = filtered_df[filtered_df["Current status"].isin(["Prioritization", "Implementation", "Deployed"])]
bar_data1 = status_filtered.groupby(["Business Unit", "Current status"]).size().reset_index(name="Count")
fig1 = px.bar(
    bar_data1,
    x="Business Unit",
    y="Count",
    color="Current status",
    barmode="stack",
    title="AI Use Cases by Business Unit & Status"
)
st.plotly_chart(fig1, use_container_width=True)

# Visual 2: Use Case Health Status by Business Unit
st.subheader("Use Case Health Status by Business Unit")
ryg_filtered = filtered_df[filtered_df["Overall RYG status"].isin(["Red", "Yellow", "Green"])]
bar_data2 = ryg_filtered.groupby(["Business Unit", "Overall RYG status"]).size().reset_index(name="Count")
fig2 = px.bar(
    bar_data2,
    x="Business Unit",
    y="Count",
    color="Overall RYG status",
    barmode="stack",
    title="Use Case Health Status by Business Unit"
)
st.plotly_chart(fig2, use_container_width=True)

# Optional: Display filtered table
st.markdown("---")
st.subheader("Filtered Use Case Table")
st.dataframe(filtered_df)
