import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="ULB Dashboard 2023",
    layout="wide"
)

st.title("ULB Dashboard 2023")

# LOAD DATA
df = pd.read_csv("Data/ulb_2023_cleaned.csv")

# CLEAN DATA
numeric_cols = [
    "sewage_mld",
    "installed_stp_mld",
    "utilised_stp_mld",
    "gap_mld"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.fillna(0)

# FILTERS
col1, col2, col3 = st.columns(3)

with col1:
    district_list = ["All"] + sorted(
        df["district"].dropna().unique().tolist()
    )

    selected_district = st.selectbox(
        "Select District",
        district_list
    )

with col2:
    type_list = ["All"] + sorted(
        df["type"].dropna().unique().tolist()
    )

    selected_type = st.selectbox(
        "Select Type",
        type_list
    )

with col3:
    ulb_list = ["All"] + sorted(
        df["ulb"].dropna().unique().tolist()
    )

    selected_ulb = st.selectbox(
        "Select ULB",
        ulb_list
    )

# APPLY FILTERS
filtered_df = df.copy()

if selected_district != "All":
    filtered_df = filtered_df[
        filtered_df["district"] == selected_district
    ]

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

if selected_ulb != "All":
    filtered_df = filtered_df[
        filtered_df["ulb"] == selected_ulb
    ]

# KPI SECTION
st.subheader("Key Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Total ULBs",
        filtered_df["ulb"].nunique()
    )

with c2:
    st.metric(
        "Total Sewage (MLD)",
        round(filtered_df["sewage_mld"].sum(), 2)
    )

with c3:
    st.metric(
        "Installed Capacity",
        round(filtered_df["installed_stp_mld"].sum(), 2)
    )

with c4:
    st.metric(
        "Utilised Capacity",
        round(filtered_df["utilised_stp_mld"].sum(), 2)
    )

with c5:
    st.metric(
        "Gap (MLD)",
        round(filtered_df["gap_mld"].sum(), 2)
    )

# TOP 10 GAP
st.subheader("Top 10 ULBs by Sewage Gap")

top_gap = (
    filtered_df
    .sort_values("gap_mld", ascending=False)
    .head(10)
)

fig_gap = px.bar(
    top_gap,
    x="ulb",
    y="gap_mld",
    color="gap_mld"
)

st.plotly_chart(
    fig_gap,
    use_container_width=True
)

# TOP 10 SEWAGE
st.subheader("Top 10 ULBs by Sewage Generated")

top_sewage = (
    filtered_df
    .sort_values("sewage_mld", ascending=False)
    .head(10)
)

fig_sewage = px.bar(
    top_sewage,
    x="ulb",
    y="sewage_mld",
    color="sewage_mld"
)

st.plotly_chart(
    fig_sewage,
    use_container_width=True
)

# TOP 10 INSTALLED
st.subheader("Top 10 ULBs by Installed Capacity")

top_installed = (
    filtered_df
    .sort_values("installed_stp_mld", ascending=False)
    .head(10)
)

fig_installed = px.bar(
    top_installed,
    x="ulb",
    y="installed_stp_mld",
    color="installed_stp_mld"
)

st.plotly_chart(
    fig_installed,
    use_container_width=True
)

# TOP 10 UTILISED
st.subheader("Top 10 ULBs by Utilised Capacity")

top_utilised = (
    filtered_df
    .sort_values("utilised_stp_mld", ascending=False)
    .head(10)
)

fig_utilised = px.bar(
    top_utilised,
    x="ulb",
    y="utilised_stp_mld",
    color="utilised_stp_mld"
)

st.plotly_chart(
    fig_utilised,
    use_container_width=True
)


# TREATMENT PERFORMANCE
st.subheader("Treatment Performance")

scatter_df = filtered_df[
    (filtered_df["sewage_mld"] > 0)
    & (filtered_df["utilised_stp_mld"] > 0)
]

fig_scatter = px.scatter(
    scatter_df,
    x="sewage_mld",
    y="utilised_stp_mld",
    color="gap_mld",
    hover_name="ulb",
    title="Sewage vs Utilised Capacity"
)

fig_scatter.update_traces(
    marker=dict(
        size=12,
        opacity=0.75
    )
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# DETAILED DATA
st.subheader("Detailed ULB Data")

display_df = filtered_df.copy()

display_df = display_df.reset_index(drop=True)
display_df.index = display_df.index + 1

st.dataframe(
    display_df,
    use_container_width=True
)