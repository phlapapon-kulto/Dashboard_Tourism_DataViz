"""
Thailand Tourism Intelligence Dashboard
Main Application Entry Point (Streamlit)
Developed based on BRD and Verified Open Data Catalog (MOTS, NESDC, TAT, NSO)
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

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Prompt', 'Sarabun', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #0D9488 100%);
        padding: 24px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0;
        padding-bottom: 6px;
    }
    .main-header p {
        color: #E2E8F0 !important;
        font-size: 0.95rem;
        margin: 0;
    }
    
    .kpi-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
        transition: transform 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.07);
    }
    .kpi-title {
        color: #64748B;
        font-size: 0.82rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #0F172A;
        font-size: 1.7rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-subtitle {
        color: #10B981;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;
    }
    .kpi-subtitle.negative {
        color: #EF4444;
    }
    .kpi-subtitle.neutral {
        color: #64748B;
    }

    .smart-card {
        background: #F8FAFC;
        border-left: 5px solid #3B82F6;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 14px;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
    }
    .smart-card.CRITICAL {
        border-left-color: #EF4444;
        background: #FEF2F2;
    }
    .smart-card.SUCCESS {
        border-left-color: #10B981;
        background: #F0FDF4;
    }
    .smart-card.OPPORTUNITY {
        border-left-color: #8B5CF6;
        background: #F5F3FF;
    }
    .smart-card.WARNING {
        border-left-color: #F59E0B;
        background: #FFFBEB;
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
    create_cluster_scatter
)

@st.cache_data
def get_cached_dataset():
    return load_data()

# Load Core Data
fact_tourism, fact_gpp, dim_province, dim_date = get_cached_dataset()

# Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>🇹🇭 Thailand Tourism Intelligence Dashboard</h1>
            <p>ระบบแดชบอร์ดอัจฉริยะวิเคราะห์ข้อมูลการท่องเที่ยวไทยเชิงลึกตามมิติเศรษฐกิจ พฤติกรรม และความพึ่งพาเชิงพื้นที่</p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 8px; backdrop-filter: blur(4px);">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">Data Sources Verified</div>
            <div style="font-weight: 600; font-size: 0.88rem;">MOTS • NESDC (สภาพัฒน์) • TAT • NSO</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🎛️ SIDEBAR: GLOBAL FILTERS
# ==========================================
st.sidebar.header("🎛️ ตัวกรองข้อมูล (Global Filters)")

# 1. Year Selector
available_years = sorted(fact_tourism["year"].unique())
year_options_map = {yr: f"พ.ศ. {yr + 543} (ค.ศ. {yr})" for yr in available_years}
selected_year = st.sidebar.selectbox(
    "📅 เลือกปี (Year)",
    options=available_years,
    index=len(available_years) - 1,  # Default to latest (2024)
    format_func=lambda yr: year_options_map[yr]
)

# 2. Month Range Filter
month_names = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
               "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
month_range = st.sidebar.slider(
    "📆 ช่วงเดือน (Month Range)",
    min_value=1,
    max_value=12,
    value=(1, 12),
    format="%d"
)
st.sidebar.caption(f"เลือกช่วง: {month_names[month_range[0]-1]} – {month_names[month_range[1]-1]}")

# 3. Region Filter
all_regions = sorted(dim_province["region"].unique())
selected_regions = st.sidebar.multiselect(
    "🗺️ ภูมิภาค (Region)",
    options=all_regions,
    default=all_regions
)

# 4. Province Filter (Filtered dynamically by Region)
filtered_provinces = dim_province[dim_province["region"].isin(selected_regions)]
province_options = sorted(filtered_provinces["province_name_th"].unique())
selected_provinces = st.sidebar.multiselect(
    "📍 จังหวัด (Provinces)",
    options=province_options,
    default=[]  # Empty means all selected
)

# 5. Visitor Type Filter
visitor_type = st.sidebar.radio(
    "👥 ประเภทนักท่องเที่ยว (Visitor Type)",
    options=["ทั้งหมด (Total)", "ชาวไทย (Domestic)", "ชาวต่างชาติ (International)"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 ดัชนีหลัก (Core Principle)")
st.sidebar.info(
    "**คำถามวิจัยเชิงยุทธศาสตร์:**\n"
    "• *ความพึ่งพาการท่องเที่ยว (Dependency Ratio)* วัดจาก **รายได้เทียบกับ GPP จังหวัด**\n"
    "• ไม่สรุปความพึ่งพาจากจำนวนนักท่องเที่ยวเพียงอย่างเดียว"
)

# ==========================================
# 🔍 FILTER LOGIC
# ==========================================
df_filtered = fact_tourism[
    (fact_tourism["year"] == selected_year) &
    (fact_tourism["month"] >= month_range[0]) &
    (fact_tourism["month"] <= month_range[1]) &
    (fact_tourism["region"].isin(selected_regions))
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
    dep_subset = dep_df[dep_df["region"].isin(selected_regions)]
top_dep_name = dep_subset.iloc[0]["province_name_th"] if not dep_subset.empty else "N/A"
top_dep_val = dep_subset.iloc[0]["dependency_ratio"] if not dep_subset.empty else 0.0

# ==========================================
# 📑 TAB SELECTION
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📊 Tab 1 — Tourism Demand & Visitors",
    "💰 Tab 2 — Tourism Revenue & Accommodation",
    "🧠 Tab 3 — Tourism Intelligence & Insights"
])

# ==============================================================================
# TAB 1: TOURISM DEMAND & VISITORS
# ==============================================================================
with tab1:
    st.subheader("อุปสงค์และพฤติกรรมการเดินทางของผู้เยี่ยมเยือน (Tourism Demand & Spatial Patterns)")
    
    # KPI Summary Cards (Row 1)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">นักท่องเที่ยวรวม (Total Visitors)</div>
            <div class="kpi-value">{total_tourists:,.0f} <span style="font-size: 1rem; font-weight: 500;">คน</span></div>
            <div class="kpi-subtitle {'negative' if tourist_growth < 0 else ''}">
                {'▲' if tourist_growth >= 0 else '▼'} {tourist_growth:+.1f}% YoY Growth
            </div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        thai_pct = (thai_tourists / total_tourists * 100) if total_tourists > 0 else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">นักท่องเที่ยวชาวไทย (Domestic)</div>
            <div class="kpi-value">{thai_tourists:,.0f} <span style="font-size: 1rem; font-weight: 500;">คน</span></div>
            <div class="kpi-subtitle neutral">สัดส่วน {thai_pct:.1f}% ของผู้เยี่ยมเยือนรวม</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        foreign_pct = (foreign_tourists / total_tourists * 100) if total_tourists > 0 else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">นักท่องเที่ยวต่างชาติ (International)</div>
            <div class="kpi-value">{foreign_tourists:,.0f} <span style="font-size: 1rem; font-weight: 500;">คน</span></div>
            <div class="kpi-subtitle neutral">สัดส่วน {foreign_pct:.1f}% ของผู้เยี่ยมเยือนรวม</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">อัตราเข้าพักเฉลี่ย (Average Occupancy)</div>
            <div class="kpi-value">{avg_occ:.1f}%</div>
            <div class="kpi-subtitle neutral">เกณฑ์เฉลี่ยมาตรฐานธุรกิจโรงแรม</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # Visualizations Row 2: Monthly Trend Line Chart & Donut Share
    r2_col1, r2_col2 = st.columns([7, 3])
    with r2_col1:
        # Determine metric according to visitor type radio
        trend_metric = "total_tourists"
        if visitor_type == "ชาวไทย (Domestic)":
            trend_metric = "thai_tourists"
        elif visitor_type == "ชาวต่างชาติ (International)":
            trend_metric = "foreign_tourists"
            
        fig_trend = create_monthly_trend_chart(fact_tourism[fact_tourism["region"].isin(selected_regions)], metric=trend_metric)
        st.plotly_chart(fig_trend, use_container_width=True)
    with r2_col2:
        fig_donut = create_visitor_share_donut(df_filtered)
        st.plotly_chart(fig_donut, use_container_width=True)

    # Visualizations Row 3: Top Provinces Bar Chart & Thailand Geospatial Map
    r3_col1, r3_col2 = st.columns([5, 5])
    with r3_col1:
        fig_top = create_top_provinces_chart(df_filtered, top_n=10, metric=trend_metric)
        st.plotly_chart(fig_top, use_container_width=True)
    with r3_col2:
        fig_map = create_thailand_map(df_filtered, metric="total_tourists")
        st.plotly_chart(fig_map, use_container_width=True)

    # Visualizations Row 4: Seasonality Analysis
    st.markdown("### ☀️ การวิเคราะห์ฤดูกาลท่องเที่ยว (Seasonality Analysis)")
    fig_season = create_seasonality_chart(fact_tourism[fact_tourism["region"].isin(selected_regions)])
    st.plotly_chart(fig_season, use_container_width=True)

# ==============================================================================
# TAB 2: TOURISM REVENUE & ACCOMMODATION
# ==============================================================================
with tab2:
    st.subheader("รายได้ทางเศรษฐกิจและการใช้บริการที่พัก (Economic Revenue & Accommodation Performance)")
    
    # KPI Summary Cards (Row 1)
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">รายได้รวมจากการท่องเที่ยว (Total Revenue)</div>
            <div class="kpi-value">{total_revenue:,.1f} <span style="font-size: 1rem; font-weight: 500;">ล้านบาท</span></div>
            <div class="kpi-subtitle {'negative' if revenue_growth < 0 else ''}">
                {'▲' if revenue_growth >= 0 else '▼'} {revenue_growth:+.1f}% YoY Growth
            </div>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Yield per Visitor)</div>
            <div class="kpi-value">{avg_yield:,.0f} <span style="font-size: 1rem; font-weight: 500;">บาท/คน</span></div>
            <div class="kpi-subtitle neutral">การใช้จ่ายเฉลี่ยต่อทริป</div>
        </div>
        """, unsafe_allow_html=True)
    with e3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">ความพึ่งพาการท่องเที่ยวสูงสุด (Max Dependency)</div>
            <div class="kpi-value">{top_dep_val:.1f}% <span style="font-size: 1rem; font-weight: 500;">GPP</span></div>
            <div class="kpi-subtitle neutral">จังหวัด: {top_dep_name}</div>
        </div>
        """, unsafe_allow_html=True)
    with e4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">รายได้จากต่างชาติ (Foreign Revenue)</div>
            <div class="kpi-value">{foreign_revenue:,.1f} <span style="font-size: 1rem; font-weight: 500;">ล้านบาท</span></div>
            <div class="kpi-subtitle neutral">สัดส่วน {(foreign_revenue / total_revenue * 100) if total_revenue > 0 else 0:.1f}% ของรายได้รวม</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # Revenue Row 2: Revenue Trend & High Volume vs High Yield Scatter
    rev_col1, rev_col2 = st.columns([6, 4])
    with rev_col1:
        fig_rev_trend = create_monthly_trend_chart(fact_tourism[fact_tourism["region"].isin(selected_regions)], metric="total_revenue")
        st.plotly_chart(fig_rev_trend, use_container_width=True)
    with rev_col2:
        fig_vol_yield = create_volume_vs_yield_scatter(df_filtered)
        st.plotly_chart(fig_vol_yield, use_container_width=True)

    # Revenue Row 3: Occupancy Rate Benchmarking & Top Revenue Provinces
    occ_col1, occ_col2 = st.columns([5, 5])
    with occ_col1:
        fig_occ = create_occupancy_bar_chart(df_filtered)
        st.plotly_chart(fig_occ, use_container_width=True)
    with occ_col2:
        fig_rev_rank = create_top_provinces_chart(df_filtered, top_n=10, metric="total_revenue")
        st.plotly_chart(fig_rev_rank, use_container_width=True)

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

# ==============================================================================
# TAB 3: TOURISM INTELLIGENCE & ADVANCED ANALYTICS
# ==============================================================================
with tab3:
    st.subheader("ระบบอัจฉริยะวิเคราะห์โอกาสและข้อมูลเชิงลึก (Tourism Intelligence & Decision Support)")

    # 1. Automated Smart Recommendations & Strategic Policy Cards
    st.markdown("### 💡 ข้อเสนอแนะเชิงยุทธศาสตร์และอินไซต์อัตโนมัติ (Rule-Based Strategic Recommendations)")
    smart_insights = generate_smart_recommendations(df_filtered, fact_gpp, selected_year)

    rec_cols = st.columns(2)
    for i, ins in enumerate(smart_insights):
        col_idx = i % 2
        with rec_cols[col_idx]:
            st.markdown(f"""
            <div class="smart-card {ins['severity']}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 600; font-size: 0.95rem; color: #1E293B;">{ins['icon']} {ins['title']}</span>
                    <span style="font-size: 0.8rem; background: #E2E8F0; padding: 2px 8px; border-radius: 12px; font-weight: 600;">{ins['metric']}</span>
                </div>
                <div style="font-size: 0.88rem; color: #334155; line-height: 1.5;">{ins['body']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # 2. Opportunity Matrix (Four-Quadrant Scatter Plot)
    st.markdown("### 🎯 เมทริกซ์วิเคราะห์โอกาสเชิงยุทธศาสตร์ (4-Quadrant Opportunity Matrix)")
    st.caption("แกน X: รายได้เฉลี่ยต่อหัว (Yield Baht) | แกน Y: อัตราการเติบโตของรายได้ (YoY Growth Rate %)")
    matrix_df, med_yield, med_growth = compute_opportunity_matrix(df_filtered)
    fig_matrix = create_opportunity_matrix_chart(matrix_df, med_yield, med_growth)
    st.plotly_chart(fig_matrix, use_container_width=True)

    # 3. Time Series Anomaly Detection Drilldown
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
        st.metric("จำนวนช่วงเวลาที่พบความผิดปกติ", f"{anomaly_count} เดือน", delta="ตรวจพบสัญญาณเตือน" if anomaly_count > 0 else "ปกติ", delta_color="inverse")
        
    with anom_col2:
        fig_anom = create_anomaly_chart(anom_df)
        st.plotly_chart(fig_anom, use_container_width=True)

    # 4. Provincial Strategic K-Means Clustering
    st.markdown("### 🧩 การจำแนกโปรไฟล์ 77 จังหวัดด้วยการจัดกลุ่มเชิงสถิติ (Provincial K-Means Clustering)")
    st.caption("จัดกลุ่มจาก 5 ตัวแปร: ปริมาณนักท่องเที่ยว, รายได้ต่อหัว (Yield), ดัชนีความพึ่งพา GPP, สัดส่วนชาวต่างชาติ, และอัตราเข้าพัก")
    clustered_df = perform_province_clustering(fact_tourism, fact_gpp, selected_year)
    fig_clusters = create_cluster_scatter(clustered_df)
    st.plotly_chart(fig_clusters, use_container_width=True)

# ==========================================
# 📥 FOOTER & EXPORT
# ==========================================
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns([6, 3, 3])
with f_col1:
    st.caption("🇹🇭 **Thailand Tourism Intelligence Dashboard** | Designed for Antigravity Engine | Open Data Compliant")
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
