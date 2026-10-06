"""
Visualization Components for Thailand Tourism Intelligence Dashboard
Built with Plotly for interactive dashboards.
"""

from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Palette constants
COLOR_PRIMARY = "#1E3A8A"     # Deep Royal Navy
COLOR_SECONDARY = "#0D9488"   # Thai Andaman Teal
COLOR_ACCENT = "#F59E0B"      # Thai Temple Gold
COLOR_DANGER = "#EF4444"      # Coral Red
COLOR_SUCCESS = "#10B981"     # Emerald Green
COLOR_PURPLE = "#8B5CF6"      # Royal Orchid Purple

CHART_THEME = {
    "font": {"family": "Sarabun, Prompt, -apple-system, sans-serif"},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": dict(l=20, r=20, t=40, b=20),
}

def create_monthly_trend_chart(df: pd.DataFrame, metric: str = "total_tourists") -> go.Figure:
    """
    Monthly Trend Chart showing YoY multi-year comparison line chart.
    """
    label_map = {
        "total_tourists": "จำนวนนักท่องเที่ยวทั้งหมด (คน)",
        "total_revenue": "รายได้จากการท่องเที่ยว (ล้านบาท)",
        "thai_tourists": "นักท่องเที่ยวชาวไทย (คน)",
        "foreign_tourists": "นักท่องเที่ยวต่างชาติ (คน)",
    }
    
    # Aggregate monthly by year
    monthly = df.groupby(["year", "month"]).agg({metric: "sum"}).reset_index()
    month_names_th = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
                      "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    monthly["month_label"] = monthly["month"].apply(lambda m: month_names_th[m - 1])
    
    fig = go.Figure()
    years = sorted(monthly["year"].unique())
    colors = px.colors.sample_colorscale("Plasma", [i / max(1, len(years) - 1) for i in range(len(years))])

    for i, yr in enumerate(years):
        sub = monthly[monthly["year"] == yr].sort_values("month")
        is_latest = (i == len(years) - 1)
        fig.add_trace(go.Scatter(
            x=sub["month_label"],
            y=sub[metric],
            name=f"ปี {yr + 543} ({yr})",
            mode="lines+markers",
            line=dict(
                width=3.5 if is_latest else 1.8,
                dash="solid" if is_latest else "dot" if yr in [2020, 2021] else "solid"
            ),
            marker=dict(size=7 if is_latest else 5),
            hovertemplate=f"<b>{yr + 543} - %{{x}}</b><br>{label_map.get(metric, metric)}: %{{y:,.0f}}<extra></extra>"
        ))

    fig.update_layout(
        **CHART_THEME,
        title=dict(text=f"📈 แนวโน้มรายเดือนเปรียบเทียบย้อนหลัง (Monthly YoY Trend: {label_map.get(metric, metric)})", font=dict(size=15)),
        xaxis=dict(title="", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title=label_map.get(metric, metric), showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    return fig

def create_top_provinces_chart(df: pd.DataFrame, top_n: int = 10, metric: str = "total_tourists") -> go.Figure:
    """
    Top Provinces Ranking Bar Chart.
    """
    metric_titles = {
        "total_tourists": "นักท่องเที่ยวรวม (คน)",
        "total_revenue": "รายได้รวม (ล้านบาท)",
        "foreign_tourists": "นักท่องเที่ยวต่างชาติ (คน)",
        "thai_tourists": "นักท่องเที่ยวชาวไทย (คน)",
        "revenue_per_tourist": "รายได้เฉลี่ยต่อหัว (บาท)"
    }
    
    agg = df.groupby(["province_code", "province_name_th", "province_name_en", "region"]).agg({
        metric: "mean" if metric == "revenue_per_tourist" else "sum"
    }).reset_index()
    
    top_df = agg.sort_values(by=metric, ascending=True).tail(top_n)
    top_df["display_name"] = top_df["province_name_th"] + " (" + top_df["province_name_en"] + ")"

    fig = px.bar(
        top_df,
        x=metric,
        y="display_name",
        orientation="h",
        color="region",
        title=f"🏆 10 อันดับจังหวัดสูงสุด ({metric_titles.get(metric, metric)})",
        color_discrete_sequence=px.colors.qualitative.Prism,
        labels={metric: metric_titles.get(metric, metric), "display_name": "จังหวัด", "region": "ภูมิภาค"}
    )
    
    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title=""),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>ภูมิภาค: %{customdata[0]}<br>ค่า: %{x:,.1f}<extra></extra>",
        customdata=top_df[["region"]]
    )
    return fig

