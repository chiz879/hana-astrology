import swisseph as swe
from datetime import datetime
import pytz

ZODIAC_SIGNS_JP = [
    "牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座",
    "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"
]

def format_degree(decimal_degree: float) -> str:
    """
    360度表記の浮動小数点を「星座名 度°分'秒\"」の形式に変換します。
    """
    normalized_degree = decimal_degree % 360.0
    sign_index = int(normalized_degree // 30)
    sign_name = ZODIAC_SIGNS_JP[sign_index]
    
    sign_degree = normalized_degree % 30.0
    degrees = int(sign_degree)
    
    minutes_float = (sign_degree - degrees) * 60.0
    minutes = int(minutes_float)
    
    seconds_float = (minutes_float - minutes) * 60.0
    seconds = int(seconds_float)
    
    return f"{sign_name} {degrees:02d}°{minutes:02d}'{seconds:02d}\""

class HoroscopeCalculator:
    @staticmethod
    def calculate_houses(birth_date_str: str, birth_time_str: str, latitude: float, longitude: float, timezone_str: str, house_system: str = "P"):
        """
        指定されたパラメータからハウスのカスプ、ASC、MCを計算します。
        
        :param birth_date_str: "YYYY-MM-DD"形式
        :param birth_time_str: "HH:MM"形式
        :param latitude: 緯度
        :param longitude: 経度
        :param timezone_str: IANAタイムゾーン（例: "Asia/Tokyo"）
        :param house_system: ハウス分割方式のコード（"P" = Placidus, "K" = Koch, "E" = Equal, "W" = Whole Sign 等）
        """
        # ローカル日時のパース
        local_dt_str = f"{birth_date_str} {birth_time_str}"
        local_dt = datetime.strptime(local_dt_str, "%Y-%m-%d %H:%M")
        
        # タイムゾーンの適用とUTCへの変換
        tz = pytz.timezone(timezone_str)
        localized_dt = tz.localize(local_dt)
        utc_dt = localized_dt.astimezone(pytz.utc)
        
        # 10進法表記のUTC時間を計算
        decimal_hour = utc_dt.hour + (utc_dt.minute / 60.0) + (utc_dt.second / 3600.0)
        
        # ユリウス日の計算
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, decimal_hour)
        
        # ハウスシステムをバイト列に変換
        hsys_byte = house_system.encode('utf-8')
        
        # ハウスの計算
        cusps, ascmc = swe.houses(jd_ut, latitude, longitude, hsys_byte)
        
        # 結果の整形
        formatted_cusps = []
        for i, cusp in enumerate(cusps):
            formatted_cusps.append({
                "house": i + 1,
                "degree": cusp,
                "formatted": format_degree(cusp)
            })
            
        return {
            "asc": {
                "degree": ascmc[0],
                "formatted": format_degree(ascmc[0])
            },
            "mc": {
                "degree": ascmc[1],
                "formatted": format_degree(ascmc[1])
            },
            "cusps": formatted_cusps,
            "metadata": {
                "julian_day": jd_ut,
                "utc_datetime": utc_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "house_system": house_system
            }
        }

# 簡単なテスト用コード
if __name__ == "__main__":
    calc = HoroscopeCalculator()
    # 東京 2000-01-01 12:00
    res = calc.calculate_houses("2000-01-01", "12:00", 35.6762, 139.6503, "Asia/Tokyo", "P")
    print("ASC:", res["asc"]["formatted"])
    print("MC:", res["mc"]["formatted"])
    for c in res["cusps"]:
        print(f"House {c['house']}: {c['formatted']}")
