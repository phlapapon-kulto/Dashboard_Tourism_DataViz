"""
Intelligence & Analytics Engine for Thailand Tourism Intelligence Dashboard
Implements:
1. Four-Quadrant Opportunity Matrix (Yield vs Growth)
2. Time-Series Anomaly Detection (Z-Score & Rolling Bollinger Bands)
3. Rule-Based Strategic Policy & Business Recommendations
4. Provincial K-Means Clustering Segmentation
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def compute_opportunity_matrix(
    df: pd.DataFrame,
    min_visitors: int = 50000
) -> Tuple[pd.DataFrame, float, float]:
    """
    Computes coordinates and quadrant classification for the Opportunity Matrix.
    X-axis: Revenue per Visitor (Yield in Baht)
    Y-axis: YoY Revenue Growth Rate (%)
    """
    # Aggregate province metrics for the filtered period
    agg_df = df.groupby(["province_code", "province_name_th", "province_name_en", "region"]).agg({
        "total_tourists": "sum",
        "total_revenue": "sum",
        "foreign_tourists": "sum",
        "thai_tourists": "sum",
        "revenue_yoy_growth": "mean",
        "tourists_yoy_growth": "mean",
    }).reset_index()

    # Derived Yield
    agg_df["revenue_per_visitor"] = (
        (agg_df["total_revenue"] * 1_000_000) / agg_df["total_tourists"].replace(0, 1)
    ).round(2)
    agg_df["foreign_share_pct"] = (
        (agg_df["foreign_tourists"] / agg_df["total_tourists"].replace(0, 1)) * 100
    ).round(2)

    # Filter out very small baselines if requested
    filtered = agg_df[agg_df["total_tourists"] >= min_visitors].copy()
    if filtered.empty:
        filtered = agg_df.copy()

    # Thresholds: medians
    median_yield = float(filtered["revenue_per_visitor"].median())
    median_growth = float(filtered["revenue_yoy_growth"].median())

    def classify_quadrant(row):
        y = row["revenue_yoy_growth"]
        x = row["revenue_per_visitor"]
        if x >= median_yield and y >= median_growth:
            return "Star: High Yield & High Growth (ดาวเด่นมูลค่าสูง)"
        elif x < median_yield and y >= median_growth:
            return "Hidden Gem: High Growth Potential (เพชรเม็ดงามน่าจับตา)"
        elif x >= median_yield and y < median_growth:
            return "Mature Asset: High Yield Stable (แหล่งสร้างรายได้หลัก)"
        else:
            return "Repositioning: Underperforming (ต้องยกระดับกลยุทธ์)"

    filtered["quadrant"] = filtered.apply(classify_quadrant, axis=1)
    return filtered, median_yield, median_growth

def detect_anomalies(
    df: pd.DataFrame,
    province_code: int = None,
    z_threshold: float = 2.0
) -> pd.DataFrame:
    """
    Detects monthly tourist volume anomalies using rolling 3-month moving average
    and standard deviation score (Z-Score).
    """
    if province_code:
        sub_df = df[df["province_code"] == province_code].sort_values("period_str").copy()
    else:
        # National aggregate
        sub_df = df.groupby(["period_str", "year", "month"]).agg({
            "total_tourists": "sum",
            "total_revenue": "sum",
            "thai_tourists": "sum",
            "foreign_tourists": "sum"
        }).reset_index().sort_values("period_str")
        sub_df["province_name_th"] = "ระดับประเทศ (National)"
        sub_df["province_name_en"] = "Nationwide"

    # Rolling calculations
    sub_df["rolling_mean"] = sub_df["total_tourists"].rolling(window=3, min_periods=1).mean()
    sub_df["rolling_std"] = sub_df["total_tourists"].rolling(window=3, min_periods=1).std().fillna(1.0)
    sub_df["z_score"] = (sub_df["total_tourists"] - sub_df["rolling_mean"]) / sub_df["rolling_std"].replace(0, 1.0)
    sub_df["pct_deviation"] = (
        ((sub_df["total_tourists"] - sub_df["rolling_mean"]) / sub_df["rolling_mean"].replace(0, 1.0)) * 100
    ).round(2)

    # Flag anomaly
    def flag_anomaly(row):
        if row["z_score"] >= z_threshold:
            return "Surge Spike (พุ่งขึ้นผิดปกติ)"
        elif row["z_score"] <= -z_threshold:
            return "Drop Dip (ลดลงผิดปกติ)"
        return "Normal (ปกติ)"

    sub_df["anomaly_status"] = sub_df.apply(flag_anomaly, axis=1)
    return sub_df

def generate_smart_recommendations(
    filtered_df: pd.DataFrame,
    gpp_df: pd.DataFrame,
    selected_year: int
) -> List[Dict[str, Any]]:
    """
    Rule-based analytical engine synthesizing policy and strategic business insights.
    Adheres strictly to handoff guidelines:
    - Never equate highest tourists to highest dependency
    - Differentiate Domestic vs Foreign yield
    """
    insights = []
    
    # 1. Dependency Analysis
    from src.pipeline.data_loader import compute_tourism_dependency
    dep_df = compute_tourism_dependency(filtered_df, gpp_df, selected_year)
    
    if not dep_df.empty:
        top_dep = dep_df.iloc[0]
        insights.append({
            "category": "Tourism Economic Dependency (ความพึ่งพาทางเศรษฐกิจ)",
            "severity": "CRITICAL" if top_dep["dependency_ratio"] > 40 else "INFO",
            "icon": "⚠️" if top_dep["dependency_ratio"] > 40 else "📈",
            "title": f"จังหวัดที่พึ่งพาการท่องเที่ยวสูงสุด: {top_dep['province_name_th']} ({top_dep['province_name_en']})",
            "metric": f"{top_dep['dependency_ratio']}% ของ GPP",
            "body": (
                f"รายได้จากการท่องเที่ยวของ {top_dep['province_name_th']} คิดเป็นสัดส่วนสูงถึง "
                f"**{top_dep['dependency_ratio']}% ของผลิตภัณฑ์มวลรวมจังหวัด (GPP)** "
                f"(รายได้ {top_dep['total_revenue']:,.1f} ล้านบาท จาก GPP รวม {top_dep['gpp_total']:,.1f} ล้านบาท) "
                f"สะท้อนความเปราะบางต่อความผันผวนภายนอก นโยบายควรเน้นการประกันความเสี่ยงและการกระจายโครงสร้างเศรษฐกิจ"
            )
        })

    # 2. High-Yield vs High-Volume Matrix Insight
    prov_agg = filtered_df.groupby(["province_code", "province_name_th", "province_name_en"]).agg({
        "total_tourists": "sum",
        "total_revenue": "sum",
        "revenue_per_tourist": "mean",
        "revenue_yoy_growth": "mean",
        "tourists_yoy_growth": "mean"
    }).reset_index()

    if not prov_agg.empty:
        # Province with revenue growth outperforming visitor growth
        prov_agg["yield_expansion"] = prov_agg["revenue_yoy_growth"] - prov_agg["tourists_yoy_growth"]
        best_yield_prov = prov_agg.sort_values(by="yield_expansion", ascending=False).iloc[0]
        
        insights.append({
            "category": "High-Yield Transition (การยกระดับสู่การท่องเที่ยวคุณภาพ)",
            "severity": "SUCCESS",
            "icon": "💎",
            "title": f"การขยายตัวของคุณภาพรายได้: {best_yield_prov['province_name_th']} ({best_yield_prov['province_name_en']})",
            "metric": f"+{best_yield_prov['yield_expansion']:.1f}% Yield Spread",
            "body": (
                f"จังหวัด {best_yield_prov['province_name_th']} มีอัตราการเติบโตของรายได้ (+{best_yield_prov['revenue_yoy_growth']:.1f}%) "
                f"สูงกว่าการเติบโตของจำนวนนักท่องเที่ยว (+{best_yield_prov['tourists_yoy_growth']:.1f}%) ส่วนต่าง {best_yield_prov['yield_expansion']:.1f}% "
                f"สะท้อนการเปลี่ยนผ่านสู่โมเดล **High-Yield Tourism** (การใช้จ่ายต่อหัวสูงขึ้น) อย่างชัดเจน"
            )
        })

    # 3. Hidden Gems Potential (High Growth, Moderate/Low Base)
    hidden_gems = prov_agg[
        (prov_agg["total_tourists"] < prov_agg["total_tourists"].median()) &
        (prov_agg["revenue_yoy_growth"] > prov_agg["revenue_yoy_growth"].median())
    ].sort_values(by="revenue_yoy_growth", ascending=False)

    if not hidden_gems.empty:
        gem = hidden_gems.iloc[0]
        insights.append({
            "category": "Hidden Gems Opportunity (เมืองรองดาวรุ่ง)",
            "severity": "OPPORTUNITY",
            "icon": "🌟",
            "title": f"เมืองรองศักยภาพสูง: {gem['province_name_th']} ({gem['province_name_en']})",
            "metric": f"+{gem['revenue_yoy_growth']:.1f}% YoY Growth",
            "body": (
                f"จังหวัด {gem['province_name_th']} มีการเติบโตของรายได้โดดเด่นถึง +{gem['revenue_yoy_growth']:.1f}% "
                f"ในขณะที่ฐานนักท่องเที่ยวยังเป็นระดับเมืองรอง ({gem['total_tourists']:,.0f} คน) "
                f"เป็นเป้าหมายสำคัญสำหรับยุทธศาสตร์การกระจายตัวของนักท่องเที่ยวจากเมืองหลักสู่เมืองน่าเที่ยว"
            )
        })

    # 4. Seasonality Concentration Vulnerability
    monthly_sum = filtered_df.groupby("month")["total_tourists"].sum()
    if not monthly_sum.empty:
        peak_m = monthly_sum.idxmax()
        low_m = monthly_sum.idxmin()
        ratio = monthly_sum[peak_m] / monthly_sum[low_m] if monthly_sum[low_m] > 0 else 1.0
        month_names = {1: "มกราคม", 2: "กุมภาพันธ์", 3: "มีนาคม", 4: "เมษายน", 5: "พฤษภาคม", 6: "มิถุนายน",
                       7: "กรกฎาคม", 8: "สิงหาคม", 9: "กันยายน", 10: "ตุลาคม", 11: "พฤศจิกายน", 12: "ธันวาคม"}
        
        insights.append({
            "category": "Seasonality & Capacity Balance (สมดุลฤดูกาล)",
            "severity": "WARNING" if ratio > 1.6 else "INFO",
            "icon": "🗓️",
            "title": f"ความแปรผันของฤดูกาลท่องเที่ยว: Peak vs Low อัตราส่วน {ratio:.2f}x",
            "metric": f"{ratio:.2f}x Peak Spread",
            "body": (
                f"เดือนที่มีนักท่องเที่ยวหนาแน่นที่สุดคือ **{month_names.get(peak_m)}** ({monthly_sum[peak_m]:,.0f} คน) "
                f"เทียบกับเดือนที่ซบเซาที่สุด **{month_names.get(low_m)}** ({monthly_sum[low_m]:,.0f} คน) "
                f"ควรจัดแคมเปญกระตุ้น Green Season / Rainy Season และเทศกาลย่อยเพื่อลดการกระจุกตัวในโครงสร้างพื้นฐาน"
            )
        })

    return insights

def perform_province_clustering(
    tourism_df: pd.DataFrame,
    gpp_df: pd.DataFrame,
    selected_year: int,
    n_clusters: int = 4
) -> pd.DataFrame:
    """
    Segments 77 provinces into 4 strategic analytical clusters using K-Means.
    Features:
    1. Log Total Tourists (Volume scale)
    2. Revenue per Tourist (Yield Baht)
    3. Tourism Dependency Ratio (% GPP)
    4. Foreign Tourist Share (%)
    5. Average Occupancy Rate (%)
    """
    from src.pipeline.data_loader import compute_tourism_dependency
    dep_df = compute_tourism_dependency(tourism_df, gpp_df, selected_year)

    feature_cols = ["total_tourists", "yield_per_tourist", "dependency_ratio", "foreign_share_pct", "occupancy_rate"]
    X = dep_df[feature_cols].copy()
    
    # Log transform volume for normality
    X["total_tourists"] = np.log1p(X["total_tourists"])
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    dep_df["cluster_id"] = kmeans.fit_predict(X_scaled)
    
    # Map cluster IDs to human-readable strategic labels based on their centroids
    cluster_means = dep_df.groupby("cluster_id")[["yield_per_tourist", "dependency_ratio", "total_tourists", "foreign_share_pct"]].mean()
    
    labels = {}
    for c_id, row in cluster_means.iterrows():
        if row["dependency_ratio"] > 25 or row["foreign_share_pct"] > 40:
            labels[c_id] = "Cluster A: Global Island & High-Yield Hubs (แหล่งท่องเที่ยวนานาชาติมูลค่าสูง)"
        elif row["total_tourists"] > dep_df["total_tourists"].quantile(0.75):
            labels[c_id] = "Cluster B: Metropolitan & High-Volume Domestic (ศูนย์กลางเมืองหลวงและเมืองใหญ่)"
        elif row["yield_per_tourist"] > dep_df["yield_per_tourist"].median():
            labels[c_id] = "Cluster C: Emerging Culture & Eco Destinations (เมืองรองเชิงวัฒนธรรมและธรรมชาติ)"
        else:
            labels[c_id] = "Cluster D: Local Community & Agro-Tourism (การท่องเที่ยวชุมชนและเกษตรท้องถิ่น)"
            
    dep_df["cluster_label"] = dep_df["cluster_id"].map(labels)
    return dep_df