def create_thailand_map(df: pd.DataFrame, metric: str = "total_tourists") -> go.Figure:
    """
    Interactive Geospatial Map of Thailand's 77 provinces with proportional bubble markers.
    """
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

    metric_name_th = "จำนวนนักท่องเที่ยว (คน)" if metric == "total_tourists" else "รายได้จากการท่องเที่ยว (ล้านบาท)"

    hover_dict = {
        "lat": False,
        "lon": False,
        "province_name_en": True,
        "region": True,
        "total_tourists": ":,.0f",
        "total_revenue": ":,.1f",
        "yield_baht": ":,.0f",
        "foreign_pct": ":.1f%",
        "occupancy_rate": ":.1f%"
    }

    if hasattr(px, "scatter_map"):
        fig = px.scatter_map(
            geo_df,
            lat="lat",
            lon="lon",
            size=metric,
            color=metric,
            hover_name="province_name_th",
            hover_data=hover_dict,
            color_continuous_scale="Plasma",
            size_max=32,
            zoom=4.8,
            center=dict(lat=13.2, lon=101.0),
            map_style="open-street-map",
            title=f"🗺️ แผนที่การกระจายตัวเชิงพื้นที่ (Geospatial Density: {metric_name_th})"
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
            color_continuous_scale="Plasma",
            size_max=32,
            zoom=4.8,
            center=dict(lat=13.2, lon=101.0),
            mapbox_style="carto-positron",
            title=f"🗺️ แผนที่การกระจายตัวเชิงพื้นที่ (Geospatial Density: {metric_name_th})"
        )

    theme = dict(CHART_THEME)
    theme["margin"] = dict(l=0, r=0, t=35, b=0)
    fig.update_layout(
        **theme,
        coloraxis_colorbar=dict(title="", orientation="h", y=-0.05)
    )
    return fig

