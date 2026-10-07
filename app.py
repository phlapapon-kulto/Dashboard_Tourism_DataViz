"""
Thailand Tourism Intelligence Dashboard - Streamlit entry point.
Dashboard-concept layout with Hero Banner, High-Contrast UI, and Full Visual Hierarchy.
"""
import re
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Thailand Tourism Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS & STYLING ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], [class*="st-"] { 
    font-family: 'IBM Plex Sans Thai', 'Noto Sans Thai', sans-serif !important; 
}

:root { 
    --tint-teal: #E3F1EE; 
    --tint-coral: #FFE8DF; 
    --tint-sand: #FBF1DD; 
    --teal: #0F766E; 
    --coral: #FF7F50; 
    --sand: #F5E6CA; 
    --ink: #0F172A; 
    --muted: #64748B; 
    --page: #FBF6EB; 
}

.stApp { background: #FFFFFF; }
.block-container { padding: 1.2rem 2rem 3rem; max-width: 100%; overflow-x: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* ---------- Left Sidebar Card ---------- */
[data-testid="stSidebar"] { 
    background: #fff; 
    border-right: 1px solid rgba(15, 118, 110, .10); 
    min-width: 300px !important; 
    max-width: 300px !important; 
}
[data-testid="stSidebar"] > div:first-child { padding: 0.6rem 0.6rem 1.5rem; }
[data-testid="stSidebarContent"] { padding: 0 .4rem; }

.brand { display: flex; align-items: center; gap: 12px; padding: 14px 8px 10px; }
.brand-logo { 
    width: 42px; height: 42px; border-radius: 50%; background: var(--teal); color: #fff; 
    display: flex; align-items: center; justify-content: center; font-weight: 700; 
    font-size: 1.05rem; box-shadow: 0 0 0 5px rgba(15, 118, 110, .14); 
}
.brand-name { font-size: 1.15rem; font-weight: 700; color: var(--teal); line-height: 1.1; }
.brand-sub { font-size: .7rem; color: var(--muted); }
.side-label { font-size: .75rem; font-weight: 600; color: #94A3B8; margin: 18px 8px 6px; letter-spacing: .02em; }

/* Navigation items */
.st-key-nav div[role="radiogroup"] { flex-direction: column; gap: 2px; width: 100%; }
.st-key-nav div[role="radiogroup"] label { 
    width: 100%; margin: 0; padding: 10px 14px; border-radius: 0 10px 10px 0; 
    border-left: 3px solid transparent; cursor: pointer; 
}
.st-key-nav div[role="radiogroup"] label > div:first-child { display: none; }
.st-key-nav div[role="radiogroup"] label p { color: var(--muted) !important; font-weight: 600; font-size: .92rem; }
.st-key-nav div[role="radiogroup"] label:hover { background: rgba(245, 230, 202, .45); }
.st-key-nav div[role="radiogroup"] label:has(input:checked) { background: rgba(15, 118, 110, .09); border-left-color: var(--teal); }
.st-key-nav div[role="radiogroup"] label:has(input:checked) p { color: var(--teal) !important; }

/* ---------- Top Bar & Search Pill ---------- */
.topbar { 
    display: flex; justify-content: space-between; align-items: center; gap: 14px; flex-wrap: wrap; 
    border-radius: 16px; padding: 12px 16px; background: var(--tint-sand); 
    border: 1px solid rgba(212, 163, 115, .40); margin-bottom: 18px; 
}
.search-pill { 
    flex: 1; min-width: 260px; display: flex; align-items: center; gap: 10px; background: #fff; 
    border-radius: 10px; padding: 10px 16px; color: var(--muted); font-size: .88rem; 
}
.search-pill svg { flex: none; }
.src-badge { background: var(--teal); color: #fff; padding: 9px 16px; border-radius: 10px; font-weight: 600; font-size: .82rem; }

/* ---------- Hero Banner (Thailand Tourism Image) ---------- */
.hero-banner {
    position: relative;
    width: 100%;
    border-radius: 20px;
    padding: 36px 32px;
    margin-bottom: 22px;
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.25) 0%, rgba(15, 23, 42, 0.65) 100%), 
                url('https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
    box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.12);
    overflow: hidden;
}
.hero-banner h1 {
    color: #FFFFFF !important;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 6px 0;
    padding: 0;
    text-shadow: 0 2px 6px rgba(0,0,0,0.4);
}
.hero-banner p {
    color: #F8FAFC !important;
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
    padding: 0;
    text-shadow: 0 1px 4px rgba(0,0,0,0.4);
    max-width: 750px;
}

/* ---------- Cards & Containers ---------- */
[data-testid="stVerticalBlockBorderWrapper"] { 
    background: #fff; border: 1px solid #EFE7D6 !important; border-radius: 18px !important;
    box-shadow: none; padding: 8px 12px 6px; overflow: hidden !important; 
}
[data-testid="stVerticalBlockBorderWrapper"]:has([class*="_tone_teal"]) { background: var(--tint-teal); border-color: rgba(15, 118, 110, .22) !important; }
[data-testid="stVerticalBlockBorderWrapper"]:has([class*="_tone_coral"]) { background: var(--tint-coral); border-color: rgba(255, 127, 80, .30) !important; }
[data-testid="stVerticalBlockBorderWrapper"]:has([class*="_tone_sand"]) { background: var(--tint-sand); border-color: rgba(212, 163, 115, .40) !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] { padding: 0; }
[data-testid="stPlotlyChart"] { overflow: hidden; max-width: 100%; }

/* High-Contrast Inputs & Select Boxes */
div[data-baseweb="select"] > div { background: #fff !important; border: 1px solid #CBD5E1 !important; border-radius: 10px !important; }
div[data-baseweb="select"] * { color: #0F172A !important; font-weight: 500 !important; }
div[data-baseweb="popover"] li, div[data-baseweb="popover"] li * { color: #0F172A !important; }
span[data-baseweb="tag"], span[data-baseweb="tag"] * { background: #0F766E !important; color: #fff !important; }
div[data-testid="stWidgetLabel"] p { font-weight: 600; color: #334155; font-size: .85rem; }
div[role="radiogroup"] label p { color: #0F172A; font-weight: 600; }

/* Section Titles */
.section-title { font-size: 1.35rem; font-weight: 700; color: var(--ink); margin: 6px 0 2px; }
.section-sub { font-size: .88rem; color: var(--muted); margin-bottom: 10px; }

/* KPI Grid */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 4px 0 18px; }
.kpi-card { 
    background: var(--tint-teal); border: 1px solid rgba(15, 118, 110, .22); border-radius: 18px; 
    padding: 18px 20px; min-height: 128px; display: flex; flex-direction: column;
    justify-content: space-between; gap: 6px; box-sizing: border-box; overflow: hidden; position: relative; 
}
.kpi-card:nth-child(4n+2) { background: var(--tint-coral); border-color: rgba(255, 127, 80, .30); }
.kpi-card:nth-child(4n+3) { background: var(--tint-sand); border-color: rgba(212, 163, 115, .40); }
.kpi-card::after { content: ""; position: absolute; right: -18px; top: -18px; width: 70px; height: 70px; border-radius: 50%; background: rgba(255, 255, 255, .6); }
.kpi-title { color: var(--muted); font-size: .82rem; font-weight: 600; line-height: 1.3; overflow-wrap: anywhere; position: relative; z-index: 1; }
.kpi-value { color: var(--ink); font-size: 1.8rem; font-weight: 700; line-height: 1.15; overflow-wrap: anywhere; }
.kpi-value small { font-size: .88rem; font-weight: 500; color: var(--muted); }
.kpi-sub { display: inline-block; align-self: flex-start; font-size: .78rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; overflow-wrap: anywhere; }

/* Positive Growth Status Color Fix */
.kpi-sub.positive { color: #0F766E !important; background: rgba(255, 255, 255, .90); }
.kpi-sub.negative { color: #D9552B !important; background: rgba(255, 255, 255, .90); }
.kpi-sub.neutral { color: #7A5C2E !important; background: rgba(255, 255, 255, .90); }

.chart-source { 
    font-size: .74rem; color: var(--muted); background: rgba(255, 255, 255, .75); 
    padding: 5px 10px; border-radius: 8px; border-left: 3px solid var(--teal); 
    margin: 2px 0 6px; line-height: 1.4; overflow-wrap: anywhere; 
}

/* Strategic Recommendation Cards */
.smart-card { background: var(--tint-teal); border-radius: 16px; border-left: 5px solid var(--teal); padding: 14px 16px; margin-bottom: 14px; overflow: hidden; }
.smart-card.CRITICAL, .smart-card.WARNING { border-left-color: var(--coral); background: var(--tint-coral); }
.smart-card.SUCCESS { background: var(--tint-teal); } 
.smart-card.OPPORTUNITY { border-left-color: #D4A373; background: var(--tint-sand); }
.smart-head { font-weight: 700; font-size: .95rem; color: var(--ink); overflow-wrap: anywhere; }
.smart-metric { font-size: 1.7rem; font-weight: 800; color: var(--teal); line-height: 1.15; margin: 4px 0 6px; overflow-wrap: anywhere; }
.smart-card ul { margin: 0; padding-left: 18px; font-size: .84rem; color: #334155; line-height: 1.5; }
.smart-card ul b { color: var(--teal); }

/* Tourism Recommendation Cards */
.rec-card { background: var(--tint-sand); border: 1px solid rgba(212, 163, 115, .40); border-radius: 18px; overflow: hidden; }
.rec-img-container { position: relative; width: 100%; aspect-ratio: 16/10; overflow: hidden; background: var(--sand); }
.rec-img-container img.rec-img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center; display: block; }
.rec-badge { position: absolute; top: 12px; left: 12px; background: #FF7F50; color: #fff; font-weight: 700; font-size: .9rem; padding: 4px 14px; border-radius: 20px; }
.rec-body { padding: 16px 18px; overflow: hidden; }
.rec-title { color: #0F766E; font-size: 1.25rem; font-weight: 700; margin: 0 0 4px; overflow-wrap: anywhere; }
.rec-stat { background: #fff; border: 1px solid #EFE4CC; border-radius: 10px; padding: 8px 12px; margin: 8px 0 10px; display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
</style>
""", unsafe_allow_html=True)

# ============ DATA PIPELINE & COMPONENTS IMPORTS ============
from src.pipeline.data_loader import load_data, compute_tourism_dependency
from src.analytics.intelligence import (
    compute_opportunity_matrix, detect_anomalies,
    generate_smart_recommendations, perform_province_clustering
)

DEFAULT_CHART_SOURCES = {
    "monthly_trend_tourists": "กองเศรษฐกิจการท่องเที่ยวและกีฬา กระทรวงการท่องเที่ยวและกีฬา (MOTS) | Dataset: fact_tourism_monthly",
    "monthly_trend_revenue": "กองเศรษฐกิจการท่องเที่ยวและกีฬา กระทรวงการท่องเที่ยวและกีฬา (MOTS) | Dataset: fact_tourism_monthly",
    "visitor_share": "กองเศรษฐกิจการท่องเที่ยวและกีฬา กระทรวงการท่องเที่ยวและกีฬา (MOTS) & สำนักงานสถิติแห่งชาติ (NSO)",
    "top_provinces": "กระทรวงการท่องเที่ยวและกีฬา (MOTS) & การท่องเที่ยวแห่งประเทศไทย (TAT Data Portal)",
    "thailand_map": "กระทรวงการท่องเที่ยวและกีฬา (MOTS) & สำนักงานสถิติแห่งชาติ (NSO)",
    "seasonality": "กองเศรษฐกิจการท่องเที่ยวและกีฬา กระทรวงการท่องเที่ยวและกีฬา (MOTS) สถิติสะสมรายเดือน",
    "volume_vs_yield": "กระทรวงการท่องเที่ยวและกีฬา (MOTS) & สำนักงานสภาพัฒนาการเศรษฐกิจและสังคมแห่งชาติ (NESDC GPP)",
    "occupancy_rate": "การท่องเที่ยวแห่งประเทศไทย (TAT Data Catalog: สถิติจำนวนห้องพักและอัตราการเข้าพัก)",
    "dependency_table": "สำนักงานสภาพัฒนาการเศรษฐกิจและสังคมแห่งชาติ (NESDC Provincial GPP) & กระทรวงการท่องเที่ยวและกีฬา (MOTS)",
    "opportunity_matrix": "การคำนวณ Yield และ YoY Growth จากฐานข้อมูล MOTS & NESDC (Star Schema Engine)",
    "anomaly_detection": "สถิติผู้เยี่ยมเยือนรายเดือน MOTS (วิเคราะห์ด้วยแบบจำลอง Rolling Bollinger Bands ±2σ)",
    "clustering": "การจัดกลุ่ม 77 จังหวัดด้วยแบบจำลอง K-Means โดยประมวลผลข้อมูลร่วม MOTS, NESDC และ TAT"
}

import src.components.charts as charts_module
from src.components.charts import (
    create_monthly_trend_chart, create_top_provinces_chart, create_thailand_map, create_seasonality_chart,
    create_visitor_share_donut, create_volume_vs_yield_scatter, create_occupancy_bar_chart,
    create_opportunity_matrix_chart, create_anomaly_chart, create_cluster_profile_chart
)
from src.components.recommendations import get_top5_recommended_provinces

CHART_SOURCES = getattr(charts_module, "CHART_SOURCES", DEFAULT_CHART_SOURCES)

# ---------- HELPER FUNCTIONS ----------
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2B07\uFE0F\u200d]+\\s*")
def strip_emoji(t): 
    return EMOJI_RE.sub("", str(t or "")).strip()

def style_fig(fig, height=None):
    if height: 
        fig.update_layout(height=height)
    return fig

_TONES = ["teal", "sand", "coral"]
_card_n = [0]
def chart_card(fig, source_key, height=None):
    _card_n[0] += 1
    with st.container(border=True, key=f"card{_card_n[0]}_tone_{_TONES[(_card_n[0] - 1) % 3]}"):
        st.plotly_chart(style_fig(fig, height), use_container_width=True)
        src = CHART_SOURCES.get(source_key, DEFAULT_CHART_SOURCES.get(source_key, "MOTS"))
        st.markdown(f'<div class="chart-source"><b>Source:</b> {src}</div>', unsafe_allow_html=True)

def section(title, sub=None):
    clean_title = strip_emoji(title)
    st.markdown(f'<div class="section-title">{clean_title}</div>' + (f'<div class="section-sub">{sub}</div>' if sub else ""), unsafe_allow_html=True)

def kpi(title, value, unit="", sub="", cls="neutral"):
    clean_title = strip_emoji(title)
    u = f" <small>{unit}</small>" if unit else ""
    return f'<div class="kpi-card"><div class="kpi-title">{clean_title}</div><div class="kpi-value">{value}{u}</div><div class="kpi-sub {cls}">{sub}</div></div>'

def growth(g, label="YoY"):
    return ("positive" if g >= 0 else "negative"), f"{'▲' if g >= 0 else '▼'} {g:+.1f}% {label}"

def to_bullets(body, n=3, max_chars=95):
    text = re.sub(r"<[^>]+>", "", str(body))
    parts = [p.strip(" -•") for p in re.split(r"(?<=[.!?])\s+|\n+|•", text) if p.strip(" -•")]
    out = []
    for p in parts[:n]:
        p = (p[:max_chars].rstrip() + "…") if len(p) > max_chars else p
        out.append("<li>" + re.sub(r"(\d[\d,\.]*\s*%?)", r"<b>\1</b>", p) + "</li>")
    return "".join(out)

def rec_card(item):
    m = item["meta"]
    atts = "".join(f"<li>{a}</li>" for a in m["attractions"][:3])
    return f"""<div class="rec-card"><div class="rec-img-container">
      <img class="rec-img" src="{m['image_url']}" alt="{item['province_name_en']}" loading="lazy">
      <div class="rec-badge">#{item['rank']}</div></div>
      <div class="rec-body">
        <div class="rec-title">{item['province_name_th']} <span style="font-size:.9rem;font-weight:500;color:#64748B">({item['province_name_en']})</span></div>
        <div style="font-size:.8rem;color:#FF7F50;font-weight:600">{item['region']} • {m['travel_style']}</div>
        <div class="rec-stat">
          <div><div style="font-size:.72rem;color:#64748B">ผู้เยี่ยมเยือน</div><div style="font-weight:700;color:#0F766E">{item['total_tourists']:,.0f} คน</div></div>
          <div style="text-align:right"><div style="font-size:.72rem;color:#64748B">Yield/หัว</div><div style="font-weight:700;color:#FF7F50">{item['yield_baht']:,.0f} บาท</div></div></div>
        <div style="font-weight:700;color:#0F766E;font-size:.88rem">แหล่งแนะนำ</div>
        <ul style="font-size:.82rem;color:#334155;padding-left:18px;margin:2px 0 8px;line-height:1.4">{atts}</ul>
        <div style="font-size:.82rem;color:#475569;line-height:1.45">{m['why_visit']}</div>
        <div style="border-top:1px dashed #E2E8F0;margin-top:8px;padding-top:6px;font-size:.76rem;color:#64748B"><b>ช่วงแนะนำ:</b> {m['best_season']}<br>
        <span style="font-size:.7rem;color:#94A3B8">ภาพ: {m['image_credit']}</span></div>
      </div></div>"""

@st.cache_data
def get_cached_dataset():
    return load_data()

fact_tourism, fact_gpp, dim_province, dim_date = get_cached_dataset()

# ---------- SIDEBAR CONTROL PANEL ----------
PAGES = ["ภาพรวม", "เศรษฐกิจ", "อินไซต์", "แนะนำที่เที่ยว"]
month_en = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
month_th = ["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.","ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]
REGION_MAP = {
    "ทุกภูมิภาค": None, "กลาง": "ภาคกลาง", "เหนือ": "ภาคเหนือ", 
    "อีสาน": "ภาคตะวันออกเฉียงเหนือ", "ใต้": "ภาคใต้", 
    "ตะวันออก": "ภาคตะวันออก", "ตะวันตก": "ภาคตะวันตก"
}
VISITOR = {"ทั้งหมด": "total_tourists", "ไทย": "thai_tourists", "ต่างชาติ": "foreign_tourists"}

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-logo">TH</div><div><div class="brand-name">Tourism Intel</div>'
                '<div class="brand-sub">Thailand Dashboard</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-label">เมนูหลัก</div>', unsafe_allow_html=True)
    nav_page = st.radio("หน้า", PAGES, key="nav", label_visibility="collapsed")
    
    st.markdown('<div class="side-label">ตัวกรองข้อมูล</div>', unsafe_allow_html=True)
    years = sorted(fact_tourism["year"].unique())
    selected_year = st.selectbox("ปี (พ.ศ.)", years, index=len(years) - 1, format_func=lambda y: f"{y + 543}")
    month_range = st.slider("ช่วงเดือน", 1, 12, (1, 12))
    region_label = st.selectbox("ภูมิภาค", list(REGION_MAP))
    
    all_regions = sorted(dim_province["region"].unique())
    active_regions = all_regions if REGION_MAP[region_label] is None else [REGION_MAP[region_label]]
    prov_opts = sorted(dim_province[dim_province["region"].isin(active_regions)]["province_name_th"].unique())
    selected_provinces = st.multiselect("จังหวัด", prov_opts, default=[])
    visitor_label = st.radio("ประเภทนักท่องเที่ยว", list(VISITOR), horizontal=True)

trend_metric = VISITOR[visitor_label]
range_th = f"{month_th[month_range[0]-1]} – {month_th[month_range[1]-1]} {selected_year + 543}"

# ---------- TOP BAR & HERO BANNER ----------
st.markdown(f"""
<div class="topbar">
  <div class="search-pill">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
    <span>พ.ศ. {selected_year + 543} &nbsp;•&nbsp; {range_th} &nbsp;•&nbsp; {region_label} &nbsp;•&nbsp; {visitor_label}</span>
  </div>
  <div class="src-badge">MOTS • NESDC • TAT • NSO</div>
</div>

<div class="hero-banner">
  <h1>Thailand Tourism Intelligence</h1>
  <p>แดชบอร์ดวิเคราะห์การท่องเที่ยวไทย: เศรษฐกิจ พฤติกรรม ความพึ่งพาเชิงพื้นที่</p>
</div>
""", unsafe_allow_html=True)

# ---------- FILTER DATA LOGIC ----------
df_filtered = fact_tourism[(fact_tourism["year"] == selected_year) & 
                           (fact_tourism["month"] >= month_range[0]) &
                           (fact_tourism["month"] <= month_range[1]) & 
                           (fact_tourism["region"].isin(active_regions))].copy()

if selected_provinces:
    df_filtered = df_filtered[df_filtered["province_name_th"].isin(selected_provinces)]

region_df = fact_tourism[fact_tourism["region"].isin(active_regions)]

total_tourists = df_filtered["total_tourists"].sum()
thai_tourists = df_filtered["thai_tourists"].sum()
foreign_tourists = df_filtered["foreign_tourists"].sum()
total_revenue = df_filtered["total_revenue"].sum()
foreign_revenue = df_filtered["foreign_revenue"].sum()

avg_occ = df_filtered["occupancy_rate"].mean() if not df_filtered.empty else 0.0
avg_yield = (total_revenue * 1_000_000 / total_tourists) if total_tourists > 0 else 0.0
tourist_growth = df_filtered["tourists_yoy_growth"].mean() if not df_filtered.empty else 0.0
revenue_growth = df_filtered["revenue_yoy_growth"].mean() if not df_filtered.empty else 0.0

dep_df = compute_tourism_dependency(fact_tourism, fact_gpp, selected_year)
dep_subset = dep_df[dep_df["province_name_th"].isin(selected_provinces)] if selected_provinces else dep_df[dep_df["region"].isin(active_regions)]
top_dep_name = dep_subset.iloc[0]["province_name_th"] if not dep_subset.empty else "N/A"
top_dep_val = dep_subset.iloc[0]["dependency_ratio"] if not dep_subset.empty else 0.0

pct = lambda a, b: (a / b * 100) if b > 0 else 0

def apply_visitor_view(df):
    d = df.copy()
    if visitor_label == "ไทย":
        d["total_tourists"] = d["thai_tourists"]
        d["total_revenue"] = d["total_revenue"] - d["foreign_revenue"]
    elif visitor_label == "ต่างชาติ":
        d["total_tourists"] = d["foreign_tourists"]
        d["total_revenue"] = d["foreign_revenue"]
    return d

df_view, region_view = apply_visitor_view(df_filtered), apply_visitor_view(region_df)
view_tourists = df_view["total_tourists"].sum()
view_revenue = df_view["total_revenue"].sum()
view_yield = (view_revenue * 1_000_000 / view_tourists) if view_tourists > 0 else 0.0
rev_label = {"ทั้งหมด": "รายได้รวม", "ไทย": "รายได้ชาวไทย", "ต่างชาติ": "รายได้ต่างชาติ"}[visitor_label]

MAIN_W, SIDE_W = 2.1, 1

# ============ PAGE 1: OVERVIEW ============
if nav_page == "ภาพรวม":
    section("ภาพรวมนักท่องเที่ยว", f"ปี พ.ศ. {selected_year + 543} | {range_th} | {region_label}")
    gc, gt = growth(tourist_growth)
    st.markdown('<div class="kpi-grid">' +
        kpi("นักท่องเที่ยวรวม", f"{total_tourists:,.0f}", "คน", gt, gc) +
        kpi("ชาวไทย", f"{thai_tourists:,.0f}", "คน", f"สัดส่วน {pct(thai_tourists, total_tourists):.1f}%") +
        kpi("ต่างชาติ", f"{foreign_tourists:,.0f}", "คน", f"สัดส่วน {pct(foreign_tourists, total_tourists):.1f}%") +
        kpi("อัตราเข้าพักเฉลี่ย", f"{avg_occ:.1f}%", "", "ทั้งช่วงที่เลือก") + '</div>', unsafe_allow_html=True)
    
    main, side = st.columns([MAIN_W, SIDE_W], gap="medium")
    with main:
        chart_card(create_monthly_trend_chart(region_df, metric=trend_metric), "monthly_trend_tourists", 440)
        chart_card(create_top_provinces_chart(df_filtered, top_n=10, metric=trend_metric), "top_provinces", 460)
        chart_card(create_seasonality_chart(region_df), "seasonality", 420)
    with side:
        chart_card(create_visitor_share_donut(df_filtered), "visitor_share", 380)
        chart_card(create_thailand_map(df_view, metric="total_tourists"), "thailand_map", 560)

# ============ PAGE 2: ECONOMY ============
elif nav_page == "เศรษฐกิจ":
    section("รายได้และที่พัก", f"ปี พ.ศ. {selected_year + 543} | {range_th} | นักท่องเที่ยว: {visitor_label}")
    gc, gt = growth(revenue_growth)
    st.markdown('<div class="kpi-grid">' +
        kpi(rev_label, f"{view_revenue:,.1f}", "ล้านบาท", gt, gc) +
        kpi("รายได้ต่อหัว", f"{view_yield:,.0f}", "บาท/คน", "ค่าใช้จ่ายเฉลี่ย") +
        kpi("พึ่งพาท่องเที่ยวสูงสุด", f"{top_dep_val:.1f}%", "GPP", f"จังหวัด: {top_dep_name}") +
        kpi("รายได้ต่างชาติ", f"{foreign_revenue:,.1f}", "ล้านบาท", f"สัดส่วน {pct(foreign_revenue, total_revenue):.1f}%") + '</div>', unsafe_allow_html=True)
    
    main, side = st.columns([MAIN_W, SIDE_W], gap="medium")
    with main:
        chart_card(create_monthly_trend_chart(region_view, metric="total_revenue"), "monthly_trend_revenue", 440)
        chart_card(create_top_provinces_chart(df_view, top_n=10, metric="total_revenue"), "top_provinces", 460)
        section("ดัชนีพึ่งพา GPP", "ความพึ่งพา (%) = รายได้ท่องเที่ยว / GPP จังหวัด × 100")
        show = dep_subset[["province_name_th", "province_name_en", "region", "dependency_ratio", "total_revenue", "gpp_total",
                           "total_tourists", "yield_per_tourist", "foreign_share_pct"]].rename(columns={
            "province_name_th": "จังหวัด", "province_name_en": "Province", "region": "ภูมิภาค", "dependency_ratio": "พึ่งพา (% GPP)",
            "total_revenue": "รายได้ (MB)", "gpp_total": "GPP (MB)", "total_tourists": "นักท่องเที่ยว (คน)",
            "yield_per_tourist": "Yield (บาท)", "foreign_share_pct": "ต่างชาติ (%)"})
        with st.container(border=True, key="dep_table_tone_sand"):
            st.dataframe(show.head(15), use_container_width=True, hide_index=True)
            st.markdown(f'<div class="chart-source"><b>Source:</b> {DEFAULT_CHART_SOURCES["dependency_table"]}</div>', unsafe_allow_html=True)
    with side:
        chart_card(create_volume_vs_yield_scatter(df_view), "volume_vs_yield", 420)
        chart_card(create_occupancy_bar_chart(df_filtered), "occupancy_rate", 460)

# ============ PAGE 3: INSIGHTS ============
elif nav_page == "อินไซต์":
    main, side = st.columns([MAIN_W, SIDE_W], gap="medium")
    with main:
        section("เมทริกซ์ 4 ควอแดรนท์", "แกน X = Yield, แกน Y = โตรายได้ YoY, ขนาด = รายได้รวม, เส้นประ = ค่ามัธยฐาน")
        matrix_df, med_yield, med_growth = compute_opportunity_matrix(df_filtered)
        fig_m = create_opportunity_matrix_chart(matrix_df, med_yield, med_growth)
        chart_card(fig_m, "opportunity_matrix")

        section("ความผิดปกติ")
        a1, a2 = st.columns([4, 8])
        with a1:
            with st.container(border=True, key="anom_ctl_tone_coral"):
                target = st.selectbox("เป้าหมาย", ["ระดับประเทศ"] + sorted(dim_province["province_name_th"].tolist()))
                z_thresh = st.slider("เกณฑ์ Z-Score", 1.5, 3.0, 2.0, 0.1)
                code = None
                if target != "ระดับประเทศ":
                    row = dim_province[dim_province["province_name_th"] == target]
                    code = int(row.iloc[0]["province_code"]) if not row.empty else None
                anom_df = detect_anomalies(fact_tourism, province_code=code, z_threshold=z_thresh)
                n_anom = anom_df[anom_df["anomaly_status"] != "Normal (ปกติ)"].shape[0]
                st.markdown(f'<div class="kpi-title">สัญญาณผิดปกติ</div><div class="kpi-value" style="color:{"#FF7F50" if n_anom else "#0F766E"}">{n_anom} <small>เดือน</small></div>', unsafe_allow_html=True)
        with a2: 
            chart_card(create_anomaly_chart(anom_df), "anomaly_detection", 400)

        section("กลุ่มจังหวัด", "K-Means 5 ตัวแปร: ปริมาณ, Yield, พึ่งพา GPP, สัดส่วนต่างชาติ, อัตราเข้าพัก")
        clustered = perform_province_clustering(fact_tourism, fact_gpp, selected_year)
        fig_c = create_cluster_profile_chart(clustered)
        chart_card(fig_c, "clustering", 460)
        
    with side:
        section("ข้อเสนอแนะเชิงยุทธศาสตร์", "ตัวเลขสำคัญจากกฎวิเคราะห์อัตโนมัติ")
        insights = generate_smart_recommendations(df_filtered, fact_gpp, selected_year)
        for ins in insights:
            st.markdown(f"""<div class="smart-card {ins['severity']}">
              <div class="smart-head">{strip_emoji(ins['title'])}</div>
              <div class="smart-metric">{ins['metric']}</div><ul>{to_bullets(ins['body'])}</ul></div>""", unsafe_allow_html=True)

# ============ PAGE 4: TRAVEL RECOMMENDATIONS ============
else:
    section("จุดหมายยอดนิยม Top 5", "จัดอันดับจากจำนวนผู้เยี่ยมเยือนจริง (MOTS) พร้อมแหล่งท่องเที่ยวและช่วงเวลาที่เหมาะสม")
    top5 = get_top5_recommended_provinces(df_filtered)
    if not top5:
        st.warning("ไม่พบข้อมูลตามตัวกรอง โปรดปรับภูมิภาคหรือช่วงเวลา")
    else:
        for start, n in ((0, 3), (3, 2)):
            chunk = top5[start:start + n]
            if chunk:
                for col, item in zip(st.columns(n), chunk):
                    with col: 
                        st.markdown(rec_card(item), unsafe_allow_html=True)
        st.markdown('<div class="chart-source"><b>Source:</b> สถิติผู้เยี่ยมเยือนรายจังหวัด MOTS ร่วมกับ TAT</div>', unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("---")
fc1, fc2, fc3 = st.columns([6, 3, 3])
fc1.caption("Thailand Tourism Intelligence Dashboard | Open Data: MOTS • NESDC • TAT • NSO")
fc2.download_button(
    "ดาวน์โหลดข้อมูล (CSV)", 
    df_filtered.to_csv(index=False).encode("utf-8-sig"),
    f"tourism_data_{selected_year}.csv", 
    "text/csv", 
    use_container_width=True
)
fc3.download_button(
    "ดาวน์โหลดดัชนี GPP (CSV)", 
    dep_subset.to_csv(index=False).encode("utf-8-sig"),
    f"tourism_dependency_{selected_year}.csv", 
    "text/csv", 
    use_container_width=True
)