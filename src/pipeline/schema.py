"""
Data Architecture & Star Schema Definitions for Thailand Tourism Intelligence Dashboard
Defines dimensions: dim_province, dim_date, dim_visitor_type
"""

from typing import List, Dict, Any
import pandas as pd

# 77 Provinces of Thailand with geographic coordinates, region, and official codes
PROVINCES_DATA: List[Dict[str, Any]] = [
    # Bangkok & Central Region (ภาคกลาง)
    {"province_code": 10, "province_name_th": "กรุงเทพมหานคร", "province_name_en": "Bangkok", "region": "ภาคกลาง", "lat": 13.7563, "lon": 100.5018, "base_gpp": 5300000},
    {"province_code": 11, "province_name_th": "สมุทรปราการ", "province_name_en": "Samut Prakan", "region": "ภาคกลาง", "lat": 13.5991, "lon": 100.5998, "base_gpp": 820000},
    {"province_code": 12, "province_name_th": "นนทบุรี", "province_name_en": "Nonthaburi", "region": "ภาคกลาง", "lat": 13.8621, "lon": 100.5144, "base_gpp": 340000},
    {"province_code": 13, "province_name_th": "ปทุมธานี", "province_name_en": "Pathum Thani", "region": "ภาคกลาง", "lat": 14.0208, "lon": 100.5250, "base_gpp": 410000},
    {"province_code": 14, "province_name_th": "พระนครศรีอยุธยา", "province_name_en": "Phra Nakhon Si Ayutthaya", "region": "ภาคกลาง", "lat": 14.3532, "lon": 100.5684, "base_gpp": 450000},
    {"province_code": 15, "province_name_th": "อ่างทอง", "province_name_en": "Ang Thong", "region": "ภาคกลาง", "lat": 14.5896, "lon": 100.4550, "base_gpp": 32000},
    {"province_code": 16, "province_name_th": "ลพบุรี", "province_name_en": "Lop Buri", "region": "ภาคกลาง", "lat": 14.7995, "lon": 100.6534, "base_gpp": 120000},
    {"province_code": 17, "province_name_th": "สิงห์บุรี", "province_name_en": "Sing Buri", "region": "ภาคกลาง", "lat": 14.8879, "lon": 100.4042, "base_gpp": 31000},
    {"province_code": 18, "province_name_th": "ชัยนาท", "province_name_en": "Chai Nat", "region": "ภาคกลาง", "lat": 15.1852, "lon": 100.1251, "base_gpp": 38000},
    {"province_code": 19, "province_name_th": "สระบุรี", "province_name_en": "Saraburi", "region": "ภาคกลาง", "lat": 14.5289, "lon": 100.9101, "base_gpp": 260000},
    {"province_code": 60, "province_name_th": "นครสวรรค์", "province_name_en": "Nakhon Sawan", "region": "ภาคกลาง", "lat": 15.6930, "lon": 100.1226, "base_gpp": 130000},
    {"province_code": 61, "province_name_th": "อุทัยธานี", "province_name_en": "Uthai Thani", "region": "ภาคกลาง", "lat": 15.3835, "lon": 100.0245, "base_gpp": 36000},
    {"province_code": 73, "province_name_th": "นครปฐม", "province_name_en": "Nakhon Pathom", "region": "ภาคกลาง", "lat": 13.8196, "lon": 100.0601, "base_gpp": 370000},
    {"province_code": 74, "province_name_th": "สมุทรสาคร", "province_name_en": "Samut Sakhon", "region": "ภาคกลาง", "lat": 13.5475, "lon": 100.2744, "base_gpp": 430000},
    {"province_code": 75, "province_name_th": "สมุทรสงคราม", "province_name_en": "Samut Songkhram", "region": "ภาคกลาง", "lat": 13.4098, "lon": 99.9989, "base_gpp": 29000},
    {"province_code": 26, "province_name_th": "นครนายก", "province_name_en": "Nakhon Nayok", "region": "ภาคกลาง", "lat": 14.2069, "lon": 101.2131, "base_gpp": 34000},
    {"province_code": 66, "province_name_th": "พิจิตร", "province_name_en": "Phichit", "region": "ภาคกลาง", "lat": 16.4429, "lon": 100.3499, "base_gpp": 54000},
    {"province_code": 65, "province_name_th": "พิษณุโลก", "province_name_en": "Phitsanulok", "region": "ภาคกลาง", "lat": 16.8211, "lon": 100.2659, "base_gpp": 115000},
    {"province_code": 67, "province_name_th": "เพชรบูรณ์", "province_name_en": "Phetchabun", "region": "ภาคกลาง", "lat": 16.4190, "lon": 101.1573, "base_gpp": 95000},
    {"province_code": 62, "province_name_th": "กำแพงเพชร", "province_name_en": "Kamphaeng Phet", "region": "ภาคกลาง", "lat": 16.4828, "lon": 99.5227, "base_gpp": 125000},
    {"province_code": 64, "province_name_th": "สุโขทัย", "province_name_en": "Sukhothai", "region": "ภาคกลาง", "lat": 17.0078, "lon": 99.8234, "base_gpp": 62000},
    {"province_code": 72, "province_name_th": "สุพรรณบุรี", "province_name_en": "Suphan Buri", "region": "ภาคกลาง", "lat": 14.4745, "lon": 100.1177, "base_gpp": 102000},

    # Eastern Region (ภาคตะวันออก)
    {"province_code": 20, "province_name_th": "ชลบุรี", "province_name_en": "Chon Buri", "region": "ภาคตะวันออก", "lat": 13.3611, "lon": 100.9847, "base_gpp": 1100000},
    {"province_code": 21, "province_name_th": "ระยอง", "province_name_en": "Rayong", "region": "ภาคตะวันออก", "lat": 12.6815, "lon": 101.2816, "base_gpp": 1050000},
    {"province_code": 22, "province_name_th": "จันทบุรี", "province_name_en": "Chanthaburi", "region": "ภาคตะวันออก", "lat": 12.6114, "lon": 102.1039, "base_gpp": 160000},
    {"province_code": 23, "province_name_th": "ตราด", "province_name_en": "Trat", "region": "ภาคตะวันออก", "lat": 12.2428, "lon": 102.5175, "base_gpp": 53000},
    {"province_code": 24, "province_name_th": "ฉะเชิงเทรา", "province_name_en": "Chachoengsao", "region": "ภาคตะวันออก", "lat": 13.6904, "lon": 101.0780, "base_gpp": 380000},
    {"province_code": 25, "province_name_th": "ปราจีนบุรี", "province_name_en": "Prachin Buri", "region": "ภาคตะวันออก", "lat": 14.0510, "lon": 101.3734, "base_gpp": 320000},
    {"province_code": 27, "province_name_th": "สระแก้ว", "province_name_en": "Sa Kaeo", "region": "ภาคตะวันออก", "lat": 13.8140, "lon": 102.0722, "base_gpp": 72000},

    # Northern Region (ภาคเหนือ)
    {"province_code": 50, "province_name_th": "เชียงใหม่", "province_name_en": "Chiang Mai", "region": "ภาคเหนือ", "lat": 18.7883, "lon": 98.9853, "base_gpp": 265000},
    {"province_code": 51, "province_name_th": "ลำพูน", "province_name_en": "Lamphun", "region": "ภาคเหนือ", "lat": 18.5745, "lon": 99.0087, "base_gpp": 91000},
    {"province_code": 52, "province_name_th": "ลำปาง", "province_name_en": "Lampang", "region": "ภาคเหนือ", "lat": 18.2888, "lon": 99.4928, "base_gpp": 77000},
    {"province_code": 53, "province_name_th": "อุตรดิตถ์", "province_name_en": "Uttaradit", "region": "ภาคเหนือ", "lat": 17.6201, "lon": 100.0993, "base_gpp": 43000},
    {"province_code": 54, "province_name_th": "แพร่", "province_name_en": "Phrae", "region": "ภาคเหนือ", "lat": 18.1446, "lon": 100.1411, "base_gpp": 34000},
    {"province_code": 55, "province_name_th": "น่าน", "province_name_en": "Nan", "region": "ภาคเหนือ", "lat": 18.7838, "lon": 100.7782, "base_gpp": 37000},
    {"province_code": 56, "province_name_th": "พะเยา", "province_name_en": "Phayao", "region": "ภาคเหนือ", "lat": 19.1664, "lon": 99.9022, "base_gpp": 40000},
    {"province_code": 57, "province_name_th": "เชียงราย", "province_name_en": "Chiang Rai", "region": "ภาคเหนือ", "lat": 19.9105, "lon": 99.8406, "base_gpp": 120000},
    {"province_code": 58, "province_name_th": "แม่ฮ่องสอน", "province_name_en": "Mae Hong Son", "region": "ภาคเหนือ", "lat": 19.3020, "lon": 97.9654, "base_gpp": 16000},

    # Western Region (ภาคตะวันตก)
    {"province_code": 63, "province_name_th": "ตาก", "province_name_en": "Tak", "region": "ภาคตะวันตก", "lat": 16.8839, "lon": 99.1258, "base_gpp": 56000},
    {"province_code": 70, "province_name_th": "ราชบุรี", "province_name_en": "Ratchaburi", "region": "ภาคตะวันตก", "lat": 13.5283, "lon": 99.8134, "base_gpp": 195000},
    {"province_code": 71, "province_name_th": "กาญจนบุรี", "province_name_en": "Kanchanaburi", "region": "ภาคตะวันตก", "lat": 14.0228, "lon": 99.5328, "base_gpp": 115000},
    {"province_code": 76, "province_name_th": "เพชรบุรี", "province_name_en": "Phetchaburi", "region": "ภาคตะวันตก", "lat": 13.1110, "lon": 99.9398, "base_gpp": 77000},
    {"province_code": 77, "province_name_th": "ประจวบคีรีขันธ์", "province_name_en": "Prachuap Khiri Khan", "region": "ภาคตะวันตก", "lat": 11.8124, "lon": 99.7972, "base_gpp": 105000},

    # Southern Region (ภาคใต้)
    {"province_code": 80, "province_name_th": "นครศรีธรรมราช", "province_name_en": "Nakhon Si Thammarat", "region": "ภาคใต้", "lat": 8.4304, "lon": 99.9631, "base_gpp": 180000},
    {"province_code": 81, "province_name_th": "กระบี่", "province_name_en": "Krabi", "region": "ภาคใต้", "lat": 8.0863, "lon": 98.9063, "base_gpp": 105000},
    {"province_code": 82, "province_name_th": "พังงา", "province_name_en": "Phangnga", "region": "ภาคใต้", "lat": 8.4501, "lon": 98.5255, "base_gpp": 85000},
    {"province_code": 83, "province_name_th": "ภูเก็ต", "province_name_en": "Phuket", "region": "ภาคใต้", "lat": 7.8804, "lon": 98.3923, "base_gpp": 240000},
    {"province_code": 84, "province_name_th": "สุราษฎร์ธานี", "province_name_en": "Surat Thani", "region": "ภาคใต้", "lat": 9.1382, "lon": 99.3217, "base_gpp": 235000},
    {"province_code": 85, "province_name_th": "ระนอง", "province_name_en": "Ranong", "region": "ภาคใต้", "lat": 9.9658, "lon": 98.6348, "base_gpp": 31000},
    {"province_code": 86, "province_name_th": "ชุมพร", "province_name_en": "Chumphon", "region": "ภาคใต้", "lat": 10.4930, "lon": 99.1800, "base_gpp": 94000},
    {"province_code": 90, "province_name_th": "สงขลา", "province_name_en": "Songkhla", "region": "ภาคใต้", "lat": 7.1898, "lon": 100.5954, "base_gpp": 270000},
    {"province_code": 91, "province_name_th": "สตูล", "province_name_en": "Satun", "region": "ภาคใต้", "lat": 6.6238, "lon": 100.0674, "base_gpp": 38000},
    {"province_code": 92, "province_name_th": "ตรัง", "province_name_en": "Trang", "region": "ภาคใต้", "lat": 7.5563, "lon": 99.6114, "base_gpp": 72000},
    {"province_code": 93, "province_name_th": "พัทลุง", "province_name_en": "Phatthalung", "region": "ภาคใต้", "lat": 7.6167, "lon": 100.0833, "base_gpp": 43000},
    {"province_code": 94, "province_name_th": "ปัตตานี", "province_name_en": "Pattani", "region": "ภาคใต้", "lat": 6.8671, "lon": 101.2501, "base_gpp": 53000},
    {"province_code": 95, "province_name_th": "ยะลา", "province_name_en": "Yala", "region": "ภาคใต้", "lat": 6.5411, "lon": 101.2813, "base_gpp": 48000},
    {"province_code": 96, "province_name_th": "นราธิวาส", "province_name_en": "Narathiwat", "region": "ภาคใต้", "lat": 6.4255, "lon": 101.8253, "base_gpp": 47000},

    # Northeastern Region (ภาคตะวันออกเฉียงเหนือ)
    {"province_code": 30, "province_name_th": "นครราชสีมา", "province_name_en": "Nakhon Ratchasima", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 14.9799, "lon": 102.0978, "base_gpp": 320000},
    {"province_code": 31, "province_name_th": "บุรีรัมย์", "province_name_en": "Buri Ram", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 14.9930, "lon": 103.1029, "base_gpp": 105000},
    {"province_code": 32, "province_name_th": "สุรินทร์", "province_name_en": "Surin", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 14.8818, "lon": 103.4936, "base_gpp": 88000},
    {"province_code": 33, "province_name_th": "ศรีสะเกษ", "province_name_en": "Si Sa Ket", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 15.1186, "lon": 104.3220, "base_gpp": 82000},
    {"province_code": 34, "province_name_th": "อุบลราชธานี", "province_name_en": "Ubon Ratchathani", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 15.2448, "lon": 104.8473, "base_gpp": 135000},
    {"province_code": 35, "province_name_th": "ยโสธร", "province_name_en": "Yasothon", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 15.7926, "lon": 104.1451, "base_gpp": 33000},
    {"province_code": 36, "province_name_th": "ชัยภูมิ", "province_name_en": "Chaiyaphum", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 15.8080, "lon": 102.0317, "base_gpp": 74000},
    {"province_code": 37, "province_name_th": "อำนาจเจริญ", "province_name_en": "Amnat Charoen", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 15.8584, "lon": 104.6298, "base_gpp": 23000},
    {"province_code": 38, "province_name_th": "บึงกาฬ", "province_name_en": "Bueng Kan", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 18.3626, "lon": 103.6529, "base_gpp": 29000},
    {"province_code": 39, "province_name_th": "หนองบัวลำภู", "province_name_en": "Nong Bua Lam Phu", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 17.2039, "lon": 102.4407, "base_gpp": 32000},
    {"province_code": 40, "province_name_th": "ขอนแก่น", "province_name_en": "Khon Kaen", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 16.4419, "lon": 102.8360, "base_gpp": 230000},
    {"province_code": 41, "province_name_th": "อุดรธานี", "province_name_en": "Udon Thani", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 17.4138, "lon": 102.7872, "base_gpp": 130000},
    {"province_code": 42, "province_name_th": "เลย", "province_name_en": "Loei", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 17.4860, "lon": 101.7223, "base_gpp": 61000},
    {"province_code": 43, "province_name_th": "หนองคาย", "province_name_en": "Nong Khai", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 17.8783, "lon": 102.7420, "base_gpp": 46000},
    {"province_code": 44, "province_name_th": "มหาสารคาม", "province_name_en": "Maha Sarakham", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 16.1852, "lon": 103.3007, "base_gpp": 65000},
    {"province_code": 45, "province_name_th": "ร้อยเอ็ด", "province_name_en": "Roi Et", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 16.0538, "lon": 103.6520, "base_gpp": 86000},
    {"province_code": 46, "province_name_th": "กาฬสินธุ์", "province_name_en": "Kalasin", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 16.4322, "lon": 103.5065, "base_gpp": 64000},
    {"province_code": 47, "province_name_th": "สกลนคร", "province_name_en": "Sakon Nakhon", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 17.1612, "lon": 104.1473, "base_gpp": 70000},
    {"province_code": 48, "province_name_th": "นครพนม", "province_name_en": "Nakhon Phanom", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 17.3998, "lon": 104.7695, "base_gpp": 53000},
    {"province_code": 49, "province_name_th": "มุกดาหาร", "province_name_en": "Mukdahan", "region": "ภาคตะวันออกเฉียงเหนือ", "lat": 16.5436, "lon": 104.7235, "base_gpp": 31000},
]

