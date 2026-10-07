"""
Thailand Tourism Intelligence Dashboard - Streamlit entry point.
Z-pattern layout: (1) top-left brand -> top-right sources/nav, (2) global filter bar,
(3) diagonal: KPI strip -> hero chart, (4) bottom row left -> right: supporting charts -> insight/CTA.
Design: Teal #0F766E, Coral #FF7F50, Sand #F5E6CA, IBM Plex Sans Thai.
"""
import re
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Thailand Tourism Intelligence Dashboard", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"], [class*="st-"] { font-family:'IBM Plex Sans Thai','Noto Sans Thai',sans-serif !important; }
.block-container { padding:1.2rem 2rem 3rem; max-width:100%; overflow-x:hidden; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }

/* Banner: light overlay so the photo keeps its natural colour */
.main-header { background:linear-gradient(135deg, rgba(15,118,110,.30) 0%, rgba(15,23,42,.30) 100%),
  url('https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
  padding:26px 34px; border-radius:16px; margin-bottom:14px; border:1px solid rgba(255,255,255,.15); }
.main-header h1 { color:#fff !important; font-size:2rem; font-weight:700; margin:0; text-shadow:0 2px 6px rgba(0,0,0,.55); }
.main-header p { color:#fff !important; font-size:.98rem; margin:4px 0 0; text-shadow:0 1px 4px rgba(0,0,0,.55); }
.src-badge { background:rgba(15,23,42,.55); border:1px solid rgba(255,255,255,.3); padding:8px 16px; border-radius:10px; color:#fff; font-weight:600; font-size:.85rem; }

/* Cards: every chart/filter block is a bounded container */
[data-testid="stVerticalBlockBorderWrapper"] { background:#fff; border:1px solid #E2E8F0 !important; border-radius:14px !important;
  box-shadow:0 2px 8px rgba(0,0,0,.04); padding:6px 10px 4px; overflow:hidden !important; }
[data-testid="stPlotlyChart"] { overflow:hidden; max-width:100%; }

/* Select boxes: readable dark text on white */
div[data-baseweb="select"] > div { background:#fff !important; border:1px solid #CBD5E1 !important; border-radius:8px !important; }
div[data-baseweb="select"] * { color:#0F172A !important; }
div[data-baseweb="popover"] li, div[data-baseweb="popover"] li * { color:#0F172A !important; }
span[data-baseweb="tag"], span[data-baseweb="tag"] * { background:#0F766E !important; color:#fff !important; }
div[data-testid="stWidgetLabel"] p { font-weight:600; color:#334155; font-size:.85rem; }
div[role="radiogroup"] label p { color:#0F172A !important; font-weight:600; }

/* Section headers: bold, larger, keyword-only */
.section-title { font-size:1.6rem; font-weight:700; color:#0F172A; margin:18px 0 2px; }
.section-sub { font-size:.9rem; color:#64748B; margin-bottom:10px; }

/* KPI */
.kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:16px; margin:8px 0 16px; }
.kpi-card { background:#fff; border:1px solid #E2E8F0; border-top:4px solid #0F766E; border-radius:12px; padding:16px 18px;
  min-height:130px; display:flex; flex-direction:column; justify-content:space-between; box-sizing:border-box; overflow:hidden; }
.kpi-title { color:#475569; font-size:.82rem; font-weight:700; line-height:1.3; overflow-wrap:anywhere; }
.kpi-value { color:#0F766E; font-size:1.55rem; font-weight:700; line-height:1.2; overflow-wrap:anywhere; }
.kpi-value small { font-size:.9rem; font-weight:500; }
.kpi-sub { font-size:.85rem; font-weight:700; overflow-wrap:anywhere; }
.kpi-sub.positive { color:#16A34A; } .kpi-sub.negative { color:#DC2626; } .kpi-sub.neutral { color:#64748B; }

.chart-source { font-size:.76rem; color:#64748B; background:#FAF8F5; padding:5px 10px; border-radius:6px;
  border-left:3px solid #0F766E; margin:2px 0 6px; line-height:1.4; overflow-wrap:anywhere; }

/* Strategic recommendation cards */
.smart-card { background:#fff; border:1px solid #E2E8F0; border-left:5px solid #0F766E; border-radius:12px; padding:14px 16px;
  margin-bottom:12px; overflow:hidden; }
.smart-card.CRITICAL, .smart-card.WARNING { border-left-color:#FF7F50; background:#FFF7F3; }
.smart-card.SUCCESS { background:#F0FDF4; } .smart-card.OPPORTUNITY { border-left-color:#D97706; background:#FFFBEB; }
.smart-head { font-weight:700; font-size:.95rem; color:#0F172A; overflow-wrap:anywhere; }
.smart-metric { font-size:1.9rem; font-weight:800; color:#0F766E; line-height:1.15; margin:4px 0 6px; overflow-wrap:anywhere; }
.smart-card ul { margin:0; padding-left:18px; font-size:.86rem; color:#334155; line-height:1.5; }
.smart-card ul b { color:#0F766E; }

/* Travel cards: full-frame image */
.rec-card { background:#fff; border:1px solid #E2E8F0; border-radius:14px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,.05); }
.rec-img-container { position:relative; width:100%; aspect-ratio:16/10; overflow:hidden; background:#E2E8F0; }
.rec-img-container img.rec-img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center; display:block; }
.rec-badge { position:absolute; top:12px; left:12px; background:#FF7F50; color:#fff; font-weight:700; font-size:.9rem; padding:4px 14px; border-radius:20px; }
.rec-body { padding:16px 18px; overflow:hidden; }
.rec-title { color:#0F766E; font-size:1.25rem; font-weight:700; margin:0 0 4px; overflow-wrap:anywhere; }
.rec-stat { background:#FAF8F5; border:1px solid #E2E8F0; border-radius:8px; padding:8px 12px; margin:8px 0 10px; display:flex; justify-content:space-between; gap:8px; flex-wrap:wrap; }
</style>
""", unsafe_allow_html=True)

from src.pipeline.data_loader import load_data, compute_tourism_dependency
from src.analytics.intelligence import (compute_opportunity_matrix, detect_anomalies,
                                         generate_smart_recommendations, perform_province_clustering)
# Robust Source Catalog fallback
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
    create_opportunity_matrix_chart, create_anomaly_chart, create_cluster_scatter, create_cluster_profile_chart)
from src.components.recommendations import get_top5_recommended_provinces
CHART_SOURCES = getattr(charts_module, "CHART_SOURCES", DEFAULT_CHART_SOURCES)

# ---------- helpers ----------
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2B07\uFE0F\u200d]+\\s*")
def strip_emoji(t): return EMOJI_RE.sub("", str(t or "")).strip()

def style_fig(fig, height=None):
    """Title, legend and margins are set in charts.py (_finalize); only apply the card height here."""
    if height: fig.update_layout(height=height)
    return fig

def chart_card(fig, source_key, height=None):
    with st.container(border=True):
        st.plotly_chart(style_fig(fig, height), use_container_width=True)
        src = CHART_SOURCES.get(source_key, DEFAULT_CHART_SOURCES.get(source_key, "MOTS"))
        st.markdown(f'<div class="chart-source"><b>Source:</b> {src}</div>', unsafe_allow_html=True)

def section(title, sub=None):
    st.markdown(f'<div class="section-title">{title}</div>' + (f'<div class="section-sub">{sub}</div>' if sub else ""), unsafe_allow_html=True)

def kpi(title, value, unit="", sub="", cls="neutral"):
    u = f" <small>{unit}</small>" if unit else ""
    return f'<div class="kpi-card"><div class="kpi-title">{title}</div><div class="kpi-value">{value}{u}</div><div class="kpi-sub {cls}">{sub}</div></div>'

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

# ---------- Z row 1: top-left brand -> top-right sources ----------
st.markdown("""
<div class="main-header"><div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px">
  <div><h1>Thailand Tourism Intelligence</h1><p>แดชบอร์ดวิเคราะห์การท่องเที่ยวไทย: เศรษฐกิจ พฤติกรรม ความพึ่งพาเชิงพื้นที่</p></div>
  <div class="src-badge">MOTS • NESDC • TAT • NSO</div></div></div>
""", unsafe_allow_html=True)

# ---------- Global top filter bar (replaces sidebar) ----------
PAGES = ["ภาพรวม", "เศรษฐกิจ", "อินไซต์", "แนะนำที่เที่ยว"]
month_en = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
month_th = ["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.","ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]
REGION_MAP = {"ทุกภูมิภาค": None, "กลาง": "ภาคกลาง", "เหนือ": "ภาคเหนือ", "อีสาน": "ภาคตะวันออกเฉียงเหนือ",
              "ใต้": "ภาคใต้", "ตะวันออก": "ภาคตะวันออก", "ตะวันตก": "ภาคตะวันตก"}
VISITOR = {"ทั้งหมด": "total_tourists", "ไทย": "thai_tourists", "ต่างชาติ": "foreign_tourists"}

with st.container(border=True):
    nav_page = st.radio("หน้า", PAGES, horizontal=True, label_visibility="collapsed")
    f1, f2, f3, f4, f5 = st.columns([1.1, 1.6, 1.3, 2.2, 1.8])
    years = sorted(fact_tourism["year"].unique())
    selected_year = f1.selectbox("ปี (พ.ศ.)", years, index=len(years) - 1, format_func=lambda y: f"{y + 543}")
    month_range = f2.slider("ช่วงเดือน", 1, 12, (1, 12))
    region_label = f3.selectbox("ภูมิภาค", list(REGION_MAP))
    all_regions = sorted(dim_province["region"].unique())
    active_regions = all_regions if REGION_MAP[region_label] is None else [REGION_MAP[region_label]]
    prov_opts = sorted(dim_province[dim_province["region"].isin(active_regions)]["province_name_th"].unique())
    selected_provinces = f4.multiselect("จังหวัด", prov_opts, default=[])
    visitor_label = f5.radio("นักท่องเที่ยว", list(VISITOR), horizontal=True)
trend_metric = VISITOR[visitor_label]
range_th = f"{month_th[month_range[0]-1]} – {month_th[month_range[1]-1]} {selected_year + 543}"

# ---------- filter logic ----------
df_filtered = fact_tourism[(fact_tourism["year"] == selected_year) & (fact_tourism["month"] >= month_range[0]) &
                           (fact_tourism["month"] <= month_range[1]) & (fact_tourism["region"].isin(active_regions))].copy()
if selected_provinces:
    df_filtered = df_filtered[df_filtered["province_name_th"].isin(selected_provinces)]
region_df = fact_tourism[fact_tourism["region"].isin(active_regions)]

total_tourists = df_filtered["total_tourists"].sum(); thai_tourists = df_filtered["thai_tourists"].sum()
foreign_tourists = df_filtered["foreign_tourists"].sum(); total_revenue = df_filtered["total_revenue"].sum()
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

# ============ PAGE 1: OVERVIEW ============
if nav_page == "ภาพรวม":
    section("ภาพรวมนักท่องเที่ยว", f"ปี พ.ศ. {selected_year + 543} | {range_th} | {region_label}")
    gc, gt = growth(tourist_growth)
    st.markdown('<div class="kpi-grid">' +
        kpi("นักท่องเที่ยวรวม", f"{total_tourists:,.0f}", "คน", gt, gc) +
        kpi("ชาวไทย", f"{thai_tourists:,.0f}", "คน", f"สัดส่วน {pct(thai_tourists, total_tourists):.1f}%") +
        kpi("ต่างชาติ", f"{foreign_tourists:,.0f}", "คน", f"สัดส่วน {pct(foreign_tourists, total_tourists):.1f}%") +
        kpi("อัตราเข้าพักเฉลี่ย", f"{avg_occ:.1f}%", "", "ทั้งช่วงที่เลือก") + '</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([7, 3])                      # hero (diagonal start) -> share
    with c1: chart_card(create_monthly_trend_chart(region_df, metric=trend_metric), "monthly_trend_tourists", 420)
    with c2: chart_card(create_visitor_share_donut(df_filtered), "visitor_share", 420)
    c3, c4 = st.columns(2)                           # bottom row: ranking (left) -> map (right)
    with c3: chart_card(create_top_provinces_chart(df_filtered, top_n=10, metric=trend_metric), "top_provinces", 460)
    with c4: chart_card(create_thailand_map(df_filtered, metric="total_tourists"), "thailand_map", 460)
    section("ฤดูกาลท่องเที่ยว")
    chart_card(create_seasonality_chart(region_df), "seasonality", 420)

# ============ PAGE 2: ECONOMY ============
elif nav_page == "เศรษฐกิจ":
    section("รายได้และที่พัก", f"ปี พ.ศ. {selected_year + 543} | {range_th}")
    gc, gt = growth(revenue_growth)
    st.markdown('<div class="kpi-grid">' +
        kpi("รายได้รวม", f"{total_revenue:,.1f}", "ล้านบาท", gt, gc) +
        kpi("รายได้ต่อหัว", f"{avg_yield:,.0f}", "บาท/คน", "ค่าใช้จ่ายเฉลี่ย") +
        kpi("พึ่งพาท่องเที่ยวสูงสุด", f"{top_dep_val:.1f}%", "GPP", f"จังหวัด: {top_dep_name}") +
        kpi("รายได้ต่างชาติ", f"{foreign_revenue:,.1f}", "ล้านบาท", f"สัดส่วน {pct(foreign_revenue, total_revenue):.1f}%") + '</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([6, 4])
    with c1: chart_card(create_monthly_trend_chart(region_df, metric="total_revenue"), "monthly_trend_revenue", 420)
    with c2: chart_card(create_volume_vs_yield_scatter(df_filtered), "volume_vs_yield", 420)
    c3, c4 = st.columns(2)
    with c3: chart_card(create_occupancy_bar_chart(df_filtered), "occupancy_rate", 440)
    with c4: chart_card(create_top_provinces_chart(df_filtered, top_n=10, metric="total_revenue"), "top_provinces", 440)
    section("ดัชนีพึ่งพา GPP", "ความพึ่งพา (%) = รายได้ท่องเที่ยว / GPP จังหวัด × 100")
    show = dep_subset[["province_name_th", "province_name_en", "region", "dependency_ratio", "total_revenue", "gpp_total",
                       "total_tourists", "yield_per_tourist", "foreign_share_pct"]].rename(columns={
        "province_name_th": "จังหวัด", "province_name_en": "Province", "region": "ภูมิภาค", "dependency_ratio": "พึ่งพา (% GPP)",
        "total_revenue": "รายได้ (MB)", "gpp_total": "GPP (MB)", "total_tourists": "นักท่องเที่ยว (คน)",
        "yield_per_tourist": "Yield (บาท)", "foreign_share_pct": "ต่างชาติ (%)"})
    with st.container(border=True):
        st.dataframe(show.head(15), use_container_width=True, hide_index=True)
        st.markdown(f'<div class="chart-source"><b>Source:</b> {DEFAULT_CHART_SOURCES["dependency_table"]}</div>', unsafe_allow_html=True)

# ============ PAGE 3: INSIGHTS ============
elif nav_page == "อินไซต์":
    section("ข้อเสนอแนะเชิงยุทธศาสตร์", "ตัวเลขสำคัญจากกฎวิเคราะห์อัตโนมัติ")
    insights = generate_smart_recommendations(df_filtered, fact_gpp, selected_year)
    cols = st.columns(min(3, max(1, len(insights))))
    for i, ins in enumerate(insights):
        with cols[i % len(cols)]:
            st.markdown(f"""<div class="smart-card {ins['severity']}">
              <div class="smart-head">{strip_emoji(ins['title'])}</div>
              <div class="smart-metric">{ins['metric']}</div><ul>{to_bullets(ins['body'])}</ul></div>""", unsafe_allow_html=True)

    section("เมทริกซ์ 4 ควอแดรนท์", "แกน X = Yield, แกน Y = โตรายได้ YoY, ขนาด = รายได้รวม, เส้นประ = ค่ามัธยฐาน")
    matrix_df, med_yield, med_growth = compute_opportunity_matrix(df_filtered)
    fig_m = create_opportunity_matrix_chart(matrix_df, med_yield, med_growth)
    chart_card(fig_m, "opportunity_matrix")

    section("ความผิดปกติ")
    a1, a2 = st.columns([4, 8])
    with a1:
        with st.container(border=True):
            target = st.selectbox("เป้าหมาย", ["ระดับประเทศ"] + sorted(dim_province["province_name_th"].tolist()))
            z_thresh = st.slider("เกณฑ์ Z-Score", 1.5, 3.0, 2.0, 0.1)
            code = None
            if target != "ระดับประเทศ":
                row = dim_province[dim_province["province_name_th"] == target]
                code = int(row.iloc[0]["province_code"]) if not row.empty else None
            anom_df = detect_anomalies(fact_tourism, province_code=code, z_threshold=z_thresh)
            n_anom = anom_df[anom_df["anomaly_status"] != "Normal (ปกติ)"].shape[0]
            st.markdown(f'<div class="kpi-title">สัญญาณผิดปกติ</div><div class="kpi-value" style="color:{"#DC2626" if n_anom else "#16A34A"}">{n_anom} <small>เดือน</small></div>', unsafe_allow_html=True)
    with a2: chart_card(create_anomaly_chart(anom_df), "anomaly_detection", 400)

    section("กลุ่มจังหวัด", "K-Means 5 ตัวแปร: ปริมาณ, Yield, พึ่งพา GPP, สัดส่วนต่างชาติ, อัตราเข้าพัก")
    clustered = perform_province_clustering(fact_tourism, fact_gpp, selected_year)
    fig_c = create_cluster_profile_chart(clustered)
    chart_card(fig_c, "clustering", 460)

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
                    with col: st.markdown(rec_card(item), unsafe_allow_html=True)
        st.markdown('<div class="chart-source"><b>Source:</b> สถิติผู้เยี่ยมเยือนรายจังหวัด MOTS ร่วมกับ TAT</div>', unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("---")
fc1, fc2, fc3 = st.columns([6, 3, 3])
fc1.caption("Thailand Tourism Intelligence Dashboard | Open Data: MOTS • NESDC • TAT • NSO")
fc2.download_button("ดาวน์โหลดข้อมูล (CSV)", df_filtered.to_csv(index=False).encode("utf-8-sig"),
                    f"tourism_data_{selected_year}.csv", "text/csv", use_container_width=True)
fc3.download_button("ดาวน์โหลดดัชนี GPP (CSV)", dep_subset.to_csv(index=False).encode("utf-8-sig"),
                    f"tourism_dependency_{selected_year}.csv", "text/csv", use_container_width=True)