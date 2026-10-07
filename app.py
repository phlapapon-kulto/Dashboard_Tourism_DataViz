"""
Thailand Tourism Intelligence Dashboard
Main Application Entry Point (Streamlit)
Developed based on BRD and Verified Open Data Catalog (MOTS, NESDC, TAT, NSO)

Design System:
- Primary Teal: #0F766E
- Secondary Coral: #FF7F50
- Sand Background: #F5E6CA / #FFFDF9
- Fonts: IBM Plex Sans Thai / Noto Sans Thai
- Strict Visual Hierarchy, Uniform Responsive KPI Boxes, Source under every chart
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Thailand Tourism Intelligence Dashboard",
    page_icon="🇹🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Font Family */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'IBM Plex Sans Thai', 'Noto Sans Thai', -apple-system, sans-serif !important;
        overflow-x: hidden;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 100%;
        overflow-x: hidden;
    }

    /* =========================================
       SIDEBAR STYLING (#0F766E Teal Theme)
       ========================================= */
    [data-testid="stSidebar"] {
        background-color: #0F766E !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stSlider label {
        color: #F5E6CA !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* Sidebar Navigation Radio Buttons */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 6px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.22);
        border-color: #FF7F50;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background: #FF7F50 !important;
        border-color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Selectbox Dropdown Input Fields in Sidebar */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    /* Custom Slider Line & Handle Styling (Thicker Track & Handle) */
    [data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"] {
        background-color: #FF7F50 !important;
        border: 2px solid #FFFFFF !important;
        width: 22px !important;
        height: 22px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35) !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"]::after {
        content: "⭐";
        font-size: 11px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    [data-testid="stSidebar"] div[data-baseweb="slider"] > div > div {
        height: 8px !important;
        border-radius: 4px !important;
    }

    /* =========================================
       DASHBOARD TOP BANNER (Thai Tourism Visual)
       ========================================= */
    .main-header {
        background: linear-gradient(135deg, rgba(15, 118, 110, 0.92) 0%, rgba(15, 23, 42, 0.88) 100%),
                    url('https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
        padding: 28px 36px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 6px 20px rgba(15, 118, 110, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-size: 1.95rem;
        font-weight: 700;
        margin: 0;
        padding-bottom: 6px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: #F5E6CA !important;
        font-size: 0.98rem;
        margin: 0;
        font-weight: 400;
    }

    /* =========================================
       UNIFORM KPI BOXES (Consistent Grid & Heights)
       ========================================= */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 16px;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0F766E;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        min-height: 135px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(15, 118, 110, 0.12);
        border-top-color: #FF7F50;
    }
    .kpi-title {
        color: #475569;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        line-height: 1.3;
        overflow-wrap: break-word;
    }
    .kpi-value {
        color: #0F766E;
        font-size: 1.7rem;
        font-weight: 700;
        line-height: 1.2;
        overflow-wrap: break-word;
    }
    .kpi-subtitle {
        font-size: 0.85rem;
        font-weight: 600;
        overflow-wrap: break-word;
    }
    .kpi-subtitle.positive {
        color: #0F766E;
    }
    .kpi-subtitle.negative {
        color: #FF7F50;
    }
    .kpi-subtitle.neutral {
        color: #64748B;
    }

    /* =========================================
       SOURCE UNDER CHARTS STYLING
       ========================================= */
    .chart-source {
        font-size: 0.78rem;
        color: #64748B;
        background: #FAF8F5;
        padding: 6px 12px;
        border-radius: 6px;
        border-left: 3px solid #0F766E;
        margin-top: -6px;
        margin-bottom: 22px;
        line-height: 1.4;
        overflow-wrap: break-word;
    }

    /* =========================================
       SMART RECOMMENDATION CARDS
       ========================================= */
    .smart-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0F766E;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .smart-card.CRITICAL {
        border-left-color: #FF7F50;
        background: #FFFDF9;
    }
    .smart-card.SUCCESS {
        border-left-color: #0F766E;
        background: #F0FDF4;
    }
    .smart-card.OPPORTUNITY {
        border-left-color: #D97706;
        background: #FFFBEB;
    }
    .smart-card.WARNING {
        border-left-color: #FF7F50;
        background: #FEF2F2;
    }

    /* =========================================
       TRAVEL RECOMMENDATION CARDS
       ========================================= */
    .rec-card {
        background: #FFFFFF;
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        margin-bottom: 24px;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .rec-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 22px rgba(15, 118, 110, 0.12);
        border-color: #0F766E;
    }
    .rec-img-container {
        position: relative;
        width: 100%;
        height: 210px;
        overflow: hidden;
        background-color: #E2E8F0;
    }
    .rec-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }
    .rec-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        background: #FF7F50;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.95rem;
        padding: 4px 14px;
        border-radius: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
    }
    .rec-body {
        padding: 20px;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        justify-content: space-between;
    }
    .rec-title {
        color: #0F766E;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        line-height: 1.3;
    }
    .rec-stat-bar {
        background: #FAF8F5;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 10px 0 14px 0;
        border: 1px solid #E2E8F0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
</style>
""", unsafe_allow_html=True)

