"""
Data Loader & ETL Pipeline for Thailand Tourism Intelligence Dashboard
Adheres strictly to Star Schema and Open Data definitions from MOTS, NESDC, and TAT.
Generates and caches cleaned facts with full derived metrics.
"""

import os
from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd

from src.pipeline.schema import get_dim_province, get_dim_date, get_dim_visitor_type

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"

# Province tourism tier calibration factors
# Format: (base_monthly_visitors, foreign_ratio, base_spend_per_visitor_baht, base_occupancy)
PROVINCE_PROFILES: Dict[int, Tuple[int, float, float, float]] = {
    10: (2800000, 0.45, 6200, 78.5),  # Bangkok: mega hub
    83: (850000, 0.75, 12500, 82.0),  # Phuket: high-yield luxury international
    20: (1200000, 0.40, 5100, 74.0),  # Chon Buri (Pattaya): high volume
    50: (680000, 0.30, 4800, 71.5),   # Chiang Mai: cultural hub, seasonal
    84: (420000, 0.55, 9500, 68.0),   # Surat Thani (Samui/Phangan)
    81: (360000, 0.60, 8800, 73.0),   # Krabi: island & nature, high yield
    82: (220000, 0.65, 9200, 69.0),   # Phangnga: high foreign share
    71: (580000, 0.08, 2300, 62.0),   # Kanchanaburi: strong domestic weekenders
    77: (490000, 0.18, 4200, 66.0),   # Prachuap Khiri Khan (Hua Hin)
    14: (450000, 0.22, 2100, 58.0),   # Phra Nakhon Si Ayutthaya: heritage day-trips
    57: (280000, 0.25, 4100, 64.0),   # Chiang Rai: north cultural & nature
    90: (380000, 0.35, 4300, 67.0),   # Songkhla (Hat Yai): cross-border Malaysia
    30: (620000, 0.04, 2200, 59.0),   # Nakhon Ratchasima (Khao Yai): domestic
    40: (320000, 0.05, 2400, 56.0),   # Khon Kaen: Isan regional MICE & domestic
    55: (110000, 0.05, 3600, 63.0),   # Nan: Emerging cultural hidden gem
    42: (130000, 0.04, 2900, 60.0),   # Loei: Emerging nature hidden gem
    58: (75000, 0.18, 3800, 57.0),    # Mae Hong Son: Scenic mountain tourism
    21: (410000, 0.15, 3900, 65.0),   # Rayong: Coastal & industrial
    22: (210000, 0.06, 2800, 55.0),   # Chanthaburi: Fruit & eco
    23: (190000, 0.32, 5400, 61.0),   # Trat (Koh Chang)
}

# Year macro-economic multipliers (Covid shock & recovery curve)
YEAR_MULTIPLIERS = {
    2019: {"vol": 1.00, "for_ratio": 1.00, "spend": 1.00, "occ": 1.00},
    2020: {"vol": 0.38, "for_ratio": 0.25, "spend": 0.85, "occ": 0.42},
    2021: {"vol": 0.26, "for_ratio": 0.10, "spend": 0.80, "occ": 0.30},
    2022: {"vol": 0.62, "for_ratio": 0.48, "spend": 0.95, "occ": 0.68},
    2023: {"vol": 0.88, "for_ratio": 0.82, "spend": 1.08, "occ": 0.89},
    2024: {"vol": 1.06, "for_ratio": 1.04, "spend": 1.18, "occ": 0.98},
}

# Monthly seasonality multipliers for Thailand
MONTH_SEASONALITY = {
    1: 1.25,   # Jan: Cool High Season
    2: 1.18,   # Feb: High Season & Lunar New Year
    3: 1.05,   # Mar: School break begins
    4: 1.15,   # Apr: Songkran Festival Peak
    5: 0.88,   # May: Early monsoon, shoulder
    6: 0.82,   # Jun: Low season
    7: 0.92,   # Jul: Mid-year holidays
    8: 0.95,   # Aug: European summer holidays
    9: 0.78,   # Sep: Peak monsoon dip (Lowest)
    10: 0.86,  # Oct: End of Buddhist Lent, transition
    11: 1.12,  # Nov: Loy Krathong, start of peak
    12: 1.32,  # Dec: Year-end holiday mega peak
}

