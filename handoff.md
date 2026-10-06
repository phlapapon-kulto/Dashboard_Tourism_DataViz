# Business Requirements Document (BRD)
## Thailand Tourism Intelligence Dashboard

### 1. ภาพรวมโครงการ (Project Overview)
เอกสารข้อกำหนดทางธุรกิจ (BRD) นี้จัดทำขึ้นเพื่อใช้เป็นแนวทางในการพัฒนา **Thailand Tourism Intelligence Dashboard** โดยเชื่อมโยงกับแหล่งข้อมูลเปิด (Open Data) ที่ผ่านการตรวจสอบแล้ว เช่น กระทรวงการท่องเที่ยวและกีฬา (MOTS), การท่องเที่ยวแห่งประเทศไทย (TAT), สำนักงานสถิติแห่งชาติ (NSO) และ data.go.th แพลตฟอร์มนี้ออกแบบมาเพื่อตอบโจทย์ผู้บริหาร นักวิเคราะห์ และผู้กำหนดนโยบายในการวิเคราะห์ข้อมูลเชิงลึกด้านการท่องเที่ยวของประเทศไทย แบ่งการแสดงผลออกเป็น 3 Tab หลัก

---

### 2. รายละเอียดแต่ละ Tab (Tab-by-Tab Specification)

#### Tab 1 — Tourism Demand & Visitors (อุปสงค์และพฤติกรรมการเดินทางของผู้เยี่ยมเยือน)
* **วัตถุประสงค์หลัก:** วิเคราะห์ปริมาณนักท่องเที่ยวและการกระจายตัวเชิงพื้นที่ (Spatial Distribution) ทั้งชาวไทยและชาวต่างชาติ
* **องค์ประกอบหน้าจอ (UI Components & Visualizations):**
  1. **KPI Summary Cards:** แสดงตัวเลขรวมของนักท่องเที่ยวทั้งหมด, สัดส่วนนักท่องเที่ยวไทย (Domestic) vs ต่างชาติ (International), และอัตราการเติบโตเทียบกับช่วงเดียวกันของปีก่อน (YoY Growth)
  2. **Trend รายเดือน (Monthly Trend Line Chart):** กราฟเส้นแสดงแนวโน้มจำนวนผู้เยี่ยมเยือนรายเดือน เปรียบเทียบย้อนหลัง (YoY Comparison) เพื่อดูพฤติกรรมการเดินทาง
  3. **Ranking รายจังหวัด (Top Provinces Bar Chart):** จัดอันดับจังหวัดที่มีจำนวนผู้เยี่ยมเยือนสูงสุด 10 อันดับแรก
  4. **Map ประเทศไทย (Geospatial Choropleth Map):** แผนที่ประเทศไทยแสดงความหนาแน่นของจำนวนนักท่องเที่ยวรายจังหวัด (Heatmap/Choropleth)
  5. **Seasonality Analysis:** กราฟวิเคราะห์ฤดูกาลท่องเที่ยว (Peak / Low Season) เพื่อระบุเดือนที่มีการกระจุกตัวของนักท่องเที่ยวสูงสุด

#### Tab 2 — Tourism Revenue & Accommodation (รายได้และการใช้บริการที่พัก)
* **วัตถุประสงค์หลัก:** ประเมินมูลค่าทางเศรษฐกิจจากการท่องเที่ยวและประสิทธิภาพการใช้ประโยชน์จากโครงสร้างพื้นฐานด้านที่พัก
* **องค์ประกอบหน้าจอ (UI Components & Visualizations):**
  1. **Economic KPI Cards:** รายได้รวมจากการท่องเที่ยวทั้งหมด (Total Tourism Revenue), รายได้เฉลี่ยต่อผู้เยี่ยมเยือน (Revenue per Visitor), และอัตราการเข้าพักแรมเฉลี่ย (Average Occupancy Rate - AOR)
  2. **Revenue Trend (Line Chart):** กราฟแสดงแนวโน้มรายได้จากการท่องเที่ยวย้อนหลังรายเดือน/รายไตรมาส
  3. **Visitors vs Revenue (Scatter Plot / Dual-Axis Chart):** กราฟเปรียบเทียบระหว่างจำนวนผู้เยี่ยมเยือนและรายได้ที่สร้างได้ เพื่อหาความสัมพันธ์เชิงเศรษฐกิจ (High Volume vs High Yield)
  4. **อัตราการเข้าพัก (Accommodation Occupancy Rate Bar Chart):** แสดงอัตราการเข้าพักแรมแยกตามรายจังหวัดหรือรายภาค เพื่อระบุพื้นที่ที่มีอัตราการใช้บริการสูงหรือต่ำกว่าเกณฑ์เฉลี่ย

#### Tab 3 — Tourism Intelligence (ระบบอัจฉริยะวิเคราะห์โอกาสและข้อมูลเชิงลึก)
* **วัตถุประสงค์หลัก:** สังเคราะห์ข้อมูลเพื่อหาโอกาสทางธุรกิจ ตรวจความผิดปกติ และนำเสนอข้อเสนอแนะเชิงนโยบายแบบอัตโนมัติ (Rule-based & Analytics)
* **องค์ประกอบหน้าจอ (UI Components & Visualizations):**
  1. **Opportunity Matrix (Four-Quadrant Scatter Plot):**
     * แกน X: รายได้ต่อผู้เยี่ยมเยือน (Revenue per Visitor / Yield)
     * แกน Y: อัตราการเติบโต (Growth Rate)
     * แบ่งกลุ่มจังหวัดเป็น 4 ควอแดนันท์ เพื่อหาจังหวัดที่เป็น *High Demand / High Revenue* และจังหวัดที่มีศักยภาพซ่อนอยู่ (Hidden Gems)
  2. **Seasonality & Anomaly Detection Panel:** ระบบตรวจจับความผิดปกติของข้อมูล (เช่น จังหวัดที่จำนวนนักท่องเที่ยวตกหล่นผิดปกติ หรือเติบโตสูงผิดวิสัยทัศน์ในเดือนใดเดือนหนึ่ง)
  3. **Rule-based Insights & Recommendations (Smart Cards):** กล่องข้อความสรุปอินไซต์อัตโนมัติ เช่น *"จังหวัดภูเก็ตมีอัตราการเติบโตของรายได้สูงกว่าจำนวนนักท่องเที่ยว 15% สะท้อนถึง High-Yield Tourism"*

---

### 3. Handoff Specification สำหรับ Antigravity
* **Target Environment:** Antigravity Dashboard Engine (Interactive Web-based UI)
* **Data Connectors:** REST API (TAT Data API) & CSV Parsers (MOTS / data.go.th)
* **Global Filters:** * Year Selector (ตัวเลือกปี)
  * Month Range Filter (ช่วงเดือน)
  * Region / Province Selector (ตัวกรองภูมิภาคและจังหวัด)
  * Visitor Type Filter (ทั้งหมด / ชาวไทย / ชาวต่างชาติ)
