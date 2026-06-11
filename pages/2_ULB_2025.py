import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG

st.set_page_config(
    page_title="ULB Dashboard 2025",
    layout="wide"
)

st.title("ULB Dashboard 2025")

# LOAD DATA

df = pd.read_excel(
    "Data/ULB_2025_Cleaned.xlsx",
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

ugd_projects = (
    df["UGD Project Details - Name of UGD Project"]
    .notna()
    .sum()
)

drain_col = "Open Drainage 2025 - Sewage and Sullage flowing in open Drains (Storm water Drains / concretised Drains /unlined/ kutcha Drains)"

open_drain_ulbs = (
    pd.to_numeric(df[drain_col], errors="coerce")
    .fillna(0)
    .gt(0)
    .sum()
)

hh_connected = pd.to_numeric(
    df["UGD_HH_Connected"],
    errors="coerce"
).sum()

total_drain_flow = (
    df.groupby("(A) Name of ULB")["Total_Drain_Flow_MLD"]
      .first()
      .sum()
)

# KPI ROW

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total ULBs", total_ulbs)
c2.metric("UGD Projects", ugd_projects)
c3.metric("ULBs with Open Drains", open_drain_ulbs)
c4.metric("HH Connected", f"{hh_connected:,.0f}")
c5.metric("Total Drain Flow (MLD)", f"{total_drain_flow:.2f}")

st.divider()

# TABS

tab1, tab2, tab3 = st.tabs(
    ["UGD", "Open Drainage", "Raw Data"]
)

# UGD TAB

with tab1:

    st.subheader("Top 10 ULBs by Sewage Generated")

    sewage_data = (
        df.groupby("(A) Name of ULB")[
            "Actual Total Sewage Generation per day"
        ]
        .first()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_sewage = px.bar(
        sewage_data,
        x="Actual Total Sewage Generation per day",
        y="(A) Name of ULB",
        orientation="h"
    )

    fig_sewage.update_layout(
        xaxis_title="Sewage Generated (MLD)",
        yaxis_title="ULB"
    )

    st.plotly_chart(fig_sewage, width="stretch")


    st.subheader("UGD Stage Distribution")

    stage_df = df[
        df["UGD Project Details - Name of UGD Project"].notna()
    ]

    stage_counts = (
        stage_df["UGD Project Details - Current Stage of UGD Network"]
        .fillna("Not Reported")
        .value_counts()
        .reset_index()
    )

    stage_counts.columns = ["Stage", "Count"]

    fig_stage = px.pie(
        stage_counts,
        names="Stage",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(fig_stage, width="stretch")

    st.subheader("UGD Projects by Completion Year")

    completion_dates = pd.to_datetime(
        df["UGD Project Details - Date of Completion"],
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

    completion_years.columns = ["Year", "Projects"]

    fig_year = px.bar(
        completion_years,
        x="Year",
        y="Projects"
    )

    st.plotly_chart(fig_year, width="stretch")

    st.subheader("Top 15 ULBs by UGD Network Length")

    length_data = (
        df.groupby("(A) Name of ULB")["UGD_Length_KM"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig_length = px.bar(
        length_data,
        x="UGD_Length_KM",
        y="(A) Name of ULB",
        orientation="h"
    )

    fig_length.update_layout(
        xaxis_title="UGD Network Length (km)",
        yaxis_title="ULB"
    )

    st.plotly_chart(fig_length, width="stretch")

    st.subheader("Top ULBs by HH Connected")

    hh_summary = (
        df.groupby("(A) Name of ULB")["UGD_HH_Connected"]
        .sum()
        .sort_values(ascending=False)
    )

    hh_summary = hh_summary[hh_summary > 0]

    hh_summary = (
        hh_summary
        .head(15)
        .reset_index()
    )

    fig_hh = px.bar(
        hh_summary,
        x="UGD_HH_Connected",
        y="(A) Name of ULB",
        orientation="h"
    )

    fig_hh.update_layout(
        xaxis_title="Households Connected",
        yaxis_title="ULB"
    )

    st.plotly_chart(fig_hh, width="stretch")

    # Top ULBs by Open Drain Flow

    st.subheader("Top ULBs by Open Drain Flow (MLD)")

    flow_data = (
        df.groupby("(A) Name of ULB")["Total_Drain_Flow_MLD"]
        .first()
        .dropna()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig_flow = px.bar(
        flow_data,
        x="Total_Drain_Flow_MLD",
        y="(A) Name of ULB",
        orientation="h"
    )

    fig_flow.update_layout(
        xaxis_title="Flow (MLD)",
        yaxis_title="ULB"
    )

    st.plotly_chart(fig_flow, width="stretch")


# OPEN DRAINAGE TAB

with tab2:

    # Open Drain Count Distribution

    st.subheader("Open Drain Count Distribution")

    temp = df.copy()

    temp["Open Drains"] = pd.to_numeric(
        temp[drain_col],
        errors="coerce"
    ).fillna(0)

    temp = temp[temp["Open Drains"] > 0]

    drain_counts = (
        temp.groupby("Open Drains")
        .agg(
            ULBs=("Open Drains", "size"),
            ULB_Names=(
                "(A) Name of ULB",
                lambda x: ", ".join(
                    sorted(set(x.dropna().astype(str)))
                )
            )
        )
        .reset_index()
    )

    fig_drain = px.bar(
        drain_counts,
        x="Open Drains",
        y="ULBs",
        hover_data=["ULB_Names"]
    )

    st.plotly_chart(fig_drain, width="stretch")

    st.subheader("View ULBs by Open Drain Count")

    selected_drain = st.selectbox(
        "Select Open Drain Count",
        sorted(temp["Open Drains"].unique())
    )

    selected_ulbs = (
        temp[temp["Open Drains"] == selected_drain]
        ["(A) Name of ULB"]
        .dropna()
        .unique()
    )

    st.dataframe(
        pd.DataFrame(
            {"ULB Name": selected_ulbs}
        ),
        width="stretch"
    )

    # Discharge Destination

    st.subheader("Discharge Destination")

    discharge_df = (
        df.groupby("(A) Name of ULB")
        .agg(
            Destination=("Drain_Discharge_Type", "first")
        )
        .reset_index()
    )

    discharge_df["Destination"] = (
        discharge_df["Destination"]
        .fillna("Not Reported")
    )

    discharge = (
        discharge_df.groupby("Destination")
        .agg(
            Count=("Destination", "size"),
            ULB_Names=(
                "(A) Name of ULB",
                lambda x: ", ".join(
                    sorted(set(x.astype(str)))
                )
            )
        )
        .reset_index()
    )

    fig_discharge = px.bar(
        discharge,
        x="Destination",
        y="Count",
        hover_data=["ULB_Names"]
    )

    st.plotly_chart(fig_discharge, width="stretch")

    st.subheader("View ULBs by Discharge Destination")

    selected_destination = st.selectbox(
        "Select Destination",
        sorted(discharge_df["Destination"].dropna().unique())
    )

    destination_ulbs = (
        discharge_df[
            discharge_df["Destination"] == selected_destination
        ]
        ["(A) Name of ULB"]
    )

    st.dataframe(
        destination_ulbs.reset_index(drop=True),
        width="stretch"
    )
# RAW DATA

with tab3:

    st.dataframe(
        df,
        width="stretch"
    )