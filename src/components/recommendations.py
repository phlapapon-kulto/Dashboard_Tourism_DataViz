"""
Travel Recommendation Component & Data Catalog
Provides curated destinations, images, and recommendation logic for Thailand's top provinces.
Calculated dynamically from real dashboard visitor data.
"""

from typing import Dict, Any, List
import pandas as pd
import streamlit as st

# Curated metadata dictionary for Thai tourism destinations
DESTINATION_CATALOG: Dict[str, Dict[str, Any]] = {
    "กรุงเทพมหานคร": {
        "en_name": "Bangkok",
        "image_url": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / Tourism Authority of Thailand",
        "attractions": [
            "วัดพระศรีรัตนศาสดาราม (วัดพระแก้ว) & พระบรมมหาราชวัง",
            "วัดอรุณราชวรารามราชวรมหาวิหาร (ริมแม่น้ำเจ้าพระยา)",
            "ตลาดนัดจตุจักร & สตรีทฟู้ดเยาวราช",
            "พิพิธภัณฑ์ศิลปะร่วมสมัย (MOCA Bangkok)"
        ],
        "why_visit": "ศูนย์กลางมหานครระดับโลก ผสมผสานศิลปวัฒนธรรม มรดกทางประวัติศาสตร์ แหล่งช้อปปิ้ง และสตรีทฟู้ดระดับมิชลินที่คึกคักตลอดทั้งปี",
        "best_season": "พฤศจิกายน – กุมภาพันธ์ (อากาศเย็นสบาย เดินเที่ยวสะดวก)",
        "travel_style": "City Tour, Cultural Heritage, Gastronomy, MICE"
    },
    "ชลบุรี": {
        "en_name": "Chon Buri (Pattaya)",
        "image_url": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Chonburi",
        "attractions": [
            "ปราสาทสัจธรรม (Sanctuary of Truth)",
            "หาดพัทยา & ถนนคนเดิน Walking Street",
            "เกาะล้าน (Koh Lan) หาดตาแหวน",
            "สวนนงนุชพัทยา & สวนน้ำรามายณะ"
        ],
        "why_visit": "เมืองตากอากาศชายทะเลระดับนานาชาติที่เดินทางสะดวกจากกรุงเทพฯ ครบครันด้วยกิจกรรมทางน้ำ รีสอร์ตหรู และความบันเทิงระดับโลก",
        "best_season": "พฤศจิกายน – เมษายน (คลื่นลมสงบ น้ำทะเลใส เหมาะแก่การดำน้ำ)",
        "travel_style": "Beach Vacation, Entertainment, Family Leisure, Water Sports"
    },
    "ภูเก็ต": {
        "en_name": "Phuket",
        "image_url": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / Phuket Tourism Portal",
        "attractions": [
            "แหลมพรหมเทพ (จุดชมพระอาทิตย์ตกชื่อดัง)",
            "ย่านเมืองเก่าภูเก็ต (Phuket Old Town สถาปัตยกรรมชิโน-โปรตุกีส)",
            "หาดป่าตอง, หาดกะตะ, หาดกะรน",
            "พระพุทธมิ่งมงคลเอกนาคคีรี (พระใหญ่เขานาคเกิด)"
        ],
        "why_visit": "ไข่มุกแห่งอันดามัน โดดเด่นด้วยการท่องเที่ยวแบบ High-Yield ชายหาดระดับเวิลด์คลาส อาหารพื้นเมืองได้รับการยกย่องเป็น UNESCO City of Gastronomy",
        "best_season": "ธันวาคม – มีนาคม (ทะเลอันดามันฟ้าใส ไร้มรสุม คลื่นนิ่งสวยงาม)",
        "travel_style": "Island Luxury, Yachting, Gastronomy, Heritage Walk"
    },
    "เชียงใหม่": {
        "en_name": "Chiang Mai",
        "image_url": "https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Northern Region",
        "attractions": [
            "วัดพระธาตุดอยสุเทพราชวรวิหาร",
            "อุทยานแห่งชาติดอยอินทนนท์ (จุดสูงสุดแดนสยาม)",
            "ถนนคนเดินท่าแพ & ชุมชนหัตถกรรมบ้านข้างวัด",
            "ม่อนแจ่ม & โครงการหลวงแม่กำปอง"
        ],
        "why_visit": "ศูนย์กลางอารยธรรมล้านนา โอบล้อมด้วยขุนเขาธรรมชาติ คาเฟ่ฮิป ชุมชนหัตถกรรมสร้างสรรค์ และสภาพอากาศหนาวเย็นสบายในฤดูหนาว",
        "best_season": "พฤศจิกายน – กุมภาพันธ์ (ฤดูหนาว ดอกนางพญาเสือโคร่งบาน ทะเลหมอก)",
        "travel_style": "Eco Tourism, Wellness, Lanna Culture, Mountain Trekking"
    },
    "กาญจนบุรี": {
        "en_name": "Kanchanaburi",
        "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Kanchanaburi",
        "attractions": [
            "สะพานข้ามแม่น้ำแคว & ทางรถไฟสายมรณะ",
            "น้ำตกเอราวัณ 7 ชั้น มรกตแห่งผืนป่าตะวันตก",
            "สังขละบุรี สะพานมอญ & เมืองบาดาล",
            "ช่องเขาขาด & น้ำตกไทรโยคใหญ่"
        ],
        "why_visit": "ปลายทางยอดนิยมสำหรับนักท่องเที่ยวชาวไทยที่รักธรรมชาติและประวัติศาสตร์ พักผ่อนบนแพริมน้ำ สัมผัสวิถีพหุวัฒนธรรมไทย-มอญ",
        "best_season": "ตุลาคม – กุมภาพันธ์ (อากาศเย็น สายนทีใสสะอาด ป่าไม้เขียวชอุ่ม)",
        "travel_style": "Nature Escape, River Rafting, Historic Trails, Cultural Immersion"
    },
    "สุราษฎร์ธานี": {
        "en_name": "Surat Thani",
        "image_url": "https://images.unsplash.com/photo-1537956965359-7573183d1f57?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Surat Thani",
        "attractions": [
            "เกาะสมุย (Koh Samui) & เกาะพะงัน (Koh Phangan)",
            "เกาะเต่า & เกาะนางยวน (แหล่งดำน้ำระดับโลก)",
            "อุทยานแห่งชาติเขาสก & เขื่อนรัชชประภา (กุ้ยหลินเมืองไทย)",
            "อุทยานแห่งชาติหมู่เกาะอ่างทอง"
        ],
        "why_visit": "เมืองร้อยเกาะ เงาะอร่อย หอยใหญ่ ครบทั้งเกาะระดับโลกและผืนป่าดึกดำบรรพ์ เป็นแหล่งดำน้ำตื้นและลึกที่ติดอันดับเอเชีย",
        "best_season": "มกราคม – สิงหาคม (อ่าวไทยคลื่นลมสงบ น้ำทะเลใสแจ๋ว)",
        "travel_style": "Island Hopping, Scuba Diving, Rainforest Adventure, Full Moon Fest"
    },
    "กระบี่": {
        "en_name": "Krabi",
        "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Krabi",
        "attractions": [
            "อ่าวไร่เลย์ & หาดถ้ำพระนาง (ผาหินปูนปีนผาระดับโลก)",
            "หมู่เกาะพีพี (เกาะพีพีดอน & อ่าวมาหยา)",
            "สระมรกต & น้ำตกร้อนคลองท่อม",
            "เกาะห้อง & ทะเลแหวก"
        ],
        "why_visit": "เมืองมรดกธรรมชาติที่มีความงามระดับตำนาน โดดเด่นด้วยเขาหินปูนตระหง่านกลางทะเลอันดามัน เหมาะสำหรับการปีนผาและพักผ่อนเชิงอนุรักษ์",
        "best_season": "พฤศจิกายน – เมษายน (ทะเลราบเรียบ ปะการังสมบูรณ์)",
        "travel_style": "Rock Climbing, Marine Eco-Tour, Luxury Hideaway"
    },
    "นครราชสีมา": {
        "en_name": "Nakhon Ratchasima (Khao Yai)",
        "image_url": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Nakhon Ratchasima",
        "attractions": [
            "อุทยานแห่งชาติเขาใหญ่ (มรดกโลกดงพญาเย็น-เขาใหญ่)",
            "อุทยานประวัติศาสตร์พิมาย (ปราสาทหินขอมโบราณ)",
            "อนุสาวรีย์ท้าวสุรนารี (ย่าโม)",
            "ไร่องุ่นพีบีวัลเล่ย์ & ฟาร์มโชคชัย"
        ],
        "why_visit": "ประตูสู่อีสาน แหล่งโอโซนบริสุทธิ์อันดับต้นของโลก เพลิดเพลินกับไวน์เนอรี่ ส่องสัตว์ยามค่ำคืน และสถาปัตยกรรมขอมโบราณ",
        "best_season": "พฤศจิกายน – กุมภาพันธ์ (อากาศหนาวเย็น สัมผัสทุ่งหญ้าและลมหนาว)",
        "travel_style": "Wildlife Safari, Agro-Tourism, Heritage, Glamping"
    },
    "สงขลา": {
        "en_name": "Songkhla (Hat Yai)",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Songkhla",
        "attractions": [
            "หาดสมิหลา & รูปปั้นนางเงือกทอง",
            "ย่านเมืองเก่าสงขลา ถนนนางงาม (Street Art)",
            "ตลาดกิมหยง หาดใหญ่ & กระเช้าลอยฟ้าเขาคอหงส์",
            "มัสยิดกลางประจำจังหวัดสงขลา (ทัชมาฮาลเมืองไทย)"
        ],
        "why_visit": "ศูนย์กลางการค้าและพหุวัฒนธรรมชายแดนใต้ แหล่งช้อปปิ้งของฝากเลื่องชื่อ สตรีทอาร์ตและอาหารพื้นถิ่นปักษ์ใต้รสเข้มข้น",
        "best_season": "กุมภาพันธ์ – กันยายน (ปลอดมรสุม)",
        "travel_style": "Cross-Border Shopping, Heritage Walk, Culinary Exploration"
    },
    "ประจวบคีรีขันธ์": {
        "en_name": "Prachuap Khiri Khan (Hua Hin)",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Prachuap",
        "attractions": [
            "ชายหาดหัวหิน & สถานีรถไฟหัวหิน",
            "อุทยานแห่งชาติเขาสามร้อยยอด (ถ้ำพระยานคร)",
            "อ่าวมะนาว & เขาช่องกระจก",
            "ตลาดโต้รุ่งหัวหิน & ตลาดซิเคด้า (Cicada Market)"
        ],
        "why_visit": "เมืองตากอากาศคลาสสิกระดับพรีเมียม สัมผัสบรรยากาศความสงบเงียบ ชายหาดทอดยาว เหมาะกับครอบครัวและการพักผ่อนระยะยาว",
        "best_season": "ธันวาคม – พฤษภาคม (ลมเย็น ทะเลสงบ อากาศปลอดโปร่ง)",
        "travel_style": "Classic Seaside, Family Wellness, Cave Exploration"
    },
    "พระนครศรีอยุธยา": {
        "en_name": "Phra Nakhon Si Ayutthaya",
        "image_url": "https://images.unsplash.com/photo-1598971861713-54ad16a7e72e?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Ayutthaya",
        "attractions": [
            "อุทยานประวัติศาสตร์พระนครศรีอยุธยา (มรดกโลก UNESCO)",
            "วัดมหาธาตุ (เศียรพระพุทธรูปในรากไม้โพธิ์)",
            "วัดไชยวัฒนาราม (ริมแม่น้ำเจ้าพระยา)",
            "ตลาดน้ำอโยธยา & ชิมกุ้งแม่น้ำเผาชื่อดัง"
        ],
        "why_visit": "อดีตราชธานี 417 ปี สัมผัสความรุ่งเรืองของมรดกโลกทางวัฒนธรรม ล่องเรือชมโบราณสถานยามค่ำคืน และลิ้มลองโรตีสายไหมและกุ้งแม่น้ำ",
        "best_season": "พฤศจิกายน – กุมภาพันธ์ (อากาศไม่ร้อน เดินชมโบราณสถานสบาย)",
        "travel_style": "Historical Heritage, Cultural Day-Trip, Riverside Dining"
    },
    "เชียงราย": {
        "en_name": "Chiang Rai",
        "image_url": "https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Chiang Rai",
        "attractions": [
            "วัดร่องขุ่น (White Temple ออกแบบโดย อ.เฉลิมชัย)",
            "สิงห์ปาร์ค (Singha Park Chiang Rai)",
            "ภูชี้ฟ้า & ดอยแม่สลอง (ไร่ชาชาชุ่มฉ่ำ)",
            "วัดร่องเสือเต้น (Blue Temple)"
        ],
        "why_visit": "ดินแดนเหนือสุดแห่งสยาม อุดมด้วยพุทธศิลป์ร่วมสมัยตระการตา ไร่ชาขั้นบันไดบนยอดดอยสูง และทะเลหมอกรับลมหนาว",
        "best_season": "พฤศจิกายน – มกราคม (อากาศหนาวเย็น ชมดอกไม้เมืองหนาวและทะเลหมอก)",
        "travel_style": "Art & Contemporary Culture, Mountain Vista, Tea Plantation"
    },
    "น่าน": {
        "en_name": "Nan",
        "image_url": "https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=800&q=80",
        "image_credit": "Unsplash / TAT Nan",
        "attractions": [
            "วัดภูมินทร์ (ภาพจิตรกรรมกระซิบรักบันลือโลก ปู่ม่านย่าม่าน)",
            "ถนนคนเดินเมืองน่าน & วัดพระธาตุแช่แห้ง",
            "อำเภอปัว ทุ่งนาเขียวขจี & ดอยเสมอดาว",
            "บ่อเกลือโบราณสินเธาว์ภูเขา"
        ],
        "why_visit": "เมืองสโลว์ไลฟ์อันเงียบสงบ มนต์เสน่ห์ล้านนาตะวันออก ผู้คนเป็นมิตร เหมาะสำหรับนักท่องเที่ยวที่แสวงหาความสงบและธรรมชาติบริสุทธิ์",
        "best_season": "กรกฎาคม – กุมภาพันธ์ (ฤดูฝนทุ่งนาเขียวสดชื่น และฤดูหนาวทะเลหมอกสวยงาม)",
        "travel_style": "Slow Life, Creative Community, Lanna Romance, Nature"
    }
}

