# 🇹🇭 Thailand Tourism Intelligence Dashboard
> **ระบบแดชบอร์ดอัจฉริยะวิเคราะห์ข้อมูลการท่องเที่ยวไทย (Thailand Tourism Intelligence Dashboard)**  
> An interactive, data-driven analytical dashboard platform empowering executives, analysts, and policymakers to uncover deep insights into Thailand's tourism economy, visitor behaviors, and provincial economic dependencies using verified Open Data.

---

link : https://dashboardtourismdataviz-8ojdjesxhrokn7twnoygsf.streamlit.app/
## 📌 1. ภาพรวมโครงการ (Project Overview)

**Thailand Tourism Intelligence Dashboard** ได้รับการออกแบบและพัฒนาขึ้นเพื่อเป็นเครื่องมือกลางสำหรับผู้กำหนดนโยบาย (Policymakers), นักวิเคราะห์เศรษฐกิจ (Economic Analysts) และผู้ประกอบการท่องเที่ยว เพื่อตอบโจทย์คำถามสำคัญเชิงยุทธศาสตร์ด้านการท่องเที่ยวของประเทศไทย ผ่านการรวบรวม วิเคราะห์ และแสดงผลข้อมูลเชิงโต้ตอบ (Interactive Data Visualization)

### คำถามวิจัยหลัก (Core Research Questions)
1. **“จังหวัดไหนพึ่งพาการท่องเที่ยวมากที่สุด?”**  
   *หลีกเลี่ยงการสรุปความพึ่งพาจากจำนวนนักท่องเที่ยวเพียงอย่างเดียว* โดยคำนวณจาก **สัดส่วนรายได้จากการท่องเที่ยวเทียบกับผลิตภัณฑ์มวลรวมจังหวัด (Tourism Dependency Ratio = Tourism Revenue / GPP × 100)**
2. **“นักท่องเที่ยวเปลี่ยนพฤติกรรมอย่างไร?”**  
   วิเคราะห์การเปลี่ยนแปลงเชิงพฤติกรรมระหว่างนักท่องเที่ยวไทย (Domestic) กับชาวต่างชาติ (International), รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Revenue per Visitor / Yield), ความยาวนานในการพำนัก, และวงจรฤดูกาลท่องเที่ยว (Seasonality)

---

## 🏛️ 2. แหล่งข้อมูลเปิด (Verified Open Data Catalog)

โครงการนี้ยึดถือหลักการ **Data Integrity** โดยเชื่อมโยงกับแหล่งข้อมูลเปิด (Public / Open Data) จากหน่วยงานภาครัฐและองค์การระหว่างประเทศที่ผ่านการตรวจสอบแล้ว:

| แหล่งข้อมูล / หน่วยงาน | ชุดข้อมูล (Dataset) | ความละเอียด (Granularity) | ช่วงเวลา (Coverage) | รูปแบบ (Format) |
| :--- | :--- | :--- | :--- | :--- |
| **MOTS** (กระทรวงการท่องเที่ยวและกีฬา) | สถิตินักท่องเที่ยวและรายได้จากการท่องเที่ยวจำแนกตามจังหวัด | รายเดือน / รายจังหวัด | พ.ศ. 2554 – 2568 | CSV / Excel / API |
| **NESDC** (สภาพัฒน์) | ผลิตภัณฑ์ภาคและจังหวัด (Gross Provincial Product: GPP) | รายปี / รายจังหวัด | พ.ศ. 2551 – 2567 | XLSX / CSV |
| **NSO** (สำนักงานสถิติแห่งชาติ) & MOTS | จำนวนนักท่องเที่ยวต่างชาติจำแนกตามสัญชาติ | รายเดือน / รายประเทศ | พ.ศ. 2555 – 2567 | XLSX / CSV |
| **TAT** (การท่องเที่ยวแห่งประเทศไทย) | อัตราการเข้าพัก (Occupancy Rate) และจำนวนสถานพักแรม | รายเดือน / รายจังหวัด | พ.ศ. 2560 – ปัจจุบัน | CSV / JSON |
| **World Bank (WDI)** | International Tourism Arrivals & Receipts Benchmark | รายปี / รายประเทศ | ระยะยาว | CSV / API |

