"""
Visualization Components for Thailand Tourism Intelligence Dashboard
Refactored for Professional Data Visualization Standards:
- Official Palette: Primary Teal (#0F766E), Secondary Coral (#FF7F50), Sand accents (#F5E6CA)
- Font: IBM Plex Sans Thai / Noto Sans Thai
- Complete Chart Elements: Titles, Explicit X & Y axes with units, Legends, Tooltips
- Responsive & Overflow-Safe
"""

from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Official Brand Color Palette
COLOR_TEAL = "#0F766E"      # Primary Teal (Main data, important lines)
COLOR_CORAL = "#FF7F50"     # Secondary Coral (Highlights, comparisons, warnings)
COLOR_SAND = "#F5E6CA"      # Sand background/accent
COLOR_SAND_DARK = "#D4A373" # Deep sand / warm amber
COLOR_DARK = "#1E293B"      # Deep slate for text
COLOR_MUTED = "#64748B"     # Muted text
COLOR_BG_LIGHT = "#FAF8F5"  # Subtle sand warm white

CHART_THEME = {
    "font": {
        "family": "'IBM Plex Sans Thai', 'Noto Sans Thai', -apple-system, sans-serif",
        "size": 12,
        "color": COLOR_DARK
    },
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
}

# Source Catalog for every chart
CHART_SOURCES: Dict[str, str] = {
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


import functools

def _finalize(fig: go.Figure, title: str, bottom: int = 96) -> go.Figure:
    """Uniform, overlap-safe layout: short bold title (top-left), legend BELOW the plot, fixed margins."""
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0, xanchor="left", y=0.98, yanchor="top",
                   font=dict(size=20, color=COLOR_DARK)),
        margin=dict(l=24, r=24, t=72, b=bottom),
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="left", x=0,
                    title=dict(text=""), font=dict(size=11)),
        autosize=True,
    )
    fig.update_xaxes(automargin=True, title_standoff=10)
    fig.update_yaxes(automargin=True, title_standoff=10)
    return fig

def _chart(title: str, bottom: int = 96):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return _finalize(fn(*args, **kwargs), title, bottom)
        return wrapper
    return deco