def get_dim_province() -> pd.DataFrame:
    """Returns the dimension table for Thailand provinces (dim_province)"""
    return pd.DataFrame(PROVINCES_DATA)

def get_dim_date(start_year: int = 2019, end_year: int = 2024) -> pd.DataFrame:
    """Returns the dimension table for Dates (dim_date)"""
    dates = []
    month_names_th = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                      "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    month_names_en = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
    
    date_id = 1
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            quarter = (month - 1) // 3 + 1
            season = "High Season" if month in [11, 12, 1, 2] else ("Shoulder Season" if month in [3, 4, 7, 8] else "Low Season")
            dates.append({
                "date_id": date_id,
                "year": year,
                "year_th": year + 543,
                "month": month,
                "month_name_th": month_names_th[month - 1],
                "month_name_en": month_names_en[month - 1],
                "quarter": f"Q{quarter}",
                "season": season,
                "period_str": f"{year}-{month:02d}",
            })
            date_id += 1
    return pd.DataFrame(dates)

def get_dim_visitor_type() -> pd.DataFrame:
    """Returns the visitor type dimension (dim_visitor_type)"""
    return pd.DataFrame([
        {"visitor_type_id": 1, "visitor_type_code": "ALL", "visitor_type_th": "ผู้เยี่ยมเยือนทั้งหมด", "visitor_type_en": "Total Visitors"},
        {"visitor_type_id": 2, "visitor_type_code": "DOMESTIC", "visitor_type_th": "ชาวไทย (Domestic)", "visitor_type_en": "Thai Domestic"},
        {"visitor_type_id": 3, "visitor_type_code": "FOREIGN", "visitor_type_th": "ชาวต่างชาติ (International)", "visitor_type_en": "Foreign International"},
    ])
