import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Last Mile Delivery Performance Dashboard",
                    layout="wide",
                    page_icon="\U0001F69A")

# ----------------------------------------------------------------------------
# Data loading & cleaning  (Stage 4)
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Last_mile_Delivery_Data.csv")

    # Strip whitespace from all string/object columns (dataset has trailing spaces,
    # e.g. "Jam ", "Urban ", and a literal string "NaN " in Traffic)
    str_cols = df.select_dtypes(include="object").columns
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].replace({"nan": np.nan, "NaN": np.nan, "": np.nan})

    # Parse dates
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

    # Handle missing values
    # Weather / Traffic: small number of missing -> fill with "Unknown" so rows aren't lost
    df["Weather"] = df["Weather"].fillna("Unknown")
    df["Traffic"] = df["Traffic"].fillna("Unknown")

    # Agent_Rating: few missing -> fill with median rating
    df["Agent_Rating"] = df["Agent_Rating"].fillna(df["Agent_Rating"].median())

    # Drop rows missing core fields needed for every chart
    df = df.dropna(subset=["Delivery_Time", "Vehicle", "Area", "Category", "Agent_Age"])

    # Agent age groups
    df["Agent_Age_Group"] = pd.cut(
        df["Agent_Age"],
        bins=[0, 24, 40, 200],
        labels=["<25", "25-40", "40+"]
    )

    # Calculated metrics
    mean_dt = df["Delivery_Time"].mean()
    std_dt = df["Delivery_Time"].std()
    late_threshold = mean_dt + std_dt
    df["Is_Late"] = df["Delivery_Time"] > late_threshold

    return df, late_threshold

df, late_threshold = load_data()

# ----------------------------------------------------------------------------
# Sidebar filters  (Stage 6)
# ----------------------------------------------------------------------------
st.sidebar.header("Filters")

weather_opts = sorted(df["Weather"].unique())
traffic_opts = sorted(df["Traffic"].unique())
vehicle_opts = sorted(df["Vehicle"].unique())
area_opts = sorted(df["Area"].unique())
category_opts = sorted(df["Category"].unique())

sel_weather = st.sidebar.multiselect("Weather", weather_opts, default=weather_opts)
sel_traffic = st.sidebar.multiselect("Traffic", traffic_opts, default=traffic_opts)
sel_vehicle = st.sidebar.multiselect("Vehicle Type", vehicle_opts, default=vehicle_opts)
sel_area = st.sidebar.multiselect("Area", area_opts, default=area_opts)
sel_category = st.sidebar.multiselect("Product Category", category_opts, default=category_opts)

filtered = df[
    df["Weather"].isin(sel_weather) &
    df["Traffic"].isin(sel_traffic) &
    df["Vehicle"].isin(sel_vehicle) &
    df["Area"].isin(sel_area) &
    df["Category"].isin(sel_category)
]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing {len(filtered):,} of {len(df):,} deliveries")

# ----------------------------------------------------------------------------
# Header & key metrics
# ----------------------------------------------------------------------------
st.title("\U0001F69A Last Mile Delivery Performance Dashboard")
st.caption("LogiSight Analytics Pvt. Ltd. — Interactive delivery insights for operations managers")

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Deliveries", f"{len(filtered):,}")
col2.metric("Avg Delivery Time", f"{filtered['Delivery_Time'].mean():.1f} min")
late_pct = filtered["Is_Late"].mean() * 100
col3.metric("% Late Deliveries", f"{late_pct:.1f}%")
col4.metric("Avg Agent Rating", f"{filtered['Agent_Rating'].mean():.2f}")

st.markdown("---")

# ----------------------------------------------------------------------------
# Stage 5: Five compulsory visualizations + optional extras
# ----------------------------------------------------------------------------

# 1. Delay Analyzer (Bar Chart) — Delivery_Time by Weather and Traffic
st.subheader("1. Delay Analyzer: Avg Delivery Time by Weather & Traffic")
c1, c2 = st.columns(2)
with c1:
    weather_avg = filtered.groupby("Weather", as_index=False)["Delivery_Time"].mean()
    fig1a = px.bar(weather_avg, x="Weather", y="Delivery_Time",
                    title="Average Delivery Time by Weather",
                    labels={"Delivery_Time": "Avg Delivery Time (min)"},
                    color="Delivery_Time", color_continuous_scale="Blues", text_auto=".1f")
    st.plotly_chart(fig1a, use_container_width=True)