@_chart("แนวโน้มรายเดือน", 96)
def create_monthly_trend_chart(df: pd.DataFrame, metric: str = "total_tourists") -> go.Figure:
    """
    Monthly Trend Chart showing YoY multi-year comparison line chart.
    Uses Primary Teal (#0F766E) for current year and Coral (#FF7F50) for highlight.
    """
    label_map = {
        "total_tourists": ("จำนวนนักท่องเที่ยวรวม", "คน"),
        "total_revenue": ("รายได้จากการท่องเที่ยวรวม", "ล้านบาท"),
        "thai_tourists": ("นักท่องเที่ยวชาวไทย (Domestic)", "คน"),
        "foreign_tourists": ("นักท่องเที่ยวต่างชาติ (International)", "คน"),
    }
    metric_name, unit = label_map.get(metric, (metric, ""))

    monthly = df.groupby(["year", "month"]).agg({metric: "sum"}).reset_index()
    month_names_th = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
                      "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    monthly["month_label"] = monthly["month"].apply(lambda m: month_names_th[m - 1])

    fig = go.Figure()
    years = sorted(monthly["year"].unique())

    # Curate palette: latest year = Primary Teal, previous year = Secondary Coral, others = Muted
    for i, yr in enumerate(years):
        sub = monthly[monthly["year"] == yr].sort_values("month")
        is_latest = (i == len(years) - 1)
        is_prev = (i == len(years) - 2)

        if is_latest:
            line_color = COLOR_TEAL
            line_width = 3.5
            dash_style = "solid"
            marker_size = 7
        elif is_prev:
            line_color = COLOR_CORAL
            line_width = 2.5
            dash_style = "solid"
            marker_size = 6
        elif yr in [2020, 2021]:
            line_color = "#94A3B8"
            line_width = 1.6
            dash_style = "dot"
            marker_size = 4
        else:
            line_color = "#CBD5E1"
            line_width = 1.8
            dash_style = "solid"
            marker_size = 5

        fig.add_trace(go.Scatter(
            x=sub["month_label"],
            y=sub[metric],
            name=f"ปี {yr + 543} ({yr})",
            mode="lines+markers",
            line=dict(color=line_color, width=line_width, dash=dash_style),
            marker=dict(size=marker_size, color=line_color),
            hovertemplate=f"<b>ปี {yr + 543} - %{{x}}</b><br>{metric_name}: %{{y:,.0f}} {unit}<extra></extra>"
        ))

    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text=f"<b>แนวโน้มรายเดือนเปรียบเทียบย้อนหลัง (Monthly YoY Trend)</b><br><span style='font-size:12px; color:#64748B;'>{metric_name} (หน่วย: {unit})</span>",
            font=dict(size=15)
        ),
        xaxis=dict(title="<b>เดือน (Month)</b>", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title=f"<b>{metric_name} ({unit})</b>", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    return fig

@_chart("จังหวัดอันดับสูงสุด", 60)
def create_top_provinces_chart(df: pd.DataFrame, top_n: int = 10, metric: str = "total_tourists") -> go.Figure:
    """
    Top Provinces Ranking Horizontal Bar Chart.
    Top 1 highlighted in Coral (#FF7F50), others in Teal (#0F766E).
    """
    metric_map = {
        "total_tourists": ("จำนวนนักท่องเที่ยวรวม", "คน"),
        "total_revenue": ("รายได้จากการท่องเที่ยวรวม", "ล้านบาท"),
        "foreign_tourists": ("นักท่องเที่ยวชาวต่างชาติ", "คน"),
        "thai_tourists": ("นักท่องเที่ยวชาวไทย", "คน"),
        "revenue_per_tourist": ("รายได้เฉลี่ยต่อหัว (Yield)", "บาท/คน")
    }
    metric_name, unit = metric_map.get(metric, (metric, ""))

    agg = df.groupby(["province_code", "province_name_th", "province_name_en", "region"]).agg({
        metric: "mean" if metric == "revenue_per_tourist" else "sum"
    }).reset_index()

    top_df = agg.sort_values(by=metric, ascending=True).tail(top_n).reset_index(drop=True)
    top_df["display_name"] = top_df["province_name_th"] + " (" + top_df["province_name_en"] + ")"

    # Bar color: Top bar in Coral, remaining in Teal gradient
    colors = [COLOR_CORAL if i == len(top_df) - 1 else COLOR_TEAL for i in range(len(top_df))]

    fig = go.Figure(go.Bar(
        x=top_df[metric],
        y=top_df["display_name"],
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.4)", width=1)),
        text=top_df[metric].apply(lambda x: f"{x:,.0f} {unit}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>" + f"{metric_name}: " + "%{x:,.0f} " + unit + "<br>ภูมิภาค: %{customdata}<extra></extra>",
        customdata=top_df["region"]
    ))

    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text=f"<b>10 อันดับจังหวัดสูงสุด (Top {top_n} Provinces Ranking)</b><br><span style='font-size:12px; color:#64748B;'>{metric_name} (หน่วย: {unit})</span>",
            font=dict(size=15)
        ),
        xaxis=dict(title=f"<b>{metric_name} ({unit})</b>", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="<b>จังหวัด (Province)</b>"),
        margin=dict(l=40, r=40, t=55, b=40)
    )
    return fig