# Fallback generator for other provinces
def get_province_destination_meta(province_name_th: str, province_name_en: str, region: str) -> Dict[str, Any]:
    if province_name_th in DESTINATION_CATALOG:
        return DESTINATION_CATALOG[province_name_th]
    
    # Regional generic fallbacks
    regional_images = {
        "ภาคเหนือ": "https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=800&q=80",
        "ภาคใต้": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?auto=format&fit=crop&w=800&q=80",
        "ภาคกลาง": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=800&q=80",
        "ภาคตะวันออก": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80",
        "ภาคตะวันตก": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?auto=format&fit=crop&w=800&q=80",
        "ภาคตะวันออกเฉียงเหนือ": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=800&q=80"
    }
    
    return {
        "en_name": province_name_en,
        "image_url": regional_images.get(region, "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=800&q=80"),
        "image_credit": f"Unsplash / Tourism Authority of Thailand ({region})",
        "attractions": [
            f"อุทยานแห่งชาติและจุดชมวิวธรรมชาติประจำจังหวัด{province_name_th}",
            f"วัดพระอารามหลวงและศูนย์รวมจิตใจชาว{province_name_th}",
            f"ตลาดวัฒนธรรมและถนนคนเดินท้องถิ่น",
            f"ชุมชนท่องเที่ยวเชิงเกษตรและภูมิปัญญาท้องถิ่น"
        ],
        "why_visit": f"สัมผัสเอกลักษณ์วิถีชีวิต ศิลปวัฒนธรรมท้องถิ่น และความงดงามทางธรรมชาติของ{province_name_th} ({region}) ปลายทางเมืองน่าเที่ยวที่รอให้ค้นหา",
        "best_season": "พฤศจิกายน – กุมภาพันธ์ (ช่วงฤดูท่องเที่ยวของไทย)",
        "travel_style": "Local Life, Nature Discovery, Culture, Community Tourism"
    }

