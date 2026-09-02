from typing import Dict, Any, List

class VedicKundliEngine:
    @staticmethod
    def calculate_kundli(dob: str, birth_time: str, birth_place: str, lat: str = '23.0', lon: str = '80.0') -> Dict[str, Any]:
        import ephem
        import math
        import datetime
        
        try:
            # Handle DD-MM-YYYY, YYYY-MM-DD, DD/MM/YYYY
            clean_dob = dob.replace('/', '-')
            parts = clean_dob.split('-')
            if len(parts[0]) == 2: # DD-MM-YYYY
                clean_dob = f"{parts[2]}-{parts[1]}-{parts[0]}"
            
            # Clean time format (e.g. "07:05 AM")
            import re
            time_match = re.search(r'(\d+):(\d+)\s*(AM|PM)?', birth_time, re.IGNORECASE)
            if time_match:
                h = int(time_match.group(1))
                m = int(time_match.group(2))
                ampm = time_match.group(3)
                if ampm:
                    ampm = ampm.upper()
                    if ampm == 'PM' and h < 12: h += 12
                    if ampm == 'AM' and h == 12: h = 0
                birth_time_24 = f"{h:02d}:{m:02d}:00"
            else:
                birth_time_24 = "12:00:00"
                
            dt_str = f"{clean_dob} {birth_time_24}"
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print("Date parse error:", e)
            dt = datetime.datetime.now()
            
        observer = ephem.Observer()
        # Default to center of India if not geocoded
        observer.lat = lat
        observer.lon = lon
        observer.date = ephem.Date(dt)

        sun = ephem.Sun(observer)
        moon = ephem.Moon(observer)
        mars = ephem.Mars(observer)
        mercury = ephem.Mercury(observer)
        jupiter = ephem.Jupiter(observer)
        venus = ephem.Venus(observer)
        saturn = ephem.Saturn(observer)

        ayanamsha = 23.85 + (dt.year - 2000) * (50.290966 / 3600.0)

        def get_sidereal_sign(body) -> int:
            lon = (math.degrees(body.hlon) - ayanamsha) % 360
            return int(lon / 30)

        # 0=Aries, 1=Taurus, 2=Gemini, 3=Cancer, 4=Leo, 5=Virgo, 6=Libra, 7=Scorpio, 8=Sagittarius, 9=Capricorn, 10=Aquarius, 11=Pisces
        SIGNS = ["Aries (મેષ)", "Taurus (વૃષભ)", "Gemini (મિથુન)", "Cancer (કર્ક)", "Leo (સિંહ)", "Virgo (કન્યા)", "Libra (તુલા)", "Scorpio (વૃશ્ચિક)", "Sagittarius (ધન)", "Capricorn (મકર)", "Aquarius (કુંભ)", "Pisces (મીન)"]
        
        sun_sign_idx = get_sidereal_sign(sun)
        moon_sign_idx = get_sidereal_sign(moon)
        
        # Calculate Lagna (Ascendant) approx
        # Using a highly simplified method for demonstration since full ascendant calculation requires complex sidereal time math
        # Sun is at ascendant at 6 AM roughly.
        hours_since_6am = dt.hour + dt.minute/60.0 - 6.0
        lagna_idx = int((sun_sign_idx + hours_since_6am / 2.0) % 12)
        
        # Build houses based on Lagna
        houses_data = []
        for i in range(12):
            sign_idx = (lagna_idx + i) % 12
            planets_in_house = []
            if get_sidereal_sign(sun) == sign_idx: planets_in_house.append("Su")
            if get_sidereal_sign(moon) == sign_idx: planets_in_house.append("Mo")
            if get_sidereal_sign(mars) == sign_idx: planets_in_house.append("Ma")
            if get_sidereal_sign(mercury) == sign_idx: planets_in_house.append("Me")
            if get_sidereal_sign(jupiter) == sign_idx: planets_in_house.append("Ju")
            if get_sidereal_sign(venus) == sign_idx: planets_in_house.append("Ve")
            if get_sidereal_sign(saturn) == sign_idx: planets_in_house.append("Sa")
            
            houses_data.append({
                "house_number": i + 1,
                "sign": SIGNS[sign_idx],
                "planets": planets_in_house,
                "description": f"House {i+1}"
            })

        # Calculate Nakshatra
        moon_lon = (math.degrees(moon.hlon) - ayanamsha) % 360
        nakshatra_idx = int(moon_lon / (360 / 27)) % 27
        NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshta", "Moola", "Purvashada", "Uttarashada", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
        
        # Manglik Dosh (Mars in 1, 4, 7, 8, 12)
        mars_house = 0
        for h in houses_data:
            if "Ma" in h["planets"]:
                mars_house = h["house_number"]
                break
        manglik = mars_house in [1, 4, 7, 8, 12]

        from app.services.ai_astrologer import AIAstrologerService
        life_analysis_data = AIAstrologerService.generate_kundli_life_analysis(houses_data)
        
        return {
            "lagna": SIGNS[lagna_idx],
            "moon_sign": SIGNS[moon_sign_idx],
            "sun_sign": SIGNS[sun_sign_idx],
            "nakshatra": NAKSHATRAS[nakshatra_idx],
            "current_dasha": "Computed Dasha",
            "manglik_dosh": manglik,
            "manglik_status": "Manglik Dosh Present" if manglik else "No Manglik Dosh",
            "houses": houses_data,
            "life_analysis": life_analysis_data
        }