@_chart("แผนที่รายจังหวัด", 80)
def create_thailand_map(df: pd.DataFrame, metric: str = "total_tourists") -> go.Figure:
    """
    Interactive Geospatial Map of Thailand's 77 provinces with proportional bubble markers.
    """
    metric_map = {
        "total_tourists": ("จำนวนนักท่องเที่ยว", "คน"),
        "total_revenue": ("รายได้จากการท่องเที่ยว", "ล้านบาท")
    }
    metric_name, unit = metric_map.get(metric, (metric, ""))

    agg = df.groupby(["province_code", "province_name_th", "province_name_en", "region"]).agg({
        "total_tourists": "sum",
        "total_revenue": "sum",
        "foreign_tourists": "sum",
        "thai_tourists": "sum",
        "occupancy_rate": "mean"
    }).reset_index()

    from src.pipeline.schema import get_dim_province
    provinces_dim = get_dim_province()
    geo_df = pd.merge(agg, provinces_dim[["province_code", "lat", "lon"]], on="province_code")

    geo_df["yield_baht"] = ((geo_df["total_revenue"] * 1_000_000) / geo_df["total_tourists"].replace(0, 1)).round(0)
    geo_df["foreign_pct"] = ((geo_df["foreign_tourists"] / geo_df["total_tourists"].replace(0, 1)) * 100).round(1)

    hover_dict = {
        "lat": False,
        "lon": False,
        "province_name_en": True,
        "region": True,
        "total_tourists": ":,.0f คน",
        "total_revenue": ":,.1f MB",
        "yield_baht": ":,.0f บาท/คน",
        "foreign_pct": ":.1f%",
        "occupancy_rate": ":.1f%"
    }

    # Custom continuous color scale: Teal to Coral
    custom_colorscale = [
        [0.0, "#0F766E"],
        [0.35, "#14B8A6"],
        [0.7, "#F59E0B"],
        [1.0, "#FF7F50"]
    ]

    if hasattr(px, "scatter_map"):
        fig = px.scatter_map(
            geo_df,
            lat="lat",
            lon="lon",
            size=metric,
            color=metric,
            hover_name="province_name_th",
            hover_data=hover_dict,
            color_continuous_scale=custom_colorscale,
            size_max=32,
            zoom=4.9,
            center=dict(lat=13.2, lon=101.0),
            map_style="open-street-map",
            title=f"<b>แผนที่การกระจายตัวเชิงพื้นที่ 77 จังหวัด</b><br><span style='font-size:12px; color:#64748B;'>Geospatial Density: {metric_name} ({unit})</span>"
        )
    else:
        fig = px.scatter_mapbox(
            geo_df,
            lat="lat",
            lon="lon",
            size=metric,
            color=metric,
            hover_name="province_name_th",
            hover_data=hover_dict,
            color_continuous_scale=custom_colorscale,
            size_max=32,
            zoom=4.9,
            center=dict(lat=13.2, lon=101.0),
            mapbox_style="carto-positron",
            title=f"<b>แผนที่การกระจายตัวเชิงพื้นที่ 77 จังหวัด</b><br><span style='font-size:12px; color:#64748B;'>Geospatial Density: {metric_name} ({unit})</span>"
        )

    theme = dict(CHART_THEME)
    theme["margin"] = dict(l=0, r=0, t=45, b=0)
    fig.update_layout(
        **theme,
        coloraxis_colorbar=dict(
            title=dict(text=f"{metric_name} ({unit})", font=dict(size=11)),
            orientation="h",
            y=-0.08, yanchor="top", thickness=12, len=0.6
        )
    )
    return fig

