import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG

st.set_page_config(
    page_title="ULB Dashboard 2026",
    layout="wide"
)

st.title("ULB Dashboard 2026")

# LOAD DATA

df = pd.read_excel(
    "ULB_2026_Cleaned.xlsx",
    engine="openpyxl"
)

# TOP FILTERS

c1, c2, c3 = st.columns(3)

districts = ["All"] + sorted(
    df["District Name"].dropna().unique()
)

selected_district = c1.selectbox(
    "Select District",
    districts
)

types = ["All"] + sorted(
    df["MC/RCM"].dropna().unique()
)

selected_type = c2.selectbox(
    "Select Type",
    types
)

ulbs = ["All"] + sorted(
    df["(A) Name of ULB"].dropna().unique()
)

selected_ulb = c3.selectbox(
    "Select ULB",
    ulbs
)

if selected_district != "All":
    df = df[df["District Name"] == selected_district]

if selected_type != "All":
    df = df[df["MC/RCM"] == selected_type]

if selected_ulb != "All":
    df = df[df["(A) Name of ULB"] == selected_ulb]
    
# KPI CALCULATIONS

total_ulbs = df["(A) Name of ULB"].nunique()

total_sewage = (
    df.groupby("(A) Name of ULB")
    ["Actual Total Sewage Generation per day"]
    .first()
    .sum()
)

total_stp_capacity = (
    df.groupby("(A) Name of ULB")
    ["Installed Treatment capacities of existing STPs"]
    .first()
    .sum()
)

ugd_projects = df["Name of UGD Project"].notna().sum()

hh_connected = pd.to_numeric(
    df["HH_Connected_Clean"],
    errors="coerce"
).sum()

# KPI ROW

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total ULBs", total_ulbs)
c2.metric("Total Sewage (MLD)", f"{total_sewage:,.2f}")
c3.metric("STP Capacity (MLD)", f"{total_stp_capacity:,.2f}")
c4.metric("UGD Projects", f"{ugd_projects:,}")
c5.metric("HH Connected", f"{hh_connected:,.0f}")

st.divider()

# TABS

tab1, tab2, tab3 = st.tabs(
    ["UGD", "Drainage & Sludge", "Raw Data"]
)

# UGD TAB

with tab1:

    st.subheader("Top 10 ULBs by Sewage Generation")

    sewage_data = (
        df.groupby("(A) Name of ULB")
        ["Actual Total Sewage Generation per day"]
        .first()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        sewage_data,
        x="Actual Total Sewage Generation per day",
        y="(A) Name of ULB",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("UGD Stage Distribution")

    ugd_df = df[df["Name of UGD Project"].notna()]

    stage_counts = (
        ugd_df["UGD_Stage_Clean"]
        .fillna("Not Reported")
        .value_counts()
        .reset_index()
    )

    stage_counts.columns = ["Stage", "Count"]

    fig = px.pie(
        stage_counts,
        names="Stage",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Physical Progress Categories")

    progress_df = ugd_df[
        ugd_df["Physical_Progress_Clean"].notna()
    ]

    progress_bins = pd.cut(
        progress_df["Physical_Progress_Clean"],
        bins=[0, 25, 50, 75, 99, 100],
        labels=[
            "0-25%",
            "26-50%",
            "51-75%",
            "76-99%",
            "100%"
        ],
        include_lowest=True
    )

    progress_counts = (
        progress_bins
        .value_counts()
        .sort_index()
        .reset_index()
    )

    progress_counts.columns = [
        "Progress Category",
        "Projects"
    ]

    fig = px.bar(
        progress_counts,
        x="Progress Category",
        y="Projects"
    )

    fig.update_layout(
        xaxis_title="Physical Progress",
        yaxis_title="Number of Projects"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("UGD Projects by Completion Year")

    completion_dates = pd.to_datetime(
        ugd_df["Date_Completion_Clean"],
        errors="coerce"
    )

    completion_years = (
        completion_dates.dt.year
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
        .reset_index()
    )

    completion_years.columns = [
        "Year",
        "Projects"
    ]

    completion_years["Year"] = (
        completion_years["Year"]
        .astype(str)
    )

    fig = px.bar(
        completion_years,
        x="Year",
        y="Projects"
    )

    fig.update_xaxes(
        type="category"
    )

    fig.update_layout(
        xaxis_title="Completion Year",
        yaxis_title="Number of Projects"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Top 15 ULBs by UGD Length")

    length_data = (
        ugd_df.groupby("(A) Name of ULB")
        ["UGD_Length_Clean"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        length_data,
        x="UGD_Length_Clean",
        y="(A) Name of ULB",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 15 ULBs by HH Connected")

    hh_data = (
        ugd_df.groupby("(A) Name of ULB")
        ["HH_Connected_Clean"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        hh_data,
        x="HH_Connected_Clean",
        y="(A) Name of ULB",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

# DRAINAGE & SLUDGE

with tab2:

    st.subheader("Top ULBs by Drain Flow")

    flow_data = (
        df.groupby("(A) Name of ULB")
        ["Flow_in_each_Drain_Clean"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        flow_data,
        x="Flow_in_each_Drain_Clean",
        y="(A) Name of ULB",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Drain Discharge Categories")

    discharge = (
        df["Drain_Discharge_Clean"]
        .fillna("Not Reported")
        .value_counts()
        .reset_index()
    )

    discharge.columns = ["Category", "Count"]

    fig = px.pie(
        discharge,
        names="Category",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("View Original Discharge Locations")

    selected_discharge = st.selectbox(
        "Discharge Category",
        sorted(
            df["Drain_Discharge_Clean"]
            .dropna()
            .unique()
        )
    )

    st.dataframe(
        df[
            df["Drain_Discharge_Clean"]
            == selected_discharge
        ][
            [
                "(A) Name of ULB",
                "Final point of discharge of Drain"
            ]
        ],
        use_container_width=True
    )

    st.subheader("Industrial Effluent Status")

    effluent = (
        df["Industrial_Effluent_Clean"]
        .fillna("Not Reported")
        .value_counts()
        .reset_index()
    )

    effluent.columns = ["Status", "Count"]

    fig = px.pie(
        effluent,
        names="Status",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sludge Management Distribution")

    sludge = (
        df["Management_of_Sludge_Clean"]
        .fillna("Not Reported")
        .value_counts()
        .reset_index()
    )

    sludge.columns = ["Category", "Count"]

    fig = px.pie(
        sludge,
        names="Category",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("View ULBs by Sludge Management")

    selected_sludge = st.selectbox(
        "Sludge Management Type",
        sorted(
            df["Management_of_Sludge_Clean"]
            .dropna()
            .unique()
        )
    )

    st.dataframe(
        df[
            df["Management_of_Sludge_Clean"]
            == selected_sludge
        ][
            [
                "(A) Name of ULB",
                "Management of Sludge"
            ]
        ],
        use_container_width=True
    )

# RAW DATA

with tab3:

    st.dataframe(
        df,
        use_container_width=True
    )