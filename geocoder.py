import requests
import urllib.parse
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

class Geocoder:
    def __init__(self):
        self.tf = TimezoneFinder()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def geocode(self, address: str):
        """
        Geocode an address into latitude and longitude using OpenStreetMap Nominatim.
        """
        if not address or not address.strip():
            raise ValueError("住所を入力してください。")

        encoded_address = urllib.parse.quote(address.strip())
        url = f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=json&limit=1"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise ValueError(f"「{address}」の位置情報を特定できませんでした。")
                
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            display_name = data[0]["display_name"]
            
            return {
                "latitude": lat,
                "longitude": lon,
                "display_name": display_name
            }
        except requests.exceptions.RequestException as e:
            # If network error or API rate-limited, raise a clear error
            raise RuntimeError(f"位置情報の取得中にネットワークエラーが発生しました: {e}")

    def get_timezone(self, latitude: float, longitude: float) -> str:
        """
        Get the IANA timezone string for a given coordinate.
        """
        timezone_str = self.tf.timezone_at(lng=longitude, lat=latitude)
        if not timezone_str:
            # Fallback if coordinate is in the ocean / international waters
            return "UTC"
        return timezone_str

    def get_utc_offset(self, timezone_str: str, local_dt: datetime) -> float:
        """
        Get UTC offset in hours for a specific local datetime in a timezone.
        Accounts for Daylight Saving Time (DST).
        """
        try:
            tz = pytz.timezone(timezone_str)
            # Localize the naive datetime to the target timezone
            # is_dst=None will raise AmbiguousTimeError or NonExistentTimeError if there is an issue,
            # so we use is_dst=False/True or localize with error handling.
            localized_dt = tz.localize(local_dt, is_dst=None)
            offset_seconds = localized_dt.utcoffset().total_seconds()
            return offset_seconds / 3600.0
        except Exception:
            # If there's an issue with localization (e.g. non-existent DST hour),
            # fallback to a simpler method
            tz = pytz.timezone(timezone_str)
            localized_dt = tz.localize(local_dt)
            offset_seconds = localized_dt.utcoffset().total_seconds()
            return offset_seconds / 3600.0

# Example usage
if __name__ == "__main__":
    geocoder = Geocoder()
    try:
        location = geocoder.geocode("Tokyo")
        print("Location:", location)
        tz = geocoder.get_timezone(location["latitude"], location["longitude"])
        print("Timezone:", tz)
        dt = datetime(2000, 1, 1, 12, 0, 0)
        offset = geocoder.get_utc_offset(tz, dt)
        print("UTC Offset at 2000-01-01 12:00 :", offset)
    except Exception as e:
        print("Error:", e)