---

## 📊 3. โครงสร้างแดชบอร์ด (Tab-by-Tab Architecture)

แดชบอร์ดแบ่งออกเป็น 3 แท็บหลักตาม Business Requirements Document (BRD):

### 🔹 Tab 1 — Tourism Demand & Visitors (อุปสงค์และพฤติกรรมการเดินทาง)
* **KPI Summary Cards:** นักท่องเที่ยวรวม (Total Visitors), สัดส่วนไทย vs ต่างชาติ (Domestic vs International Breakdown), อัตราการเติบโต YoY (%)
* **Monthly Trend (Line Chart):** แนวโน้มจำนวนนักท่องเที่ยวรายเดือนเปรียบเทียบย้อนหลัง เพื่อวิเคราะห์พฤติกรรมและแนวโน้มการฟื้นตัว
* **Top Provinces Ranking (Bar Chart):** จัดอันดับ 10 จังหวัดยอดนิยมที่มีผู้เยี่ยมเยือนสูงสุด
* **Geospatial Choropleth Map:** แผนที่ประเทศไทยแสดงความหนาแน่นและการกระจายตัวเชิงพื้นที่ของนักท่องเที่ยวรายจังหวัด
* **Seasonality Analysis:** การกระจายตัวของนักท่องเที่ยวเพื่อจำแนกช่วง Peak Season, Shoulder Season และ Low Season

### 🔹 Tab 2 — Tourism Revenue & Accommodation (รายได้และการใช้บริการที่พัก)
* **Economic KPI Cards:** รายได้รวมจากการท่องเที่ยว (Total Tourism Revenue), รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Revenue per Visitor / Yield), อัตราการเข้าพักแรมเฉลี่ย (Average Occupancy Rate - AOR)
* **Revenue Trend (Line Chart):** เส้นทางรายได้ย้อนหลังรายเดือนและรายไตรมาส
* **Visitors vs. Revenue (Scatter / Dual-Axis):** เปรียบเทียบความสัมพันธ์เชิงเศรษฐกิจระหว่าง Volume (จำนวนคน) vs Yield (รายได้)
* **Accommodation Occupancy Rate (Bar Chart):** อัตราการเข้าพักแรมแยกตามจังหวัดและภูมิภาค เปรียบเทียบกับค่าเฉลี่ยระดับประเทศ

### 🔹 Tab 3 — Tourism Intelligence (ระบบอัจฉริยะวิเคราะห์โอกาสและข้อมูลเชิงลึก)
* **Opportunity Matrix (Four-Quadrant Scatter Plot):**
  * แกน X: รายได้ต่อหัว (Revenue per Visitor / Yield)
  * แกน Y: อัตราการเติบโต (YoY Growth Rate)
  * จัดกลุ่มจังหวัด 4 กลุ่ม: *Stars (High Demand & High Yield)*, *Emerging / Hidden Gems*, *Cash Cows (High Volume)*, และ *Need Repositioning*
* **Seasonality & Anomaly Detection:** ตรวจจับความผิดปกติของตัวเลข (Anomaly Drops / Spikes) ในแต่ละจังหวัด
* **Rule-based Insights & Smart Recommendations:** ระบบวิเคราะห์และสรุปข้อเสนอแนะเชิงนโยบายและกลยุทธ์แบบอัตโนมัติ
* **Advanced Analytics:** K-Means Clustering จำแนกโปรไฟล์จังหวัด และแบบจำลองพยากรณ์อนุกรมเวลา (Time Series Forecasting)

---

## 🧩 4. สถาปัตยกรรมข้อมูล (Data Architecture & Star Schema)

โครงการนำเสนอการจัดการข้อมูลตามโมเดล **Star Schema**:

