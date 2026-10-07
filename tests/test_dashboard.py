"""
Unit and Integration Tests for Thailand Tourism Intelligence Dashboard
"""

import unittest
import pandas as pd
import numpy as np

from src.pipeline.schema import get_dim_province, get_dim_date, get_dim_visitor_type
from src.pipeline.data_loader import load_data, compute_tourism_dependency
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

class TestThailandTourismDashboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fact_tourism, cls.fact_gpp, cls.dim_province, cls.dim_date = load_data()

    def test_dimensions(self):
        """Verify Thailand 77 provinces and date dimension completeness"""
        self.assertEqual(len(self.dim_province), 77, "Should have exactly 77 provinces")
        self.assertIn("province_name_th", self.dim_province.columns)
        self.assertIn("province_name_en", self.dim_province.columns)
        self.assertIn("region", self.dim_province.columns)
        self.assertIn("lat", self.dim_province.columns)
        self.assertIn("lon", self.dim_province.columns)
        
        # Verify date dimension covers 2019 - 2024 (6 years * 12 months = 72 periods)
        self.assertEqual(len(self.dim_date), 72, "Should cover 72 monthly periods")

    def test_derived_metrics_and_formulas(self):
        """Verify derived metrics formulas strictly follow handoff specifications"""
        # Test 1: Revenue per Tourist = Total Revenue * 1M / Total Tourists
        sample = self.fact_tourism.iloc[0]
        expected_yield = round((sample["total_revenue"] * 1_000_000) / sample["total_tourists"], 2)
        self.assertAlmostEqual(sample["revenue_per_tourist"], expected_yield, places=1)

        # Test 2: Dependency ratio = (Total Revenue / Provincial GPP) * 100
        dep_df = compute_tourism_dependency(self.fact_tourism, self.fact_gpp, 2023)
        self.assertFalse(dep_df.empty)
        sample_dep = dep_df.iloc[0]
        expected_dep = round((sample_dep["total_revenue"] / sample_dep["gpp_total"]) * 100, 2)
        self.assertAlmostEqual(sample_dep["dependency_ratio"], expected_dep, places=1)
        
        # Verify top dependency is NOT simply Bangkok (which has highest visitors)
        # Phuket, Krabi, or Phangnga should lead in dependency ratio
        top_province = dep_df.iloc[0]["province_name_en"]
        self.assertIn(top_province, ["Phuket", "Krabi", "Phangnga", "Surat Thani", "Trat"])

    def test_intelligence_engine(self):
        """Verify Opportunity Matrix, Anomaly Detection, Rule-based insights, and Clustering"""
        # Opportunity Matrix
        matrix_df, med_yield, med_growth = compute_opportunity_matrix(self.fact_tourism)
        self.assertIn("quadrant", matrix_df.columns)
        self.assertGreater(med_yield, 0)

        # Anomaly Detection
        anom_df = detect_anomalies(self.fact_tourism, province_code=83)
        self.assertIn("anomaly_status", anom_df.columns)

        # Smart Recommendations
        insights = generate_smart_recommendations(self.fact_tourism, self.fact_gpp, 2023)
        self.assertGreaterEqual(len(insights), 3)

        # Clustering
        clustered = perform_province_clustering(self.fact_tourism, self.fact_gpp, 2023)
        self.assertIn("cluster_label", clustered.columns)
        self.assertEqual(len(clustered["cluster_id"].unique()), 4)

    def test_charts_compilation(self):
        """Verify that all Plotly chart generation functions run without errors"""
        sub_df = self.fact_tourism[self.fact_tourism["year"] == 2023]
        
        fig1 = create_monthly_trend_chart(sub_df)
        self.assertIsNotNone(fig1)

        fig2 = create_top_provinces_chart(sub_df)
        self.assertIsNotNone(fig2)

        fig3 = create_thailand_map(sub_df)
        self.assertIsNotNone(fig3)

        fig4 = create_seasonality_chart(sub_df)
        self.assertIsNotNone(fig4)

        fig5 = create_visitor_share_donut(sub_df)
        self.assertIsNotNone(fig5)

        fig6 = create_volume_vs_yield_scatter(sub_df)
        self.assertIsNotNone(fig6)

        fig7 = create_occupancy_bar_chart(sub_df)
        self.assertIsNotNone(fig7)

    def test_travel_recommendations(self):
        """Verify dynamic Top 5 province calculation strictly from data"""
        from src.components.recommendations import get_top5_recommended_provinces
        sub_df = self.fact_tourism[self.fact_tourism["year"] == 2024]
        top5 = get_top5_recommended_provinces(sub_df)
        self.assertEqual(len(top5), 5, "Should return exactly 5 provinces")
        
        # Verify rank order is descending
        for i in range(len(top5) - 1):
            self.assertGreaterEqual(top5[i]["total_tourists"], top5[i+1]["total_tourists"])
            self.assertEqual(top5[i]["rank"], i + 1)
            self.assertTrue(len(top5[i]["meta"]["attractions"]) > 0)
            self.assertTrue(len(top5[i]["meta"]["image_url"]) > 0)

if __name__ == "__main__":
    unittest.main()