with c2:
    traffic_avg = filtered.groupby("Traffic", as_index=False)["Delivery_Time"].mean()
    fig1b = px.bar(traffic_avg, x="Traffic", y="Delivery_Time",
                    title="Average Delivery Time by Traffic",
                    labels={"Delivery_Time": "Avg Delivery Time (min)"},
                    color="Delivery_Time", color_continuous_scale="Oranges", text_auto=".1f")
    st.plotly_chart(fig1b, use_container_width=True)

# 2. Vehicle Comparison (Bar Chart)
st.subheader("2. Vehicle Comparison: Avg Delivery Time by Vehicle Type")
vehicle_avg = filtered.groupby("Vehicle", as_index=False)["Delivery_Time"].mean().sort_values("Delivery_Time")
fig2 = px.bar(vehicle_avg, x="Vehicle", y="Delivery_Time",
              title="Average Delivery Time by Vehicle Type",
              labels={"Delivery_Time": "Avg Delivery Time (min)"},
              color="Delivery_Time", color_continuous_scale="Greens", text_auto=".1f")
st.plotly_chart(fig2, use_container_width=True)

# 3. Agent Performance Scatter Plot
st.subheader("3. Agent Performance: Rating vs Delivery Time")
fig3 = px.scatter(filtered, x="Agent_Rating", y="Delivery_Time", color="Agent_Age_Group",
                   title="Agent Rating vs Delivery Time (colored by Age Group)",
                   labels={"Agent_Rating": "Agent Rating", "Delivery_Time": "Delivery Time (min)"},
                   opacity=0.6)
st.plotly_chart(fig3, use_container_width=True)

# 4. Area Heatmap
st.subheader("4. Area Heatmap: Avg Delivery Time by Area")
area_avg = filtered.groupby("Area", as_index=False)["Delivery_Time"].mean()
fig4 = px.density_heatmap(filtered, x="Area", y="Delivery_Time",
                           title="Delivery Time Distribution by Area",
                           labels={"Delivery_Time": "Delivery Time (min)"},
                           color_continuous_scale="Viridis")
st.plotly_chart(fig4, use_container_width=True)

# 5. Category Visualizer (Boxplot)
st.subheader("5. Category Visualizer: Delivery Time Distribution by Category")
fig5 = px.box(filtered, x="Category", y="Delivery_Time",
              title="Delivery Time Distribution by Product Category",
              labels={"Delivery_Time": "Delivery Time (min)"},
              color="Category")
fig5.update_layout(showlegend=False)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.header("Optional Insights")

# Optional 1: Monthly trend line chart
st.subheader("Monthly Trend: Avg Delivery Time")
monthly_avg = filtered.dropna(subset=["Month"]).groupby("Month", as_index=False)["Delivery_Time"].mean().sort_values("Month")
fig6 = px.line(monthly_avg, x="Month", y="Delivery_Time", markers=True,
               title="Average Delivery Time by Month",
               labels={"Delivery_Time": "Avg Delivery Time (min)"})
st.plotly_chart(fig6, use_container_width=True)

# Optional 2: Delivery time distribution histogram
st.subheader("Delivery Time Distribution")
fig7 = px.histogram(filtered, x="Delivery_Time", nbins=40,
                    title="Overall Delivery Time Distribution",
                    labels={"Delivery_Time": "Delivery Time (min)"})
fig7.add_vline(x=late_threshold, line_dash="dash", line_color="red",
               annotation_text="Late threshold")
st.plotly_chart(fig7, use_container_width=True)

# Optional 3: % late deliveries by traffic
st.subheader("% Late Deliveries by Traffic Condition")
late_by_traffic = filtered.groupby("Traffic", as_index=False)["Is_Late"].mean()
late_by_traffic["Is_Late"] = late_by_traffic["Is_Late"] * 100
fig8 = px.bar(late_by_traffic, x="Traffic", y="Is_Late",
              title="% Late Deliveries by Traffic",
              labels={"Is_Late": "% Late Deliveries"}, text_auto=".1f")
st.plotly_chart(fig8, use_container_width=True)

# Optional 4: Agent count per area
st.subheader("Agent Count per Area")
agent_count = filtered.groupby("Area", as_index=False)["Order_ID"].count().rename(columns={"Order_ID": "Agent_Count"})
fig9 = px.bar(agent_count, x="Area", y="Agent_Count",
              title="Number of Deliveries (as proxy for Agent Activity) per Area",
              text_auto=True)
st.plotly_chart(fig9, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit · Data: Last Mile Delivery Dataset · LogiSight Analytics Pvt. Ltd.")