def get_top5_recommended_provinces(df_filtered: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Computes Top 5 provinces with highest visitor volume strictly from the filtered dataset.
    Never hardcoded or random!
    """
    agg = df_filtered.groupby([
        "province_code", "province_name_th", "province_name_en", "region"
    ]).agg({
        "total_tourists": "sum",
        "total_revenue": "sum",
        "foreign_tourists": "sum",
        "thai_tourists": "sum",
        "occupancy_rate": "mean"
    }).reset_index()

    # Sort descending by total tourists
    top5_df = agg.sort_values(by="total_tourists", ascending=False).head(5).reset_index(drop=True)

    recommendations = []
    for rank, row in top5_df.iterrows():
        name_th = row["province_name_th"]
        name_en = row["province_name_en"]
        region = row["region"]
        meta = get_province_destination_meta(name_th, name_en, region)
        
        yield_baht = round((row["total_revenue"] * 1_000_000) / max(1, row["total_tourists"]), 0)
        foreign_pct = round((row["foreign_tourists"] / max(1, row["total_tourists"])) * 100, 1)

        recommendations.append({
            "rank": rank + 1,
            "province_name_th": name_th,
            "province_name_en": name_en,
            "region": region,
            "total_tourists": row["total_tourists"],
            "total_revenue": row["total_revenue"],
            "yield_baht": yield_baht,
            "foreign_pct": foreign_pct,
            "occupancy_rate": round(row["occupancy_rate"], 1),
            "meta": meta
        })

    return recommendations