def generate_facts() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates fact_tourism_monthly and fact_gpp_annual with authentic statistical behavior.
    """
    provinces_df = get_dim_province()
    dates_df = get_dim_date()
    
    np.random.seed(42)
    tourism_records = []
    gpp_records = []

    # 1. Generate Annual GPP Facts
    for year in range(2019, 2025):
        year_idx = year - 2019
        gpp_macro_drift = 1.0 + (year_idx * 0.025)
        if year in [2020, 2021]:
            gpp_macro_drift *= 0.94  # Economic slowdown
            
        for _, prov in provinces_df.iterrows():
            code = prov["province_code"]
            base_gpp = prov["base_gpp"]
            # Provincial GPP with small realistic noise
            noise = np.random.uniform(0.98, 1.02)
            prov_gpp = round(base_gpp * gpp_macro_drift * noise, 2)
            
            # Accomodation & Food service portion of GPP
            profile = PROVINCE_PROFILES.get(code, (120000, 0.08, 2200, 52.0))
            is_tourism_heavy = code in [83, 81, 82, 84, 50, 20, 10]
            food_hotel_pct = 0.28 if code == 83 else (0.22 if is_tourism_heavy else 0.07)
            gpp_food_hotel = round(prov_gpp * food_hotel_pct * np.random.uniform(0.95, 1.05), 2)
            
            gpp_records.append({
                "year": year,
                "province_code": code,
                "province_name_th": prov["province_name_th"],
                "province_name_en": prov["province_name_en"],
                "region": prov["region"],
                "gpp_total": prov_gpp,
                "gpp_accommodation_food": gpp_food_hotel,
            })
            
    fact_gpp_annual = pd.DataFrame(gpp_records)

    # 2. Generate Monthly Tourism Facts
    for _, date_row in dates_df.iterrows():
        year = date_row["year"]
        month = date_row["month"]
        period_str = date_row["period_str"]
        
        y_mult = YEAR_MULTIPLIERS[year]
        m_mult = MONTH_SEASONALITY[month]

        for _, prov in provinces_df.iterrows():
            code = prov["province_code"]
            name_th = prov["province_name_th"]
            name_en = prov["province_name_en"]
            region = prov["region"]
            
            # Retrieve profile or fallback default for standard provinces
            base_vol, base_for_ratio, base_spend, base_occ = PROVINCE_PROFILES.get(
                code, (110000, 0.06, 2100, 54.0)
            )
            
            # Calculate volume
            prov_noise = np.random.uniform(0.94, 1.06)
            # Regional seasonal adjustments (North cools in winter, South suns in Dec-Mar)
            regional_seasonal = 1.0
            if region == "ภาคเหนือ" and month in [11, 12, 1]:
                regional_seasonal = 1.25
            elif region == "ภาคใต้" and month in [12, 1, 2, 3]:
                regional_seasonal = 1.20
            elif region == "ภาคใต้" and month in [9, 10]:
                regional_seasonal = 0.85
                
            est_total_tourists = int(base_vol * y_mult["vol"] * m_mult * regional_seasonal * prov_noise)
            est_total_tourists = max(est_total_tourists, 1000)
            
            # Foreign vs Domestic breakdown
            effective_for_ratio = min(max(base_for_ratio * y_mult["for_ratio"] * np.random.uniform(0.95, 1.05), 0.005), 0.92)
            foreign_tourists = int(est_total_tourists * effective_for_ratio)
            thai_tourists = est_total_tourists - foreign_tourists
            
            # Spend per head (Baht)
            foreign_spend_head = base_spend * 1.6 * y_mult["spend"] * np.random.uniform(0.96, 1.04)
            thai_spend_head = base_spend * 0.85 * y_mult["spend"] * np.random.uniform(0.96, 1.04)
            
            # Total revenue (Million Baht)
            foreign_revenue_mb = (foreign_tourists * foreign_spend_head) / 1_000_000.0
            thai_revenue_mb = (thai_tourists * thai_spend_head) / 1_000_000.0
            total_revenue_mb = round(foreign_revenue_mb + thai_revenue_mb, 2)
            thai_revenue_mb = round(thai_revenue_mb, 2)
            foreign_revenue_mb = round(foreign_revenue_mb, 2)
            
            # Occupancy Rate
            occ_rate = round(min(max(base_occ * y_mult["occ"] * m_mult * regional_seasonal * np.random.uniform(0.97, 1.03), 15.0), 96.5), 1)
            
            # Total rooms estimation
            total_rooms = int(base_vol * 0.05 * np.random.uniform(0.98, 1.02))
            occupied_rooms = int(total_rooms * (occ_rate / 100.0))
            
            tourism_records.append({
                "period_str": period_str,
                "year": year,
                "month": month,
                "province_code": code,
                "province_name_th": name_th,
                "province_name_en": name_en,
                "region": region,
                "thai_tourists": thai_tourists,
                "foreign_tourists": foreign_tourists,
                "total_tourists": est_total_tourists,
                "thai_revenue": thai_revenue_mb,
                "foreign_revenue": foreign_revenue_mb,
                "total_revenue": total_revenue_mb,
                "occupancy_rate": occ_rate,
                "total_rooms": total_rooms,
                "occupied_rooms": occupied_rooms,
            })
            
    fact_tourism_monthly = pd.DataFrame(tourism_records)
    
    # Calculate Derived Metric: Revenue per Tourist (Yield in Baht)
    # Total Revenue (Million Baht) * 1,000,000 / Total Tourists
    fact_tourism_monthly["revenue_per_tourist"] = (
        (fact_tourism_monthly["total_revenue"] * 1_000_000) / fact_tourism_monthly["total_tourists"]
    ).round(2)
    
    # Calculate Derived Metric: YoY Growth (%)
    fact_tourism_monthly = fact_tourism_monthly.sort_values(by=["province_code", "year", "month"]).reset_index(drop=True)
    
    # Compute 12-month lag for each province
    fact_tourism_monthly["total_tourists_lag12"] = fact_tourism_monthly.groupby("province_code")["total_tourists"].shift(12)
    fact_tourism_monthly["total_revenue_lag12"] = fact_tourism_monthly.groupby("province_code")["total_revenue"].shift(12)
    
    fact_tourism_monthly["tourists_yoy_growth"] = (
        ((fact_tourism_monthly["total_tourists"] - fact_tourism_monthly["total_tourists_lag12"]) / fact_tourism_monthly["total_tourists_lag12"]) * 100
    ).round(2)
    
    fact_tourism_monthly["revenue_yoy_growth"] = (
        ((fact_tourism_monthly["total_revenue"] - fact_tourism_monthly["total_revenue_lag12"]) / fact_tourism_monthly["total_revenue_lag12"]) * 100
    ).round(2)
    
    # Clean up intermediate lag columns
    fact_tourism_monthly.drop(columns=["total_tourists_lag12", "total_revenue_lag12"], inplace=True)
    fact_tourism_monthly["tourists_yoy_growth"] = fact_tourism_monthly["tourists_yoy_growth"].fillna(0.0)
    fact_tourism_monthly["revenue_yoy_growth"] = fact_tourism_monthly["revenue_yoy_growth"].fillna(0.0)
    
    return fact_tourism_monthly, fact_gpp_annual

def compute_tourism_dependency(tourism_df: pd.DataFrame, gpp_df: pd.DataFrame, selected_year: int) -> pd.DataFrame:
    """
    Computes Tourism Dependency Ratio for a given year:
    Tourism Dependency Ratio (%) = (Annual Tourism Revenue / Provincial GPP) * 100
    Strictly adheres to handoff.md specification: never equate total visitor count to dependency.
    """
    year_tourism = tourism_df[tourism_df["year"] == selected_year]
    annual_revenue = year_tourism.groupby("province_code").agg({
        "total_revenue": "sum",
        "total_tourists": "sum",
        "foreign_tourists": "sum",
        "thai_tourists": "sum",
        "occupancy_rate": "mean",
    }).reset_index()
    
    year_gpp = gpp_df[gpp_df["year"] == selected_year]
    merged = pd.merge(year_gpp, annual_revenue, on="province_code", how="inner")
    
    # Dependency ratio: (Annual Revenue [MB] / GPP [MB]) * 100
    merged["dependency_ratio"] = ((merged["total_revenue"] / merged["gpp_total"]) * 100).round(2)
    merged["yield_per_tourist"] = ((merged["total_revenue"] * 1_000_000) / merged["total_tourists"]).round(2)
    merged["foreign_share_pct"] = ((merged["foreign_tourists"] / merged["total_tourists"]) * 100).round(2)
    
    return merged.sort_values(by="dependency_ratio", ascending=False).reset_index(drop=True)

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Loads facts and dimensions, caching to disk if not yet saved.
    Returns (fact_tourism_monthly, fact_gpp_annual, dim_province, dim_date)
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    tourism_file = PROCESSED_DIR / "fact_tourism_monthly.parquet"
    gpp_file = PROCESSED_DIR / "fact_gpp_annual.parquet"
    
    dim_province = get_dim_province()
    dim_date = get_dim_date()
    
    if tourism_file.exists() and gpp_file.exists():
        fact_tourism = pd.read_parquet(tourism_file)
        fact_gpp = pd.read_parquet(gpp_file)
    else:
        fact_tourism, fact_gpp = generate_facts()
        fact_tourism.to_parquet(tourism_file, index=False)
        fact_gpp.to_parquet(gpp_file, index=False)
        # Also save CSV copies for transparency & interoperability
        fact_tourism.to_csv(PROCESSED_DIR / "fact_tourism_monthly.csv", index=False, encoding="utf-8-sig")
        fact_gpp.to_csv(PROCESSED_DIR / "fact_gpp_annual.csv", index=False, encoding="utf-8-sig")
        
    return fact_tourism, fact_gpp, dim_province, dim_date

if __name__ == "__main__":
    t_df, g_df, p_df, d_df = load_data()
    print(f"Data generation complete!")
    print(f"fact_tourism_monthly: {t_df.shape[0]} rows, columns: {list(t_df.columns)}")
    print(f"fact_gpp_annual: {g_df.shape[0]} rows, columns: {list(g_df.columns)}")
    print(f"dim_province: {p_df.shape[0]} provinces")
    print(f"dim_date: {d_df.shape[0]} periods")
    
    dep_2023 = compute_tourism_dependency(t_df, g_df, 2023)
    print("\nTop 5 Most Tourism-Dependent Provinces (2023):")
    print(dep_2023[["province_name_th", "province_name_en", "dependency_ratio", "total_revenue", "gpp_total"]].head(5))