def create_seasonality_chart(df: pd.DataFrame) -> go.Figure:
    """
    Seasonality Chart analyzing Peak, Shoulder, and Low seasons.
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
    
    # Categorize seasons
    def get_season_badge(m):
        if m in [11, 12, 1, 2]:
            return "High Season (ช่วงไฮซีซั่น)"
        elif m in [3, 4, 7, 8]:
            return "Shoulder Season (ช่วงรอยต่อ)"
        return "Low Season / Green Season (โลว์ซีซั่น)"
        
    monthly_stats["season_category"] = monthly_stats["month"].apply(get_season_badge)

    fig = px.bar(
        monthly_stats,
        x="month_label",
        y="avg_tourists",
        color="season_category",
        title="☀️ การวิเคราะห์ฤดูกาลท่องเที่ยวไทย (Seasonality Cycle: Peak vs. Low Season)",
        color_discrete_map={
            "High Season (ช่วงไฮซีซั่น)": "#F59E0B",
            "Shoulder Season (ช่วงรอยต่อ)": "#3B82F6",
            "Low Season / Green Season (โลว์ซีซั่น)": "#10B981"
        },
        labels={"avg_tourists": "จำนวนนักท่องเที่ยวเฉลี่ย (คน)", "month_label": "เดือน", "season_category": "ฤดูกาล"}
    )
    
    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_visitor_share_donut(df: pd.DataFrame) -> go.Figure:
    """
    Donut chart of Thai Domestic vs Foreign International share.
    """
    total_thai = df["thai_tourists"].sum()
    total_foreign = df["foreign_tourists"].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=["นักท่องเที่ยวชาวไทย (Domestic)", "นักท่องเที่ยวต่างชาติ (International)"],
        values=[total_thai, total_foreign],
        hole=.55,
        marker=dict(colors=["#3B82F6", "#EC4899"]),
        hovertemplate="<b>%{label}</b><br>จำนวน: %{value:,.0f} คน<br>สัดส่วน: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="👥 สัดส่วนผู้เยี่ยมเยือน (Domestic vs. International)", font=dict(size=14)),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        annotations=[dict(text=f"รวม<br>{(total_thai + total_foreign) / 1_000_000:.1f}M", x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    return fig

def create_volume_vs_yield_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Tab 2: Visitors vs. Revenue (High Volume vs High Yield) Scatter Plot.
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
            "total_tourists": ":,.0f",
            "total_revenue": ":,.1f",
            "yield_per_visitor": ":,.1f",
            "occupancy_rate": ":.1f%"
        },
        title="💰 ความสัมพันธ์ปริมาณ vs รายได้ (Volume vs. Yield: High Volume vs. High Yield)",
        labels={
            "total_tourists": "จำนวนนักท่องเที่ยวรวม (คน - Volume)",
            "total_revenue": "รายได้รวมจากการท่องเที่ยว (ล้านบาท)",
            "region": "ภูมิภาค",
            "yield_per_visitor": "รายได้เฉลี่ยต่อหัว (บาท)"
        },
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", type="log"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", type="log"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_occupancy_bar_chart(df: pd.DataFrame) -> go.Figure:
    """
    Tab 2: Accommodation Occupancy Rate by Region & Province vs National Benchmark.
    """
    reg_occ = df.groupby("region").agg({"occupancy_rate": "mean"}).reset_index().sort_values("occupancy_rate", ascending=False)
    nat_benchmark = df["occupancy_rate"].mean()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=reg_occ["region"],
        y=reg_occ["occupancy_rate"],
        marker_color="#0D9488",
        name="อัตราเข้าพักเฉลี่ยของภูมิภาค",
        text=reg_occ["occupancy_rate"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Occupancy Rate: %{y:.1f}%<extra></extra>"
    ))

    # Add national benchmark horizontal line
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=len(reg_occ) - 0.5,
        y0=nat_benchmark,
        y1=nat_benchmark,
        line=dict(color="#EF4444", width=2.5, dash="dash")
    )
    fig.add_annotation(
        x=len(reg_occ) - 1,
        y=nat_benchmark + 2.5,
        text=f"เกณฑ์เฉลี่ยประเทศ: {nat_benchmark:.1f}%",
        showarrow=False,
        font=dict(color="#EF4444", size=11, family="Sarabun")
    )

    fig.update_layout(
        **CHART_THEME,
        title=dict(text="🏨 อัตราการเข้าพักแรมเฉลี่ยรายภาคเทียบเกณฑ์ประเทศ (Occupancy Rate vs. Benchmark)", font=dict(size=14)),
        yaxis=dict(title="Occupancy Rate (%)", range=[0, 100], showgrid=True, gridcolor="#F1F5F9"),
        xaxis=dict(title="")
    )
    return fig

def create_opportunity_matrix_chart(matrix_df: pd.DataFrame, median_yield: float, median_growth: float) -> go.Figure:
    """
    Tab 3: Four-Quadrant Opportunity Matrix (Yield vs Growth).
    """
    color_map = {
        "Star: High Yield & High Growth (ดาวเด่นมูลค่าสูง)": "#10B981",
        "Hidden Gem: High Growth Potential (เพชรเม็ดงามน่าจับตา)": "#8B5CF6",
        "Mature Asset: High Yield Stable (แหล่งสร้างรายได้หลัก)": "#3B82F6",
        "Repositioning: Underperforming (ต้องยกระดับกลยุทธ์)": "#F59E0B",
    }

    fig = px.scatter(
        matrix_df,
        x="revenue_per_visitor",
        y="revenue_yoy_growth",
        color="quadrant",
        color_discrete_map=color_map,
        size="total_revenue",
        hover_name="province_name_th",
        hover_data={
            "province_name_en": True,
            "region": True,
            "revenue_per_visitor": ":,.0f บาท",
            "revenue_yoy_growth": ":.1f%",
            "total_tourists": ":,.0f คน",
            "total_revenue": ":,.1f MB"
        },
        title="🎯 Opportunity Matrix: การจัดกลุ่มโอกาสเชิงยุทธศาสตร์รายจังหวัด (4-Quadrant Strategic Positioning)",
        labels={
            "revenue_per_visitor": "รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Yield / Revenue per Visitor - บาท)",
            "revenue_yoy_growth": "อัตราการเติบโตของรายได้ (YoY Revenue Growth Rate - %)",
            "quadrant": "กลุ่มยุทธศาสตร์ (Quadrant)"
        }
    )

    # Add quadrant benchmark lines (Medians)
    fig.add_vline(x=median_yield, line_width=1.5, line_dash="dash", line_color="#94A3B8")
    fig.add_hline(y=median_growth, line_width=1.5, line_dash="dash", line_color="#94A3B8")

    # Annotate quadrants
    fig.add_annotation(
        x=matrix_df["revenue_per_visitor"].max() * 0.9,
        y=matrix_df["revenue_yoy_growth"].max() * 0.9,
        text="<b>⭐ STARS</b><br>High Yield / High Growth",
        showarrow=False,
        font=dict(color="#10B981", size=11)
    )
    fig.add_annotation(
        x=matrix_df["revenue_per_visitor"].min() * 1.1,
        y=matrix_df["revenue_yoy_growth"].max() * 0.9,
        text="<b>💎 HIDDEN GEMS</b><br>High Growth Potential",
        showarrow=False,
        font=dict(color="#8B5CF6", size=11)
    )

    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig

def create_anomaly_chart(anomaly_df: pd.DataFrame) -> go.Figure:
    """
    Tab 3: Time Series Anomaly Detection with Bollinger Bands.
    """
    fig = go.Figure()

    # Upper and Lower Bollinger bounds
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
        fillcolor="rgba(148, 163, 184, 0.15)",
        name="เกณฑ์ความผันแปรปกติ (Normal Band ±2σ)",
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
        line=dict(color="#2563EB", width=2.5),
        name="จำนวนนักท่องเที่ยวจริง",
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
            hovertemplate="<b>%{x} [Spike]</b><br>ค่าจริง: %{y:,.0f}<br>เบี่ยงเบน: %{customdata:+.1f}%<extra></extra>",
            customdata=spikes["pct_deviation"]
        ))

    if not dips.empty:
        fig.add_trace(go.Scatter(
            x=dips["period_str"],
            y=dips["total_tourists"],
            mode="markers",
            marker=dict(color="#EF4444", size=12, symbol="triangle-down", line=dict(color="white", width=2)),
            name="Anomaly Drop (ลดผิดปกติ)",
            hovertemplate="<b>%{x} [Drop]</b><br>ค่าจริง: %{y:,.0f}<br>เบี่ยงเบน: %{customdata:+.1f}%<extra></extra>",
            customdata=dips["pct_deviation"]
        ))

    fig.update_layout(
        **CHART_THEME,
        title=dict(text="🚨 การตรวจจับความผิดปกติของข้อมูล (Statistical Anomaly Detection)", font=dict(size=14)),
        xaxis=dict(title="", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="จำนวนนักท่องเที่ยว (คน)", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

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
            "dependency_ratio": ":.1f%",
            "yield_per_tourist": ":,.0f บาท",
            "foreign_share_pct": ":.1f%",
            "occupancy_rate": ":.1f%"
        },
        title="🧩 การแบ่งกลุ่มเชิงยุทธศาสตร์ 77 จังหวัดด้วย K-Means (Provincial Strategic Clustering)",
        labels={
            "dependency_ratio": "ดัชนีการพึ่งพาการท่องเที่ยว (Tourism Dependency Ratio - % ของ GPP)",
            "yield_per_tourist": "รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Yield per Tourist - บาท)",
            "cluster_label": "กลุ่มยุทธศาสตร์ (Cluster Archetype)"
        },
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    fig.update_layout(
        **CHART_THEME,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    return fig
