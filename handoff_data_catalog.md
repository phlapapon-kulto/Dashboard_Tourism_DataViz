# 🚀 Handoff Document & Open Data Catalog for Antigravity: Thailand Tourism Intelligence Dashboard

เอกสารฉบับนี้จัดทำขึ้นเพื่อส่งต่อ (Handoff) ให้กับระบบ AI หรือทีมพัฒนา **Antigravity** นำไปใช้เป็นพิมพ์เขียว (Blueprint) ในการสร้าง **Thailand Tourism Intelligence Dashboard** รวมถึงการเขียนโค้ด Data Pipeline, การจัดการ Star Schema และการสร้าง Visualizations ตามข้อกำหนดด้านล่างนี้อย่างเคร่งครัด

---

## 1. Project Overview & Core Research Questions

* **Project Name:** Thailand Tourism Intelligence Dashboard
* **Primary Research Questions:**
  1. *“จังหวัดไหนพึ่งพาการท่องเที่ยวมากที่สุด?”* (ห้ามใช้จำนวนนักท่องเที่ยวมาสรุปความพึ่งพาโดยตรง ต้องใช้สัดส่วนเทียบกับ GPP)
  2. *“นักท่องเที่ยวเปลี่ยนพฤติกรรมอย่างไร?”* (วิเคราะห์เปรียบเทียบ Thai vs Foreign, ระยะเวลาพำนัก, ค่าใช้จ่ายต่อหัว และแนวโน้มรายเดือน/รายปี)
* **Design Principle:** ห้ามสร้างข้อมูลขึ้นเองโดยเด็ดขาด ต้องใช้เฉพาะ Open Data / Public Data จากหน่วยงานรัฐบาลไทยและองค์การระหว่างประเทศที่ระบุไว้ในเอกสารนี้เท่านั้น

---

## 2. Complete Open Data Catalog (Open Data Sources)

ชุดข้อมูลทั้งหมดที่ผ่านการคัดเลือกและมี URL สำหรับดาวน์โหลดข้อมูลจริง:

