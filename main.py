import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from geocoder import Geocoder
from horoscope import HoroscopeCalculator

app = FastAPI(title="Astrology Cusp Calculator")

# Instantiate classes
geocoder = Geocoder()

class CalculationRequest(BaseModel):
    birth_date: str
    birth_time: str
    birth_place: str
    house_system: str = "P"

@app.get("/")
async def get_index():
    index_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h3>index.html not found</h3>", status_code=404)

@app.post("/api/calculate")
async def calculate_cusps(req: CalculationRequest):
    try:
        # 1. Geocode
        geo_result = geocoder.geocode(req.birth_place)
        lat = geo_result["latitude"]
        lon = geo_result["longitude"]
        display_name = geo_result["display_name"]
        
        # 2. Get Timezone
        timezone_str = geocoder.get_timezone(lat, lon)
        
        # 3. Calculate Cusps
        cusps_data = HoroscopeCalculator.calculate_houses(
            birth_date_str=req.birth_date,
            birth_time_str=req.birth_time,
            latitude=lat,
            longitude=lon,
            timezone_str=timezone_str,
            house_system=req.house_system
        )
        
        # Combine response
        response_data = {
            "status": "success",
            "resolved_location": {
                "display_name": display_name,
                "latitude": lat,
                "longitude": lon,
                "timezone": timezone_str
            },
            "data": cusps_data
        }
        return response_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内部エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
