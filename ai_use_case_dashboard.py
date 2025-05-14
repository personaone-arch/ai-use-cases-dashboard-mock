import streamlit as st
import pandas as pd
import plotly.express as px
import os # Import os module to check file existence

# --- Set up the Streamlit page configuration ---
# Sets the layout to wide and the page title
st.set_page_config(layout="wide", page_title="AI Use Cases Dashboard")

# --- Display the main title of the dashboard ---
st.title("AI Use Cases Executive Dashboard")

# --- Function to load data from Excel ---
# Uses st.cache_data to cache the data, so it's only loaded once
@st.cache_data
def load_data(file_path):
    """
    Loads data from an Excel file specified by file_path.
    Includes error handling for file not found and reading issues.
    Also attempts to convert value columns to numeric.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        st.error(f"Error: The file was not found at {file_path}. Please ensure 'ai_use_cases.xlsx' is in the same directory.")
        return None
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        # Attempt to convert value columns to numeric, coercing errors to NaN
        df['Expected value'] = pd.to_numeric(df['Expected value'], errors='coerce')
        df['Actual value realized'] = pd.to_numeric(df['Actual value realized'], errors='coerce')
        return df
    except Exception as e:
        # Catch any other exceptions during file reading
        st.error(f"An error occurred while loading the Excel file: {e}")
        return None

# --- Define the path to the Excel file ---
# Make sure 'ai_use_cases.xlsx' is in the same directory as this script
excel_file_path = 'ai_use_cases.xlsx'

# --- Load the data ---
df = load_data(excel_file_path)

# --- Proceed only if data was loaded successfully ---
if df is not None:
    # --- Sidebar for Filters ---
    st.sidebar.header("Filter Options")

    # Get unique values for filters, dropping potential NaN values and sorting
    business_units = sorted(df['Business Unit'].dropna().unique().tolist())
    statuses = sorted(df['Current status'].dropna().unique().tolist())
    ryg_statuses = sorted(df['Overall RYG status'].dropna().unique().tolist())

    # Create multiselect filters in the sidebar
    selected_business_unit = st.sidebar.multiselect(
        "Select Business Unit(s):",
        options=business_units,
        default=business_units # By default, all options are selected
    )

    selected_status = st.sidebar.multiselect(
        "Select Current Status(es):",
        options=statuses,
        default=statuses # By default, all options are selected
    )

    selected_ryg_status = st.sidebar.multiselect(
        "Select Overall RYG Status(es):",
        options=ryg_statuses,
        default=ryg_statuses # By default, all options are selected
    )

    # --- Apply Filters to the DataFrame ---
    # Filter the DataFrame based on the selections made in the sidebar
    df_filtered = df[
        df['Business Unit'].isin(selected_business_unit) &
        df['Current status'].isin(selected_status) &
        df['Overall RYG status'].isin(selected_ryg_status)
    ]

    # --- Display Key Performance Indicators (KPIs) ---
    st.subheader("Key Metrics")

    # Calculate KPIs using the filtered data
    total_use_cases = df_filtered.shape[0] # Number of rows in the filtered DataFrame
    # Sum the value columns, handling potential NaN values (sum() ignores NaNs)
    total_expected_value = df_filtered['Expected value'].sum()
    total_actual_value = df_filtered['Actual value realized'].sum()

    # Function to format currency values nicely
    def format_currency(value):
        if pd.isna(value): # Check if the value is NaN
            return "$0"
        return f"${value:,.0f}" # Format as currency with comma separators and no decimals

    # Display KPIs using columns for a clean layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Use Cases", total_use_cases)
    with col2:
        st.metric("Total Expected Value", format_currency(total_expected_value))
    with col3:
        st.metric("Total Actual Value Realized", format_currency(total_actual_value))

    # --- Add a separator line ---
    st.markdown("---")

    # --- Stage-wise Chart ---
    st.subheader("Use Cases by Current Status")

    # Check if the filtered DataFrame is not empty before creating the chart
    if not df_filtered.empty:
        # Count the occurrences of each 'Current status'
        status_counts = df_filtered['Current status'].value_counts().reset_index()
        # Rename columns for clarity in the chart
        status_counts.columns = ['Current Status', 'Count']

        # Create a bar chart using Plotly Express
        fig_status = px.bar(
            status_counts,
            x='Current Status', # X-axis represents the status
            y='Count', # Y-axis represents the count
            title='Number of Use Cases by Stage', # Chart title
            labels={'Current Status': 'Stage', 'Count': 'Number of Use Cases'}, # Axis labels
            color='Current Status' # Color bars based on the status
        )
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig_status, use_container_width=True) # use_container_width makes the chart responsive
    else:
        # Display a warning if no data matches the filters for the chart
        st.warning("No data matches the selected filters to display the chart.")

    # --- Add another separator line ---
    st.markdown("---")

    # --- Optional: Display Filtered Data Table ---
    st.subheader("Filtered Use Cases Data")
    # Display the filtered DataFrame as a table
    st.dataframe(df_filtered)

else:
    # Display an error message if the data loading failed
    st.error("Dashboard data could not be loaded. Please check the Excel file path and format.")