# Imports for data and analytics
from src.pipeline.data_loader import load_data, compute_tourism_dependency
from src.pipeline.schema import get_dim_province
from src.analytics.intelligence import (
    compute_opportunity_matrix,
    detect_anomalies,
    generate_smart_recommendations,
    perform_province_clustering
)
from src.components.charts import (
    create_monthly_trend_chart,
    create_top_provinces_chart,
    create_thailand_map,
    create_seasonality_chart,
    create_visitor_share_donut,
    create_volume_vs_yield_scatter,
    create_occupancy_bar_chart,
    create_opportunity_matrix_chart,
    create_anomaly_chart,
    create_cluster_scatter,
    CHART_SOURCES
)
from src.components.recommendations import get_top5_recommended_provinces

# Helper function to render Source caption under every chart
def render_source(source_key: str):
    source_text = CHART_SOURCES.get(source_key, "กระทรวงการท่องเที่ยวและกีฬา (MOTS) & สำนักงานสภาพัฒนาการเศรษฐกิจและสังคมแห่งชาติ (NESDC)")
    st.markdown(f'<div class="chart-source"><b>Source:</b> {source_text}</div>', unsafe_allow_html=True)

@st.cache_data
def get_cached_dataset():
    return load_data()

# Load Core Data
fact_tourism, fact_gpp, dim_province, dim_date = get_cached_dataset()

# ==========================================
# 🎛️ SIDEBAR: NAVIGATION & FILTERS
# ==========================================

# 1. Sidebar Navigation (Moved from top tabs to Sidebar as requested)
st.sidebar.markdown("""
<div style="padding: 4px 0 12px 0;">
    <h2 style="color: #FFFFFF !important; font-size: 1.2rem; font-weight: 700; margin: 0;">🧭 นำทาง (Dashboard Pages)</h2>
    <p style="color: #F5E6CA !important; font-size: 0.8rem; margin: 2px 0 0 0;">เลือกหน้าแสดงผลเพื่อวิเคราะห์เชิงลึก</p>
</div>
""", unsafe_allow_html=True)

nav_page = st.sidebar.radio(
    "เลือกหน้าแสดงผล",
    options=[
        "📊 ภาพรวม (Overview)",
        "💰 การวิเคราะห์เศรษฐกิจ (Analysis)",
        "🧠 ระบบข้อมูลเชิงลึก (Insights)",
        "🏖️ แนะนำสถานที่ท่องเที่ยว (Travel Recommendation)"
    ],
    index=0,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 0 0 8px 0;">
    <h3 style="color: #FFFFFF !important; font-size: 1.05rem; font-weight: 700; margin: 0;">🎛️ ตัวกรองข้อมูล (Filters)</h3>
</div>
""", unsafe_allow_html=True)

# 2. Year Selector
available_years = sorted(fact_tourism["year"].unique())
year_options_map = {yr: f"พ.ศ. {yr + 543} (ค.ศ. {yr})" for yr in available_years}
selected_year = st.sidebar.selectbox(
    "📅 เลือกปี (Year)",
    options=available_years,
    index=len(available_years) - 1,  # Default to latest (2024)
    format_func=lambda yr: year_options_map[yr]
)

# 3. Month Range Filter (Enhanced Slider with bold track & ⭐ handle styling)
month_names_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_names_th = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
                  "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]

month_range = st.sidebar.slider(
    "📆 ช่วงเดือน (Month Range)",
    min_value=1,
    max_value=12,
    value=(1, 12),
    format="%d"
)

# Explicitly display selected month range
range_label_en = f"{month_names_en[month_range[0]-1]} {selected_year} — {month_names_en[month_range[1]-1]} {selected_year}"
range_label_th = f"{month_names_th[month_range[0]-1]} – {month_names_th[month_range[1]-1]} {selected_year + 543}"
st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.18); border-radius: 6px; padding: 6px 10px; margin-top: -6px; margin-bottom: 12px; font-size: 0.82rem; color: #FFFFFF; font-weight: 600; text-align: center; border: 1px solid rgba(255,255,255,0.25);">
    ⭐ {range_label_en} ({range_label_th})
</div>
""", unsafe_allow_html=True)