```
                       ┌────────────────────────┐
                       │      dim_date          │
                       │ (date, year, month)    │
                       └───────────┬────────────┘
                                   │
┌───────────────────────┐          │          ┌─────────────────────────┐
│     dim_province      ├──────────┼──────────┤    dim_visitor_type     │
│ (code, name_th, en,   │          │          │ (visitor_type_id, type) │
│  region, lat, lon)    │          │          └─────────────────────────┘
└───────────┬───────────┘          │
            │          ┌───────────┴────────────┐
            ├──────────┤  fact_tourism_monthly  │
            │          │ (visitors, revenue,    │
            │          │  occupancy, etc.)      │
            │          └────────────────────────┘
            │
┌───────────┴───────────┐
│    fact_gpp_annual    │
│ (year, province_code, │
│  gpp_total, gpp_food) │
└───────────────────────┘
```

### สูตรการคำนวณตัวชี้วัดสำคัญ (Derived Metrics)
1. **รายได้เฉลี่ยต่อนักท่องเที่ยว (Revenue per Tourist):**
   $$\text{Revenue per Tourist} = \frac{\text{Total Tourism Revenue}}{\text{Total Tourists}}$$
2. **ดัชนีการพึ่งพาการท่องเที่ยว (Tourism Dependency Ratio):**
   $$\text{Tourism Dependency Ratio (\%)} = \left(\frac{\text{Tourism Revenue}}{\text{Provincial GPP}}\right) \times 100$$
3. **อัตราการเติบโตเทียบปีก่อนหน้า (YoY Growth Rate):**
   $$\text{YoY Growth (\%)} = \left(\frac{\text{Metric}_t - \text{Metric}_{t-12}}{\text{Metric}_{t-12}}\right) \times 100$$

---

## 🎛️ 5. ตัวกรองข้อมูลสากล (Global Interactive Filters)
- **Year Selector:** เลือกช่วงปีที่ต้องการวิเคราะห์ (พ.ศ. 2562 – 2567 / ค.ศ. 2019 – 2024)
- **Month Range Filter:** คัดกรองช่วงเดือน (มกราคม – ธันวาคม)
- **Region / Province Selector:** กรองตามภูมิภาค (เหนือ, ตะวันออกเฉียงเหนือ, กลาง, ใต้, ตะวันออก, ตะวันตก) หรือเลือกเฉพาะจังหวัด
- **Visitor Type Filter:** ทั้งหมด (Total), ชาวไทย (Domestic), หรือชาวต่างชาติ (International)

---

## 🛠️ 6. เทคโนโลยีที่ใช้ (Tech Stack) & การติดตั้ง (Setup)

- **Language:** Python 3.10+
- **Interactive Framework:** Streamlit
- **Data Engineering & Analytics:** Pandas, NumPy, Scikit-Learn
- **Visualization:** Plotly Express & Plotly Graph Objects, GeoJSON choropleth

### การติดตั้งและการรันระบบ (How to Run)
```bash
# 1. ติดตั้ง Dependencies
pip install -r requirements.txt

# 2. รันแอปพลิเคชันแดชบอร์ด
streamlit run app.py
```

---

## 📂 7. โครงสร้างโฟลเดอร์ (Project Structure)

```
Dashboard_Tourism_DataViz/
├── data/                       # คลังข้อมูล (Cleaned Data, Star Schema, GeoJSON)
│   ├── raw/                    # Raw Open Data
│   └── processed/              # Cleaned facts & dimensions (Parquet/CSV)
├── src/                        # Source Code
│   ├── components/             # Reusable UI components & charts
│   ├── pipeline/               # Data pipeline & ETL scripts
│   ├── analytics/              # Clustering, Anomaly Detection & Forecasting
│   └── utils/                  # Helper functions & metric calculators
├── .gitignore                  # Git ignore definitions
├── app.py                      # Main Streamlit Dashboard Application
├── handoff.md                  # Business Requirements Document (BRD)
├── handoff_data_catalog.md     # Open Data Catalog & Technical Blueprint
├── PROJECT_STATUS.md           # Step-by-step progress tracking
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```