### 1. สถิตินักท่องเที่ยวและรายได้จากการท่องเที่ยวรายจังหวัด
* **Dataset Name:** สถิตินักท่องเที่ยวและรายได้จากการท่องเที่ยวชาวไทยและชาวต่างชาติจำแนกตามจังหวัด
* **Owner:** กองเศรษฐกิจการท่องเที่ยวและกีฬา กระทรวงการท่องเที่ยวและกีฬา (MOTS)
* **Description:** ข้อมูลมหภาคด้านจำนวนผู้เยี่ยมเยือน นักท่องเที่ยวไทย/ต่างชาติ และรายได้จากการท่องเที่ยวรายจังหวัด
* **Variables:** `year`, `month`, `province_code`, `province_name`, `region`, `thai_tourists`, `foreign_tourists`, `total_tourists`, `thai_revenue`, `foreign_revenue`, `total_revenue`
* **Coverage:** พ.ศ. 2554 – 2568 | **Granularity:** รายเดือน / รายจังหวัด | **Unit:** คน / ล้านบาท
* **Format:** CSV / XLSX / API | **License:** Open Data Common
* **Direct Download URL:** [MOTS Tourism Statistics Download](https://mots.go.th/more_news.php?cid=531)
* **Dataset Page:** [MOTS Data Portal](https://mots.go.th)

### 2. ผลิตภัณฑ์ภาคและจังหวัด (Gross Regional and Provincial Product - GPP)
* **Dataset Name:** ตารางสถิติผลิตภัณฑ์ภาคและจังหวัด (Gross Provincial Product)
* **Owner:** สำนักงานสภาพัฒนาการเศรษฐกิจและสังคมแห่งชาติ (สภาพัฒน์ / NESDC)
* **Description:** บัญชีรายได้ประชาชาติระดับจังหวัด ใช้เป็นตัวหาร (Denominator) เพื่อคำนวณดัชนีการพึ่งพาการท่องเที่ยว
* **Variables:** `year`, `province_code`, `province_name`, `gpp_total`, `gpp_per_capita`, `gpp_accommodation_food`
* **Coverage:** พ.ศ. 2551 – 2567 | **Granularity:** รายปี / รายจังหวัด | **Unit:** ล้านบาท / บาท
* **Format:** XLSX / CSV | **License:** Open Data Common
* **Direct Download URL:** [NESDC GPP Excel Download](https://www.nesdc.go.th/en/info/gross-regional-and-provincial-product-gpp/)
* **Dataset Page:** [NESDC GPP Portal](https://www.nesdc.go.th)

### 3. จำนวนนักท่องเที่ยวชาวต่างชาติจำแนกตามสัญชาติ
* **Dataset Name:** จำนวนนักท่องเที่ยวชาวต่างชาติที่เดินทางเข้าประเทศไทย จำแนกตามสัญชาติ
* **Owner:** สำนักงานสถิติแห่งชาติ (NSO) ร่วมกับ กระทรวงการท่องเที่ยวและกีฬา
* **Description:** ข้อมูลสถิตินักท่องเที่ยวต่างชาติรายประเทศต้นทางเพื่อวิเคราะห์แนวโน้มและอัตราการเติบโต (YoY Growth)
* **Variables:** `year`, `month`, `nationality`, `tourist_count`, `yoy_growth`
* **Coverage:** พ.ศ. 2555 – 2567 | **Granularity:** รายเดือน / รายประเทศต้นทาง | **Unit:** คน / ร้อยละ (%)
* **Format:** XLSX / CSV | **License:** Open Data Common
* **Direct Download URL & Page:** [NSO Tourism Statistics and Indicators](https://www.nso.go.th/nsoweb/nso/statistics_and_indicators?impt_branch=320)

### 4. อัตราการเข้าพักแรมและข้อมูลสถานพักแรม (Occupancy Rate)
* **Dataset Name:** สถิติจำนวนห้องพัก อัตราการเข้าพัก และสถานประกอบการโรงแรม
* **Owner:** การท่องเที่ยวแห่งประเทศไทย (TAT Data Catalog)
* **Description:** ข้อมูลอุปทานด้านที่พัก อัตราการเข้าพัก (Occupancy Rate) รายจังหวัด
* **Variables:** `province`, `year`, `month`, `total_establishments`, `total_rooms`, `occupied_rooms`, `occupancy_rate`
* **Coverage:** ข้อมูลปัจจุบันและย้อนหลัง | **Granularity:** รายเดือน / รายจังหวัด | **Unit:** แห่ง / ห้อง / ร้อยละ (%)
* **Format:** CSV / JSON | **License:** Open Data Common
* **Direct Download URL & Page:** [TAT Data Catalog](https://datacatalog.tat.or.th/)

### 5. ข้อมูลการท่องเที่ยวระหว่างประเทศเปรียบเทียบ (International Benchmark)
* **Dataset Name:** International Tourism, Number of Arrivals & Tourism Receipts
* **Owner:** World Bank (World Development Indicators - WDI)
* **Description:** ข้อมูลเปรียบเทียบจำนวนนักท่องเที่ยวและรายได้ระหว่างประเทศไทยกับประเทศคู่แข่งระดับโลก
* **Variables:** `country_code`, `country_name`, `year`, `international_tourism_arrivals`, `international_tourism_receipts`
* **Coverage:** ข้อมูลย้อนหลังระยะยาว | **Granularity:** รายปี / รายประเทศ | **Unit:** คน / ล้าน USD
* **Format:** CSV / API | **License:** CC BY 4.0
* **Direct Download URL & Page:** [World Bank WDI Tourism Arrivals](https://data.worldbank.org/indicator/ST.INT.ARVL?locations=TH)

---

## 3. Data Architecture & Integration Schema (Star Schema)

* **Primary Join Keys:** เชื่อมโยงตารางผ่านฟิลด์ `year`, `month`, และ `province_code`
* **Derived Metrics ที่ Antigravity ต้องคำนวณเพิ่มในโค้ด:**
  1. **Revenue per Tourist:**
     $$\text{Revenue per Tourist} = \frac{\text{Total Tourism Revenue}}{\text{Total Tourists}}$$
  2. **Tourism Dependency Ratio:**
     $$\text{Tourism Dependency Ratio} = \left( \frac{\text{Tourism Revenue (หรือ GPP สาขาที่พักแรมและบริการอาหาร)}}{\text{Provincial GPP}} \right) \times 100$$
  3. **YoY Growth (%):**
     $$\text{YoY Growth} = \left( \frac{\text{Metric}_t - \text{Metric}_{t-12}}{\text{Metric}_{t-12}} \right) \times 100$$

---

## 4. Dashboard Requirements for Antigravity

Antigravity จะต้องสร้างหน้าจอและฟีเจอร์ใน Dashboard ดังต่อไปนี้:

* **KPI Header Cards:** Total Tourists, Total Revenue, Average Occupancy Rate, Revenue per Tourist, YoY Growth Rate.
* **Visualizations & Charts:**
  * 🗺️ **Tourism Map:** แผนที่ประเทศไทยแสดงความเข้มข้นของการท่องเที่ยวและค่า Dependency Index รายจังหวัด
  * 📊 **Province Ranking Bar Chart:** จัดอันดับจังหวัดที่มีนักท่องเที่ยวสูงสุดและสร้างรายได้สูงสุด
  * 📈 **Monthly Trend & Seasonality Line Chart:** กราฟเส้นแสดงแนวโน้มรายเดือนเพื่อดู High/Low Season
  * 🇹🇭 **Thai vs Foreign Comparison:** กราฟเปรียบเทียบสัดส่วนและพฤติกรรมระหว่างนักท่องเที่ยวไทยและต่างชาติ
  * 📉 **Advanced Analytics (Segmentation & Forecasting):** การจัดกลุ่มจังหวัด (K-Means Clustering: Mass Tourism, High Value, Emerging, Seasonal) และโมเดลพยากรณ์อนุกรมเวลา (Forecasting)
* **Interactive Filters:** ตัวกรองข้อมูลตาม ปี (Year), เดือน (Month), จังหวัด (Province), และประเภทนักท่องเที่ยว (Thai / Foreign)

---

## 5. Critical Guidelines & Warnings for Antigravity

1. **ห้ามสรุปสมมติฐานเกินข้อมูล:** ห้ามระบุว่า *“จังหวัดที่มีนักท่องเที่ยวมากที่สุด = จังหวัดที่พึ่งพาการท่องเที่ยวมากที่สุด”* เด็ดขาด ต้องอ้างอิงจาก Tourism Dependency Index เท่านั้น
2. **การรักษาความถูกต้องของนิยาม:** ห้ามนำคำว่า *Visitor*, *Tourist*, *Guest* และ *Traveller* มาปะปนหรือบวกกันโดยไม่ตรวจสอบนิยามของชุดข้อมูลต้นทาง
3. **การจัดการ Missing Values:** หากข้อมูลรายเดือนบางจังหวัดขาดหาย ให้ใช้ค่าเฉลี่ยเคลื่อนที่ (Moving Average) หรืออิงสัดส่วนอัตราการเติบโตของภูมิภาคเดียวกัน

---
*เอกสารฉบับนี้พร้อมสำหรับให้ระบบ Antigravity อ่านและเริ่มดำเนินกระบวนการเขียนโค้ด Data Pipeline, Star Schema และ Dashboard UI ทันที*