# 4. Region Filter (Converted from Multi-select checkboxes to Select Box / Dropdown as requested)
all_regions = sorted(dim_province["region"].unique())
region_dropdown_options = [
    "ทุกภูมิภาค (All Regions)",
    "ภาคกลาง (Central)",
    "ภาคเหนือ (North)",
    "ภาคตะวันออกเฉียงเหนือ (Northeast)",
    "ภาคใต้ (South)",
    "ภาคตะวันออก (East)",
    "ภาคตะวันตก (West)"
]

selected_region_label = st.sidebar.selectbox(
    "🗺️ ภูมิภาค (Region)",
    options=region_dropdown_options,
    index=0
)

if selected_region_label == "ทุกภูมิภาค (All Regions)":
    active_regions = all_regions
else:
    active_region_th = selected_region_label.split(" (")[0]
    active_regions = [active_region_th]

# 5. Province Filter (Filtered dynamically by chosen Region)
filtered_provinces = dim_province[dim_province["region"].isin(active_regions)]
province_options = sorted(filtered_provinces["province_name_th"].unique())
selected_provinces = st.sidebar.multiselect(
    "📍 จังหวัด (Provinces)",
    options=province_options,
    default=[]
)

# 6. Visitor Type Filter
visitor_type = st.sidebar.radio(
    "👥 ประเภทนักท่องเที่ยว (Visitor Type)",
    options=["ทั้งหมด (Total)", "ชาวไทย (Domestic)", "ชาวต่างชาติ (International)"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(255, 255, 255, 0.1); padding: 12px 14px; border-radius: 8px; border-left: 3px solid #FF7F50;">
    <div style="font-weight: 700; font-size: 0.85rem; color: #F5E6CA; margin-bottom: 4px;">📌 หลักการวิเคราะห์ (Core Principle)</div>
    <div style="font-size: 0.78rem; color: #FFFFFF; line-height: 1.4;">
        • <b>Tourism Dependency Ratio:</b> คำนวณจาก <i>รายได้ท่องเที่ยว / GPP จังหวัด</i><br>
        • ไม่สรุปความพึ่งพาจากจำนวนคนเพียงอย่างเดียว
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🔍 FILTER LOGIC
# ==========================================
df_filtered = fact_tourism[
    (fact_tourism["year"] == selected_year) &
    (fact_tourism["month"] >= month_range[0]) &
    (fact_tourism["month"] <= month_range[1]) &
    (fact_tourism["region"].isin(active_regions))
].copy()

if selected_provinces:
    df_filtered = df_filtered[df_filtered["province_name_th"].isin(selected_provinces)]

# Calculate aggregated KPI values
total_tourists = df_filtered["total_tourists"].sum()
thai_tourists = df_filtered["thai_tourists"].sum()
foreign_tourists = df_filtered["foreign_tourists"].sum()

total_revenue = df_filtered["total_revenue"].sum()
thai_revenue = df_filtered["thai_revenue"].sum()
foreign_revenue = df_filtered["foreign_revenue"].sum()

avg_occ = df_filtered["occupancy_rate"].mean() if not df_filtered.empty else 0.0
avg_yield = ((total_revenue * 1_000_000) / total_tourists) if total_tourists > 0 else 0.0

tourist_growth = df_filtered["tourists_yoy_growth"].mean() if not df_filtered.empty else 0.0
revenue_growth = df_filtered["revenue_yoy_growth"].mean() if not df_filtered.empty else 0.0

# Calculate Dependency for filtered
dep_df = compute_tourism_dependency(fact_tourism, fact_gpp, selected_year)
if selected_provinces:
    dep_subset = dep_df[dep_df["province_name_th"].isin(selected_provinces)]
else:
    dep_subset = dep_df[dep_df["region"].isin(active_regions)]
top_dep_name = dep_subset.iloc[0]["province_name_th"] if not dep_subset.empty else "N/A"
top_dep_val = dep_subset.iloc[0]["dependency_ratio"] if not dep_subset.empty else 0.0

# ==========================================
# 🏛️ TOP BANNER (Thailand Visual & Branding)
# ==========================================
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <div style="max-width: 800px;">
            <h1>🇹🇭 Thailand Tourism Intelligence Dashboard</h1>
            <p>ระบบแดชบอร์ดอัจฉริยะวิเคราะห์ข้อมูลการท่องเที่ยวไทยเชิงลึกตามมิติเศรษฐกิจ พฤติกรรม และความพึ่งพาเชิงพื้นที่</p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(255,255,255,0.25); padding: 10px 18px; border-radius: 10px; backdrop-filter: blur(8px);">
            <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #F5E6CA;">Verified Open Data Sources</div>
            <div style="font-weight: 600; font-size: 0.88rem; color: #FFFFFF;">MOTS • NESDC (สภาพัฒน์) • TAT • NSO</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# PAGE 1: 📊 ภาพรวม (OVERVIEW)
# ==============================================================================
if nav_page == "📊 ภาพรวม (Overview)":
    st.markdown("## 📊 อุปสงค์และพฤติกรรมการเดินทางของผู้เยี่ยมเยือน (Tourism Demand & Visitors)")
    st.caption(f"แสดงข้อมูลปี พ.ศ. {selected_year + 543} ({selected_year}) | ช่วงเดือน: {range_label_th} | ภูมิภาค: {selected_region_label}")

    # Uniform KPI Box Row
    thai_pct = (thai_tourists / total_tourists * 100) if total_tourists > 0 else 0
    foreign_pct = (foreign_tourists / total_tourists * 100) if total_tourists > 0 else 0

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">นักท่องเที่ยวรวม (Total Visitors)</div>
            <div class="kpi-value">{total_tourists:,.0f} <span style="font-size: 1rem; font-weight: 500;">คน</span></div>
            <div class="kpi-subtitle {'negative' if tourist_growth < 0 else 'positive'}">
                {'▲' if tourist_growth >= 0 else '▼'} {tourist_growth:+.1f}% YoY Growth
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">นักท่องเที่ยวชาวไทย (Domestic)</div>
            <div class="kpi-value">{thai_tourists:,.0f} <span style="font-size: 1rem; font-weight: 500;">คน</span></div>
            <div class="kpi-subtitle neutral">สัดส่วน {thai_pct:.1f}% ของผู้เยี่ยมเยือนรวม</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">นักท่องเที่ยวต่างชาติ (International)</div>
            <div class="kpi-value">{foreign_tourists:,.0f} <span style="font-size: 1rem; font-weight: 500;">คน</span></div>
            <div class="kpi-subtitle neutral">สัดส่วน {foreign_pct:.1f}% ของผู้เยี่ยมเยือนรวม</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">อัตราเข้าพักเฉลี่ย (Average Occupancy)</div>
            <div class="kpi-value">{avg_occ:.1f}%</div>
            <div class="kpi-subtitle neutral">เกณฑ์เฉลี่ยมาตรฐานธุรกิจโรงแรม</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Charts Row 1: Monthly Trend Line Chart & Donut Share
    r1_col1, r1_col2 = st.columns([7, 3])
    with r1_col1:
        trend_metric = "total_tourists"
        if visitor_type == "ชาวไทย (Domestic)":
            trend_metric = "thai_tourists"
        elif visitor_type == "ชาวต่างชาติ (International)":
            trend_metric = "foreign_tourists"

        fig_trend = create_monthly_trend_chart(fact_tourism[fact_tourism["region"].isin(active_regions)], metric=trend_metric)
        st.plotly_chart(fig_trend, use_container_width=True)
        render_source("monthly_trend_tourists")

    with r1_col2:
        fig_donut = create_visitor_share_donut(df_filtered)
        st.plotly_chart(fig_donut, use_container_width=True)
        render_source("visitor_share")

    # Charts Row 2: Top Provinces Bar Chart & Thailand Geospatial Map
    r2_col1, r2_col2 = st.columns([5, 5])
    with r2_col1:
        fig_top = create_top_provinces_chart(df_filtered, top_n=10, metric=trend_metric)
        st.plotly_chart(fig_top, use_container_width=True)
        render_source("top_provinces")

    with r2_col2:
        fig_map = create_thailand_map(df_filtered, metric="total_tourists")
        st.plotly_chart(fig_map, use_container_width=True)
        render_source("thailand_map")

    # Charts Row 3: Seasonality Analysis
    st.markdown("### ☀️ การวิเคราะห์ฤดูกาลท่องเที่ยวไทย (Seasonality Analysis)")
    fig_season = create_seasonality_chart(fact_tourism[fact_tourism["region"].isin(active_regions)])
    st.plotly_chart(fig_season, use_container_width=True)
    render_source("seasonality")

# ==============================================================================
# PAGE 2: 💰 การวิเคราะห์เศรษฐกิจ (ANALYSIS)
# ==============================================================================
elif nav_page == "💰 การวิเคราะห์เศรษฐกิจ (Analysis)":
    st.markdown("## 💰 รายได้ทางเศรษฐกิจและการใช้บริการที่พัก (Tourism Revenue & Accommodation)")
    st.caption(f"ประเมินมูลค่าทางเศรษฐกิจจากการท่องเที่ยวและประสิทธิภาพโครงสร้างพื้นฐานที่พัก | ปี พ.ศ. {selected_year + 543}")

    # Uniform KPI Box Row
    foreign_rev_pct = (foreign_revenue / total_revenue * 100) if total_revenue > 0 else 0

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">รายได้รวมจากการท่องเที่ยว (Total Revenue)</div>
            <div class="kpi-value">{total_revenue:,.1f} <span style="font-size: 1rem; font-weight: 500;">ล้านบาท</span></div>
            <div class="kpi-subtitle {'negative' if revenue_growth < 0 else 'positive'}">
                {'▲' if revenue_growth >= 0 else '▼'} {revenue_growth:+.1f}% YoY Growth
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Yield per Visitor)</div>
            <div class="kpi-value">{avg_yield:,.0f} <span style="font-size: 1rem; font-weight: 500;">บาท/คน</span></div>
            <div class="kpi-subtitle neutral">การใช้จ่ายเฉลี่ยต่อทริป</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">ความพึ่งพาการท่องเที่ยวสูงสุด (Max Dependency)</div>
            <div class="kpi-value">{top_dep_val:.1f}% <span style="font-size: 1rem; font-weight: 500;">GPP</span></div>
            <div class="kpi-subtitle neutral">จังหวัด: {top_dep_name}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">รายได้จากต่างชาติ (Foreign Revenue)</div>
            <div class="kpi-value">{foreign_revenue:,.1f} <span style="font-size: 1rem; font-weight: 500;">ล้านบาท</span></div>
            <div class="kpi-subtitle neutral">สัดส่วน {foreign_rev_pct:.1f}% ของรายได้รวม</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Revenue Row 1: Monthly Revenue Trend & High Volume vs High Yield Scatter
    rev_col1, rev_col2 = st.columns([6, 4])
    with rev_col1:
        fig_rev_trend = create_monthly_trend_chart(fact_tourism[fact_tourism["region"].isin(active_regions)], metric="total_revenue")
        st.plotly_chart(fig_rev_trend, use_container_width=True)
        render_source("monthly_trend_revenue")

    with rev_col2:
        fig_vol_yield = create_volume_vs_yield_scatter(df_filtered)
        st.plotly_chart(fig_vol_yield, use_container_width=True)
        render_source("volume_vs_yield")

    # Revenue Row 2: Occupancy Rate Benchmarking & Top Revenue Provinces
    occ_col1, occ_col2 = st.columns([5, 5])
    with occ_col1:
        fig_occ = create_occupancy_bar_chart(df_filtered)
        st.plotly_chart(fig_occ, use_container_width=True)
        render_source("occupancy_rate")

    with occ_col2:
        fig_rev_rank = create_top_provinces_chart(df_filtered, top_n=10, metric="total_revenue")
        st.plotly_chart(fig_rev_rank, use_container_width=True)
        render_source("top_provinces")

    # Tourism Dependency Table
    st.markdown("### 📋 ตารางดัชนีการพึ่งพาการท่องเที่ยวเทียบผลิตภัณฑ์มวลรวมจังหวัด (Tourism Dependency vs. GPP)")
    st.caption("ดัชนีพึ่งพา (%) = (รายได้จากการท่องเที่ยวรายปี / GPP จังหวัด) × 100 — ห้ามวัดความพึ่งพาจากจำนวนนักท่องเที่ยวอย่างเดียว")

    display_dep = dep_subset[[
        "province_name_th", "province_name_en", "region", "dependency_ratio",
        "total_revenue", "gpp_total", "total_tourists", "yield_per_tourist", "foreign_share_pct"
    ]].rename(columns={
        "province_name_th": "จังหวัด (TH)",
        "province_name_en": "Province (EN)",
        "region": "ภูมิภาค",
        "dependency_ratio": "ความพึ่งพา (% GPP)",
        "total_revenue": "รายได้รวม (MB)",
        "gpp_total": "GPP รวม (MB)",
        "total_tourists": "นักท่องเที่ยวรวม (คน)",
        "yield_per_tourist": "Yield ต่อหัว (บาท)",
        "foreign_share_pct": "สัดส่วนต่างชาติ (%)"
    })
    st.dataframe(display_dep.head(15), use_container_width=True)
    render_source("dependency_table")

# ==============================================================================
# PAGE 3: 🧠 ระบบข้อมูลเชิงลึก (INSIGHTS)
# ==============================================================================
elif nav_page == "🧠 ระบบข้อมูลเชิงลึก (Insights)":
    st.markdown("## 🧠 ระบบอัจฉริยะวิเคราะห์โอกาสและข้อมูลเชิงลึก (Tourism Intelligence)")
    st.caption("สังเคราะห์ข้อมูลเพื่อหาโอกาสทางธุรกิจ ตรวจจับความผิดปกติ และนำเสนอข้อเสนอแนะเชิงนโยบายอัตโนมัติ")

    # 1. Rule-Based Smart Recommendation Cards
    st.markdown("### 💡 ข้อเสนอแนะเชิงยุทธศาสตร์และอินไซต์อัตโนมัติ (Rule-Based Strategic Recommendations)")
    smart_insights = generate_smart_recommendations(df_filtered, fact_gpp, selected_year)

    rec_cols = st.columns(2)
    for i, ins in enumerate(smart_insights):
        col_idx = i % 2
        with rec_cols[col_idx]:
            st.markdown(f"""
            <div class="smart-card {ins['severity']}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; font-size: 0.95rem; color: #0F766E;">{ins['icon']} {ins['title']}</span>
                    <span style="font-size: 0.8rem; background: #FAF8F5; border: 1px solid #E2E8F0; padding: 2px 8px; border-radius: 12px; font-weight: 600; color: #FF7F50;">{ins['metric']}</span>
                </div>
                <div style="font-size: 0.88rem; color: #334155; line-height: 1.5; overflow-wrap: break-word;">{ins['body']}</div>
            </div>
            """, unsafe_allow_html=True)
    render_source("opportunity_matrix")

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # 2. Opportunity Matrix
    st.markdown("### 🎯 เมทริกซ์วิเคราะห์โอกาสเชิงยุทธศาสตร์ 4 ควอแดรนท์ (4-Quadrant Opportunity Matrix)")
    matrix_df, med_yield, med_growth = compute_opportunity_matrix(df_filtered)
    fig_matrix = create_opportunity_matrix_chart(matrix_df, med_yield, med_growth)
    st.plotly_chart(fig_matrix, use_container_width=True)
    render_source("opportunity_matrix")

    # 3. Time Series Anomaly Detection
    st.markdown("### 🚨 การตรวจจับความผิดปกติของตัวเลขนักท่องเที่ยว (Anomaly Detection)")
    anom_col1, anom_col2 = st.columns([4, 8])
    with anom_col1:
        st.markdown("**เลือกเป้าหมายการตรวจจับ:**")
        anom_target = st.selectbox(
            "จังหวัดที่ต้องการตรวจจับความผิดปกติ",
            options=["ระดับประเทศ (National)"] + sorted(dim_province["province_name_th"].tolist()),
            index=0
        )
        z_thresh = st.slider("เกณฑ์ความเข้มงวด (Z-Score Threshold)", 1.5, 3.0, 2.0, 0.1)

        selected_code = None
        if anom_target != "ระดับประเทศ (National)":
            prov_row = dim_province[dim_province["province_name_th"] == anom_target]
            if not prov_row.empty:
                selected_code = int(prov_row.iloc[0]["province_code"])

        anom_df = detect_anomalies(fact_tourism, province_code=selected_code, z_threshold=z_thresh)
        anomaly_count = anom_df[anom_df["anomaly_status"] != "Normal (ปกติ)"].shape[0]

        st.markdown(f"""
        <div style="background: #FFFFFF; border-radius: 10px; padding: 16px; border: 1px solid #E2E8F0; margin-top: 14px;">
            <div style="font-size: 0.82rem; color: #64748B; font-weight: 600;">สัญญาณเตือนความผิดปกติ</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: {'#FF7F50' if anomaly_count > 0 else '#0F766E'}; margin: 4px 0;">
                {anomaly_count} เดือน
            </div>
            <div style="font-size: 0.82rem; color: #475569;">
                {'ตรวจพบความผันผวนเกินเกณฑ์ปกติ ±2σ' if anomaly_count > 0 else 'ข้อมูลอยู่ในเกณฑ์ปกติ'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with anom_col2:
        fig_anom = create_anomaly_chart(anom_df)
        st.plotly_chart(fig_anom, use_container_width=True)
        render_source("anomaly_detection")

    # 4. Provincial Strategic K-Means Clustering
    st.markdown("### 🧩 การจำแนกโปรไฟล์ 77 จังหวัดด้วยการจัดกลุ่มเชิงสถิติ (Provincial K-Means Clustering)")
    st.caption("จัดกลุ่มจาก 5 ตัวแปร: ปริมาณนักท่องเที่ยว, รายได้ต่อหัว (Yield), ดัชนีความพึ่งพา GPP, สัดส่วนชาวต่างชาติ, และอัตราเข้าพัก")
    clustered_df = perform_province_clustering(fact_tourism, fact_gpp, selected_year)
    fig_clusters = create_cluster_scatter(clustered_df)
    st.plotly_chart(fig_clusters, use_container_width=True)
    render_source("clustering")

# ==============================================================================
# PAGE 4: 🏖️ แนะนำสถานที่ท่องเที่ยว (TRAVEL RECOMMENDATION) [NEW PAGE]
# ==============================================================================
elif nav_page == "🏖️ แนะนำสถานที่ท่องเที่ยว (Travel Recommendation)":
    st.markdown("## 🏖️ แนะนำจุดหมายปลายทางยอดนิยม (Travel Recommendation)")
    st.markdown("""
    <div style="background: #FAF8F5; border-left: 4px solid #FF7F50; padding: 14px 18px; border-radius: 8px; margin-bottom: 22px; border: 1px solid #E2E8F0;">
        <div style="font-weight: 700; font-size: 1.05rem; color: #0F766E; margin-bottom: 4px;">
            🌟 TOP 5 MOST VISITED DESTINATIONS: วิเคราะห์จากข้อมูลจริง
        </div>
        <div style="font-size: 0.92rem; color: #334155; line-height: 1.5;">
            “จากข้อมูลจำนวนนักท่องเที่ยว จังหวัดเหล่านี้เป็นจุดหมายปลายทางที่ได้รับความนิยมสูงสุดจากการจัดอันดับจริงของกระทรวงการท่องเที่ยวและกีฬา (MOTS) นำเสนอพร้อมอินไซต์เชิงลึก แหล่งท่องเที่ยวไฮไลต์ และฤดูกาลท่องเที่ยวที่เหมาะสม”
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Compute dynamically from the filtered dataset (Never hardcoded or random!)
    top5_recommendations = get_top5_recommended_provinces(df_filtered)

    if not top5_recommendations:
        st.warning("⚠️ ไม่พบข้อมูลจังหวัดตามตัวกรองที่เลือก โปรดปรับตัวกรองภูมิภาคหรือช่วงเวลา")
    else:
        # Layout in responsive columns
        # First row: 3 cards, Second row: 2 cards
        row1_cols = st.columns(3)
        for i in range(min(3, len(top5_recommendations))):
            item = top5_recommendations[i]
            meta = item["meta"]
            with row1_cols[i]:
                attractions_html = "".join([f"<li style='margin-bottom: 4px;'>{att}</li>" for att in meta["attractions"][:3]])
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-img-container">
                        <img class="rec-img" src="{meta['image_url']}" alt="{item['province_name_th']}" loading="lazy">
                        <div class="rec-badge">#{item['rank']} อันดับความนิยม</div>
                    </div>
                    <div class="rec-body">
                        <div>
                            <div class="rec-title">{item['province_name_th']} <span style="font-size: 0.95rem; font-weight: 500; color: #64748B;">({item['province_name_en']})</span></div>
                            <div style="font-size: 0.8rem; color: #FF7F50; font-weight: 600; margin-bottom: 8px;">📍 {item['region']} • {meta['travel_style']}</div>
                            <div class="rec-stat-bar">
                                <div>
                                    <div style="font-size: 0.72rem; color: #64748B;">ผู้เยี่ยมเยือน</div>
                                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F766E;">{item['total_tourists']:,.0f} คน</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 0.72rem; color: #64748B;">Yield ต่อหัว</div>
                                    <div style="font-size: 1.05rem; font-weight: 700; color: #FF7F50;">{item['yield_baht']:,.0f} บาท</div>
                                </div>
                            </div>
                            <div style="font-size: 0.88rem; font-weight: 600; color: #0F766E; margin-bottom: 4px;">📍 แหล่งท่องเที่ยวแนะนำ:</div>
                            <ul style="font-size: 0.82rem; color: #334155; padding-left: 18px; margin-bottom: 12px; line-height: 1.4;">
                                {attractions_html}
                            </ul>
                            <div style="font-size: 0.85rem; font-weight: 600; color: #0F766E; margin-bottom: 2px;">💡 อินไซต์การท่องเที่ยว:</div>
                            <div style="font-size: 0.82rem; color: #475569; line-height: 1.45; margin-bottom: 10px;">
                                {meta['why_visit']}
                            </div>
                        </div>
                        <div style="border-top: 1px dashed #E2E8F0; padding-top: 10px; margin-top: 8px;">
                            <div style="font-size: 0.76rem; color: #64748B;"><b>ช่วงเวลาที่แนะนำ:</b> {meta['best_season']}</div>
                            <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">เครดิตภาพ: {meta['image_credit']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if len(top5_recommendations) > 3:
            row2_cols = st.columns(2)
            for i in range(3, len(top5_recommendations)):
                item = top5_recommendations[i]
                meta = item["meta"]
                with row2_cols[i - 3]:
                    attractions_html = "".join([f"<li style='margin-bottom: 4px;'>{att}</li>" for att in meta["attractions"][:3]])
                    st.markdown(f"""
                    <div class="rec-card">
                        <div class="rec-img-container">
                            <img class="rec-img" src="{meta['image_url']}" alt="{item['province_name_th']}" loading="lazy">
                            <div class="rec-badge">#{item['rank']} อันดับความนิยม</div>
                        </div>
                        <div class="rec-body">
                            <div>
                                <div class="rec-title">{item['province_name_th']} <span style="font-size: 0.95rem; font-weight: 500; color: #64748B;">({item['province_name_en']})</span></div>
                                <div style="font-size: 0.8rem; color: #FF7F50; font-weight: 600; margin-bottom: 8px;">📍 {item['region']} • {meta['travel_style']}</div>
                                <div class="rec-stat-bar">
                                    <div>
                                        <div style="font-size: 0.72rem; color: #64748B;">ผู้เยี่ยมเยือน</div>
                                        <div style="font-size: 1.05rem; font-weight: 700; color: #0F766E;">{item['total_tourists']:,.0f} คน</div>
                                    </div>
                                    <div style="text-align: right;">
                                        <div style="font-size: 0.72rem; color: #64748B;">Yield ต่อหัว</div>
                                        <div style="font-size: 1.05rem; font-weight: 700; color: #FF7F50;">{item['yield_baht']:,.0f} บาท</div>
                                    </div>
                                </div>
                                <div style="font-size: 0.88rem; font-weight: 600; color: #0F766E; margin-bottom: 4px;">📍 แหล่งท่องเที่ยวแนะนำ:</div>
                                <ul style="font-size: 0.82rem; color: #334155; padding-left: 18px; margin-bottom: 12px; line-height: 1.4;">
                                    {attractions_html}
                                </ul>
                                <div style="font-size: 0.85rem; font-weight: 600; color: #0F766E; margin-bottom: 2px;">💡 อินไซต์การท่องเที่ยว:</div>
                                <div style="font-size: 0.82rem; color: #475569; line-height: 1.45; margin-bottom: 10px;">
                                    {meta['why_visit']}
                                </div>
                            </div>
                            <div style="border-top: 1px dashed #E2E8F0; padding-top: 10px; margin-top: 8px;">
                                <div style="font-size: 0.76rem; color: #64748B;"><b>ช่วงเวลาที่แนะนำ:</b> {meta['best_season']}</div>
                                <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">เครดิตภาพ: {meta['image_credit']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('<div class="chart-source"><b>Source:</b> ฐานข้อมูลสถิติผู้เยี่ยมเยือนรายจังหวัด กองเศรษฐกิจการท่องเที่ยวและกีฬา กระทรวงการท่องเที่ยวและกีฬา (MOTS) ร่วมกับการท่องเที่ยวแห่งประเทศไทย (TAT)</div>', unsafe_allow_html=True)

# ==========================================
# 📥 FOOTER & EXPORT
# ==========================================
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns([6, 3, 3])
with f_col1:
    st.caption("🇹🇭 **Thailand Tourism Intelligence Dashboard** | Designed for Antigravity Engine | Open Data Compliant (MOTS • NESDC • TAT • NSO)")
with f_col2:
    csv_data = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดข้อมูลที่กรอง (CSV)",
        data=csv_data,
        file_name=f"tourism_data_{selected_year}.csv",
        mime="text/csv",
        use_container_width=True
    )
with f_col3:
    csv_dep = dep_subset.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดดัชนี GPP (CSV)",
        data=csv_dep,
        file_name=f"tourism_dependency_{selected_year}.csv",
        mime="text/csv",
        use_container_width=True
    )