@_chart("ฤดูกาลท่องเที่ยว", 96)
def create_seasonality_chart(df: pd.DataFrame) -> go.Figure:
    """
    Seasonality Chart analyzing Peak, Shoulder, and Low seasons.
    Colors: High Season = Coral (#FF7F50), Shoulder = Teal (#0F766E), Low = Sand (#D4A373).
    """
    monthly = df.groupby(["month", "year"]).agg({"total_tourists": "sum"}).reset_index()
    monthly_stats = monthly.groupby("month").agg(
        avg_tourists=("total_tourists", "mean"),
        min_tourists=("total_tourists", "min"),
        max_tourists=("total_tourists", "max")
    ).reset_index()

    month_names_th = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
                      "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    monthly_stats["month_label"] = monthly_stats["month"].apply(lambda m: month_names_th[m - 1])

    def get_season_badge(m):
        if m in [11, 12, 1, 2]:
            return "High Season (ช่วงไฮซีซั่น)"
        elif m in [3, 4, 7, 8]:
            return "Shoulder Season (ช่วงรอยต่อ)"
        return "Low Season / Green Season (ช่วงโลว์ซีซั่น)"

    monthly_stats["season_category"] = monthly_stats["month"].apply(get_season_badge)

    fig = px.bar(
        monthly_stats,
        x="month_label",
        y="avg_tourists",
        color="season_category",
        title="<b>การวิเคราะห์วงจรฤดูกาลท่องเที่ยวไทย (Seasonality Cycle)</b><br><span style='font-size:12px; color:#64748B;'>เปรียบเทียบ Peak Season vs. Low Season (หน่วย: คน)</span>",
        color_discrete_map={
            "High Season (ช่วงไฮซีซั่น)": COLOR_CORAL,
            "Shoulder Season (ช่วงรอยต่อ)": COLOR_TEAL,
            "Low Season / Green Season (ช่วงโลว์ซีซั่น)": COLOR_SAND_DARK
        },
        labels={
            "avg_tourists": "จำนวนนักท่องเที่ยวเฉลี่ย (คน)",
            "month_label": "เดือน (Month)",
            "season_category": "ฤดูกาล (Season)"
        }
    )

    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(title="<b>เดือน (Month)</b>", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="<b>จำนวนนักท่องเที่ยวเฉลี่ย (คน)</b>", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(title=dict(text="<b>ประเภทฤดูกาล</b>"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_traces(
        texttemplate="%{y:,.0f}",
        textposition="outside"
    )
    return fig

@_chart("สัดส่วนผู้เยี่ยมเยือน", 80)
def create_visitor_share_donut(df: pd.DataFrame) -> go.Figure:
    """
    Donut chart of Thai Domestic vs Foreign International share.
    Colors: Domestic = Teal (#0F766E), Foreign = Coral (#FF7F50).
    """
    total_thai = df["thai_tourists"].sum()
    total_foreign = df["foreign_tourists"].sum()
    grand_total = total_thai + total_foreign

    fig = go.Figure(data=[go.Pie(
        labels=["นักท่องเที่ยวชาวไทย (Domestic)", "นักท่องเที่ยวต่างชาติ (International)"],
        values=[total_thai, total_foreign],
        hole=.55,
        marker=dict(colors=[COLOR_TEAL, COLOR_CORAL], line=dict(color="#FFFFFF", width=2)),
        hovertemplate="<b>%{label}</b><br>จำนวน: %{value:,.0f} คน<br>สัดส่วน: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text="<b>สัดส่วนผู้เยี่ยมเยือน (Domestic vs. International)</b><br><span style='font-size:12px; color:#64748B;'>โครงสร้างนักท่องเที่ยวไทยเทียบต่างชาติ</span>",
            font=dict(size=14)
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        annotations=[dict(
            text=f"<b>รวม</b><br>{grand_total / 1_000_000:.1f}M คน",
            x=0.5, y=0.5, font_size=15, font_color=COLOR_DARK, showarrow=False
        )]
    )
    return fig

@_chart("ปริมาณ vs รายได้", 100)
def create_volume_vs_yield_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Visitors vs. Revenue (High Volume vs High Yield) Scatter Plot.
    """
    agg = df.groupby(["province_code", "province_name_th", "province_name_en", "region"]).agg({
        "total_tourists": "sum",
        "total_revenue": "sum",
        "occupancy_rate": "mean"
    }).reset_index()

    agg["yield_per_visitor"] = ((agg["total_revenue"] * 1_000_000) / agg["total_tourists"].replace(0, 1)).round(1)

    fig = px.scatter(
        agg,
        x="total_tourists",
        y="total_revenue",
        size="yield_per_visitor",
        color="region",
        hover_name="province_name_th",
        hover_data={
            "province_name_en": True,
            "region": True,
            "total_tourists": ":,.0f คน",
            "total_revenue": ":,.1f ล้านบาท",
            "yield_per_visitor": ":,.0f บาท/คน",
            "occupancy_rate": ":.1f%"
        },
        title="<b>ความสัมพันธ์ปริมาณ vs รายได้ (High Volume vs. High Yield)</b><br><span style='font-size:12px; color:#64748B;'>แกนลอการิทึม (Log Scale) | ขนาดวงกลม = รายได้เฉลี่ยต่อหัว (Yield)</span>",
        labels={
            "total_tourists": "จำนวนนักท่องเที่ยวรวม (คน)",
            "total_revenue": "รายได้รวมจากการท่องเที่ยว (ล้านบาท)",
            "region": "ภูมิภาค (Region)",
            "yield_per_visitor": "รายได้เฉลี่ยต่อหัว (บาท/คน)"
        },
        color_discrete_sequence=[COLOR_TEAL, COLOR_CORAL, "#14B8A6", COLOR_SAND_DARK, "#8B5CF6", "#3B82F6"]
    )

    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(title="<b>จำนวนนักท่องเที่ยวรวม (คน - Log Scale)</b>", showgrid=True, gridcolor="#F1F5F9", type="log"),
        yaxis=dict(title="<b>รายได้รวมจากการท่องเที่ยว (ล้านบาท - Log Scale)</b>", showgrid=True, gridcolor="#F1F5F9", type="log"),
        legend=dict(title=dict(text="<b>ภูมิภาค</b>"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

@_chart("อัตราเข้าพักรายภาค", 80)
def create_occupancy_bar_chart(df: pd.DataFrame) -> go.Figure:
    """
    Accommodation Occupancy Rate by Region vs National Benchmark.
    Bars: Primary Teal (#0F766E), Benchmark: Secondary Coral (#FF7F50) dashed line.
    """
    reg_occ = df.groupby("region").agg({"occupancy_rate": "mean"}).reset_index().sort_values("occupancy_rate", ascending=False)
    nat_benchmark = df["occupancy_rate"].mean()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=reg_occ["region"],
        y=reg_occ["occupancy_rate"],
        marker_color=COLOR_TEAL,
        name="อัตราเข้าพักเฉลี่ยของภูมิภาค (%)",
        text=reg_occ["occupancy_rate"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>อัตราเข้าพักเฉลี่ย: %{y:.1f}%<extra></extra>"
    ))

    # Add national benchmark horizontal line
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=len(reg_occ) - 0.5,
        y0=nat_benchmark,
        y1=nat_benchmark,
        line=dict(color=COLOR_CORAL, width=2.5, dash="dash")
    )
    fig.add_annotation(
        x=len(reg_occ) - 1,
        y=nat_benchmark + 3.0,
        text=f"เกณฑ์เฉลี่ยประเทศ: {nat_benchmark:.1f}%",
        showarrow=False,
        font=dict(color=COLOR_CORAL, size=12, family="'IBM Plex Sans Thai', sans-serif")
    )

    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text="<b>อัตราการเข้าพักแรมเฉลี่ยรายภาคเทียบเกณฑ์ประเทศ</b><br><span style='font-size:12px; color:#64748B;'>Average Occupancy Rate (AOR) เทียบเส้นเกณฑ์มาตรฐาน (%)</span>",
            font=dict(size=14)
        ),
        yaxis=dict(title="<b>อัตราเข้าพักเฉลี่ย (%)</b>", range=[0, 105], showgrid=True, gridcolor="#F1F5F9"),
        xaxis=dict(title="<b>ภูมิภาค (Region)</b>"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

@_chart("เมทริกซ์ 4 ควอแดรนท์", 110)
def create_opportunity_matrix_chart(matrix_df: pd.DataFrame, median_yield: float, median_growth: float) -> go.Figure:
    """Four-quadrant matrix: X = Yield (baht/visitor), Y = revenue YoY growth (%), size = total revenue."""
    short = {
        "Star": ("ดาวเด่น", COLOR_CORAL),
        "Mature": ("รายได้หลัก", COLOR_TEAL),
        "Hidden": ("เพชรเม็ดงาม", "#D97706"),
        "Repositioning": ("ต้องยกระดับ", "#94A3B8"),
    }
    def _key(q: str) -> str:
        return next((k for k in short if str(q).startswith(k)), "Repositioning")

    df = matrix_df.copy()
    df["quadrant_short"] = df["quadrant"].map(lambda q: short[_key(q)][0])
    cmap = {v[0]: v[1] for v in short.values()}

    fig = px.scatter(
        df, x="revenue_per_visitor", y="revenue_yoy_growth", color="quadrant_short",
        color_discrete_map=cmap, size="total_revenue", size_max=34, opacity=0.8,
        hover_name="province_name_th",
        hover_data={"province_name_en": True, "region": True, "quadrant_short": False,
                    "revenue_per_visitor": ":,.0f", "revenue_yoy_growth": ":.1f",
                    "total_tourists": ":,.0f", "total_revenue": ":,.1f"},
        labels={"revenue_per_visitor": "Yield (บาท/คน)", "revenue_yoy_growth": "การเติบโตรายได้ YoY (%)",
                "quadrant_short": "กลุ่ม"},
    )

    xmin, xmax = df["revenue_per_visitor"].min(), df["revenue_per_visitor"].max()
    ymin, ymax = df["revenue_yoy_growth"].min(), df["revenue_yoy_growth"].max()
    xpad, ypad = (xmax - xmin) * 0.08 or 1, (ymax - ymin) * 0.12 or 1
    x0, x1, y0, y1 = max(0, xmin - xpad), xmax + xpad, ymin - ypad, ymax + ypad

    # Quadrant shading (below data) split at the medians
    for (xa, xb, ya, yb, col) in [
        (median_yield, x1, median_growth, y1, "rgba(255,127,80,0.07)"),
        (x0, median_yield, median_growth, y1, "rgba(217,119,6,0.07)"),
        (median_yield, x1, y0, median_growth, "rgba(15,118,110,0.07)"),
        (x0, median_yield, y0, median_growth, "rgba(148,163,184,0.10)"),
    ]:
        fig.add_shape(type="rect", x0=xa, x1=xb, y0=ya, y1=yb, fillcolor=col, line_width=0, layer="below")
    fig.add_vline(x=median_yield, line_width=1.5, line_dash="dash", line_color="#94A3B8")
    fig.add_hline(y=median_growth, line_width=1.5, line_dash="dash", line_color="#94A3B8")

    # Quadrant captions pinned to the plot corners (paper coords: never collide with data scale)
    for (px_, py_, xa, ya, txt, col) in [
        (0.99, 0.99, "right", "top", "<b>ดาวเด่น</b>  Yield สูง / โตสูง", COLOR_CORAL),
        (0.01, 0.99, "left", "top", "<b>เพชรเม็ดงาม</b>  Yield ต่ำ / โตสูง", "#D97706"),
        (0.99, 0.01, "right", "bottom", "<b>รายได้หลัก</b>  Yield สูง / โตต่ำ", COLOR_TEAL),
        (0.01, 0.01, "left", "bottom", "<b>ต้องยกระดับ</b>  Yield ต่ำ / โตต่ำ", "#64748B"),
    ]:
        fig.add_annotation(xref="paper", yref="paper", x=px_, y=py_, xanchor=xa, yanchor=ya, text=txt,
                           showarrow=False, font=dict(color=col, size=12), bgcolor="rgba(255,255,255,0.75)",
                           borderpad=3)

    # Label only the 8 largest provinces so text never piles up
    top = df.nlargest(8, "total_revenue")
    fig.add_trace(go.Scatter(x=top["revenue_per_visitor"], y=top["revenue_yoy_growth"], mode="text",
                             text=top["province_name_th"], textposition="top center",
                             textfont=dict(size=11, color=COLOR_DARK), showlegend=False, hoverinfo="skip"))

    fig.update_layout(
        **CHART_THEME,
        height=620,
        xaxis=dict(title="<b>Yield (บาท/คน)</b>", range=[x0, x1], showgrid=True, gridcolor="#F1F5F9", zeroline=False,
                   tickformat=",.0f"),
        yaxis=dict(title="<b>การเติบโตรายได้ YoY (%)</b>", range=[y0, y1], showgrid=True, gridcolor="#F1F5F9",
                   zeroline=False, ticksuffix="%"),
    )
    return fig

@_chart("ความผิดปกติรายเดือน", 110)
def create_anomaly_chart(anomaly_df: pd.DataFrame) -> go.Figure:
    """
    Time Series Anomaly Detection with Bollinger Bands.
    Actual line = Primary Teal (#0F766E), Dips = Secondary Coral (#FF7F50).
    """
    fig = go.Figure()

    # Normal Band (±2 sigma)
    fig.add_trace(go.Scatter(
        x=anomaly_df["period_str"],
        y=anomaly_df["rolling_mean"] + (2 * anomaly_df["rolling_std"]),
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=anomaly_df["period_str"],
        y=np.maximum(0, anomaly_df["rolling_mean"] - (2 * anomaly_df["rolling_std"])),
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(15, 118, 110, 0.10)",
        name="ช่วงความแปรปรวนปกติ (Normal Band ±2σ)",
        hoverinfo="skip"
    ))

    # Rolling Mean
    fig.add_trace(go.Scatter(
        x=anomaly_df["period_str"],
        y=anomaly_df["rolling_mean"],
        mode="lines",
        line=dict(color="#94A3B8", dash="dash", width=1.8),
        name="ค่าเฉลี่ยเคลื่อนที่ (3-Mo Moving Avg)"
    ))

    # Actual line
    fig.add_trace(go.Scatter(
        x=anomaly_df["period_str"],
        y=anomaly_df["total_tourists"],
        mode="lines+markers",
        line=dict(color=COLOR_TEAL, width=2.8),
        name="จำนวนนักท่องเที่ยวจริง (คน)",
        hovertemplate="<b>%{x}</b><br>นักท่องเที่ยว: %{y:,.0f} คน<extra></extra>"
    ))

    # Highlight Anomalies
    spikes = anomaly_df[anomaly_df["anomaly_status"] == "Surge Spike (พุ่งขึ้นผิดปกติ)"]
    dips = anomaly_df[anomaly_df["anomaly_status"] == "Drop Dip (ลดลงผิดปกติ)"]

    if not spikes.empty:
        fig.add_trace(go.Scatter(
            x=spikes["period_str"],
            y=spikes["total_tourists"],
            mode="markers",
            marker=dict(color="#10B981", size=12, symbol="triangle-up", line=dict(color="white", width=2)),
            name="Anomaly Surge (พุ่งผิดปกติ)",
            hovertemplate="<b>%{x} [Spike]</b><br>ค่าจริง: %{y:,.0f} คน<br>เบี่ยงเบน: %{customdata:+.1f}%<extra></extra>",
            customdata=spikes["pct_deviation"]
        ))

    if not dips.empty:
        fig.add_trace(go.Scatter(
            x=dips["period_str"],
            y=dips["total_tourists"],
            mode="markers",
            marker=dict(color=COLOR_CORAL, size=12, symbol="triangle-down", line=dict(color="white", width=2)),
            name="Anomaly Drop (ลดผิดปกติ)",
            hovertemplate="<b>%{x} [Drop]</b><br>ค่าจริง: %{y:,.0f} คน<br>เบี่ยงเบน: %{customdata:+.1f}%<extra></extra>",
            customdata=dips["pct_deviation"]
        ))

    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text="<b>การตรวจจับความผิดปกติของข้อมูล (Statistical Anomaly Detection)</b><br><span style='font-size:12px; color:#64748B;'>วิเคราะห์ด้วย Bollinger Bands (±2σ) และเกณฑ์ Z-Score (หน่วย: คน)</span>",
            font=dict(size=14)
        ),
        xaxis=dict(title="<b>ช่วงเวลา (Period: YYYY-MM)</b>", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="<b>จำนวนนักท่องเที่ยว (คน)</b>", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

@_chart("กลุ่มจังหวัด", 110)
def create_cluster_scatter(clustered_df: pd.DataFrame) -> go.Figure:
    """
    K-Means clustering scatter: Yield vs Dependency Ratio with cluster colors.
    """
    fig = px.scatter(
        clustered_df,
        x="dependency_ratio",
        y="yield_per_tourist",
        color="cluster_label",
        size="total_revenue",
        hover_name="province_name_th",
        hover_data={
            "province_name_en": True,
            "region": True,
            "dependency_ratio": ":.1f% ของ GPP",
            "yield_per_tourist": ":,.0f บาท/คน",
            "foreign_share_pct": ":.1f%",
            "occupancy_rate": ":.1f%"
        },
        title="<b>การแบ่งกลุ่มเชิงยุทธศาสตร์ 77 จังหวัดด้วย K-Means (Provincial Strategic Clustering)</b><br><span style='font-size:12px; color:#64748B;'>แกน X: ดัชนีพึ่งพา (% GPP) | แกน Y: Yield (บาท/คน) | ขนาด = รายได้รวม</span>",
        labels={
            "dependency_ratio": "ดัชนีการพึ่งพาการท่องเที่ยว (% ของ GPP)",
            "yield_per_tourist": "รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (บาท/คน)",
            "cluster_label": "กลุ่มยุทธศาสตร์ (Cluster Archetype)"
        },
        color_discrete_sequence=[COLOR_CORAL, COLOR_TEAL, "#0D9488", COLOR_SAND_DARK]
    )

    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(title="<b>ดัชนีการพึ่งพาการท่องเที่ยว (Tourism Dependency Ratio - % ของ GPP)</b>", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="<b>รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Yield per Tourist - บาท/คน)</b>", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(title=dict(text="<b>กลุ่มยุทธศาสตร์</b>"), orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    return fig


@_chart("กลุ่มจังหวัด", 40)
def create_cluster_profile_chart(clustered_df: pd.DataFrame) -> go.Figure:
    """Small multiples: one panel per metric, one horizontal bar per cluster (mean value) for easy comparison."""
    from plotly.subplots import make_subplots
    cands = {"total_tourists": "นักท่องเที่ยว (คน)", "yield_per_tourist": "Yield (บาท/คน)",
             "dependency_ratio": "พึ่งพา GPP (%)", "foreign_share_pct": "ต่างชาติ (%)", "occupancy_rate": "เข้าพัก (%)"}
    cols = [c for c in cands if c in clustered_df.columns]
    prof = clustered_df.groupby("cluster_label")[cols].mean()
    sizes = clustered_df.groupby("cluster_label").size()
    labels = [f"{k.split(' (')[0]} (n={sizes[k]})" for k in prof.index]
    palette = [COLOR_CORAL, COLOR_TEAL, "#0D9488", COLOR_SAND_DARK]
    fig = make_subplots(rows=1, cols=len(cols), subplot_titles=[cands[c] for c in cols],
                        horizontal_spacing=0.04, shared_yaxes=True)
    for i, c in enumerate(cols, 1):
        fig.add_trace(go.Bar(x=prof[c], y=labels, orientation="h", showlegend=False,
                             marker_color=[palette[j % len(palette)] for j in range(len(labels))],
                             text=[f"{v:,.0f}" if v >= 100 else f"{v:,.1f}" for v in prof[c]],
                             textposition="outside", cliponaxis=False,
                             hovertemplate="%{y}<br>" + cands[c] + ": %{x:,.1f}<extra></extra>"), row=1, col=i)
        fig.update_xaxes(showticklabels=False, showgrid=False, range=[0, float(prof[c].max()) * 1.4 or 1], row=1, col=i)
    fig.update_annotations(font=dict(size=12, color=COLOR_DARK))
    fig.update_layout(**CHART_THEME, height=420)
    return fig