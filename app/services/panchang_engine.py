import datetime
import math
from typing import Dict, Any, List

class VedicPanchangEngine:
    TITHIS_GU = [
        "શુક્લ પડવો (Pratipada)", "શુક્લ બીજ (Dwitiya)", "શુક્લ ત્રીજ (Tritiya)", "શુક્લ ચોથ (Chaturthi)",
        "શુક્લ પંચમી (Panchami)", "શુક્લ છઠ (Shashthi)", "શુક્લ સાતમ (Saptami)", "શુક્લ આઠમ (Ashtami)",
        "શુક્લ નોમ (Navami)", "શુક્લ દશમ (Dashami)", "શુક્લ અગિયારસ (Ekadashi)", "શુક્લ બારસ (Dwadashi)",
        "શુક્લ તેરસ (Trayodashi)", "શુક્લ ચૌદશ (Chaturdashi)", "પૂનમ (Purnima)",
        "કૃષ્ણ પડવો (Pratipada)", "કૃષ્ણ બીજ (Dwitiya)", "કૃષ્ણ ત્રીજ (Tritiya)", "કૃષ્ણ ચોથ (Chaturthi)",
        "કૃષ્ણ પંચમી (Panchami)", "કૃષ્ણ છઠ (Shashthi)", "કૃષ્ણ સાતમ (Saptami)", "કૃષ્ણ આઠમ (Ashtami)",
        "કૃષ્ણ નોમ (Navami)", "કૃષ્ણ દશમ (Dashami)", "કૃષ્ણ અગિયારસ (Ekadashi)", "કૃષ્ણ બારસ (Dwadashi)",
        "કૃષ્ણ તેરસ (Trayodashi)", "કૃષ્ણ ચૌદશ (Chaturdashi)", "અમાસ (Amavasya)"
    ]

    NAKSHATRAS_GU = [
        "અશ્વિની (Ashwini)", "ભરણી (Bharani)", "કૃતિકા (Krittika)", "રોહિણી (Rohini)",
        "મૃગશીર્ષ (Mrigashira)", "આર્દ્રા (Ardra)", "પુનર્વસુ (Punarvasu)", "પુષ્ય (Pushya)",
        "આશ્લેષા (Ashlesha)", "મઘા (Magha)", "પૂર્વા ફાલ્ગુની (Purva Phalguni)", "ઉત્તરા ફાલ્ગુની (Uttara Phalguni)",
        "હસ્ત (Hasta)", "ચિત્રા (Chitra)", "સ્વાતી (Swati)", "વિશાખા (Vishakha)",
        "અનુરાધા (Anuradha)", "જ્યેષ્ઠા (Jyeshta)", "મૂળ (Moola)", "પૂર્વાષાઢા (Purvashada)",
        "ઉત્તરાષાઢા (Uttarashada)", "શ્રવણ (Shravana)", "ધનિષ્ઠા (Dhanishta)", "શતભિષા (Shatabhisha)",
        "પૂર્વા ભાદ્રપદ (Purva Bhadrapada)", "ઉત્તરા ભાદ્રપદ (Uttara Bhadrapada)", "રેવતી (Revati)"
    ]

    YOGAS_GU = [
        "વિષ્કંભ (Vishkambha)", "પ્રીતિ (Priti)", "આયુષ્યમાન (Ayushman)", "સૌભાગ્ય (Saubhagya)",
        "શોભન (Shobhana)", "અતિગંડ (Atiganda)", "સુકર્મા (Sukarma)", "ધૃતિ (Dhriti)",
        "શૂલ (Shula)", "ગંડ (Ganda)", "વૃદ્ધિ (Vriddhi)", "ધ્રુવ (Dhruva)",
        "વ્યાઘાત (Vyaghata)", "હર્ષણ (Harshana)", "વજ્ર (Vajra)", "સિદ્ધિ (Siddhi)",
        "વ્યતીપાત (Vyatipata)", "વરીયાન (Variyan)", "પરીઘ (Parigha)", "શિવ (Shiva)",
        "સિદ્ધ (Siddha)", "સાધ્ય (Sadhya)", "શુભ (Subha)", "શુક્લ (Shukla)",
        "બ્રહ્મ (Brahma)", "ઐન્દ્ર (Aindra)", "વૈધૃતિ (Vaidhriti)"
    ]

    DAY_CHOGHADIYA_GU = [
        # Sun
        ['ઉદ્વેગ (Udveg)', 'ચલ (Chala)', 'લાભ (Labh)', 'અમૃત (Amrit)', 'કાળ (Kaal)', 'શુભ (Shubh)', 'રોગ (Roga)', 'ઉદ્વેગ (Udveg)'],
        # Mon
        ['અમૃત (Amrit)', 'કાળ (Kaal)', 'શુભ (Shubh)', 'રોગ (Roga)', 'ઉદ્વેગ (Udveg)', 'ચલ (Chala)', 'લાભ (Labh)', 'અમૃત (Amrit)'],
        # Tue
        ['રોગ (Roga)', 'ઉદ્વેગ (Udveg)', 'ચલ (Chala)', 'લાભ (Labh)', 'અમૃત (Amrit)', 'કાળ (Kaal)', 'શુભ (Shubh)', 'રોગ (Roga)'],
        # Wed
        ['લાભ (Labh)', 'અમૃત (Amrit)', 'કાળ (Kaal)', 'શુભ (Shubh)', 'રોગ (Roga)', 'ઉદ્વેગ (Udveg)', 'ચલ (Chala)', 'લાભ (Labh)'],
        # Thu
        ['શુભ (Shubh)', 'રોગ (Roga)', 'ઉદ્વેગ (Udveg)', 'ચલ (Chala)', 'લાભ (Labh)', 'અમૃત (Amrit)', 'કાળ (Kaal)', 'શુભ (Shubh)'],
        # Fri
        ['ચલ (Chala)', 'લાભ (Labh)', 'અમૃત (Amrit)', 'કાળ (Kaal)', 'શુભ (Shubh)', 'રોગ (Roga)', 'ઉદ્વેગ (Udveg)', 'ચલ (Chala)'],
        # Sat
        ['કાળ (Kaal)', 'શુભ (Shubh)', 'રોગ (Roga)', 'ઉદ્વેગ (Udveg)', 'ચલ (Chala)', 'લાભ (Labh)', 'અમૃત (Amrit)', 'કાળ (Kaal)'],
    ]

    @classmethod
    def calculate_panchang_for_date(cls, target_date: datetime.date, lat='21.1702', lon='72.8311') -> Dict[str, Any]:
        import ephem
        import math
        import datetime

        observer = ephem.Observer()
        observer.lat = lat
        observer.lon = lon
        observer.date = ephem.Date(target_date.strftime("%Y/%m/%d 00:00:00"))

        sun = ephem.Sun()
        moon = ephem.Moon()

        try:
            sunrise = observer.next_rising(sun).datetime() + datetime.timedelta(hours=5, minutes=30)
            sunset = observer.next_setting(sun).datetime() + datetime.timedelta(hours=5, minutes=30)
        except:
            sunrise = datetime.datetime.combine(target_date, datetime.time(6, 15))
            sunset = datetime.datetime.combine(target_date, datetime.time(19, 0))

        # Rahukaal calculation (1/8th of day length)
        day_len = sunset - sunrise
        part_len = day_len / 8
        weekday_idx = target_date.weekday() # 0=Mon
        rahukaal_map = {6: 8, 0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3}
        rahukaal_part = rahukaal_map[weekday_idx]
        
        rahukaal_start = sunrise + part_len * (rahukaal_part - 1)
        rahukaal_end = rahukaal_start + part_len

        # Now set observer to sunrise for accurate daily tithi/nakshatra
        # ephem needs UTC time. sunrise is already a local datetime with +5:30 applied.
        # We need to subtract 5:30 to get back to UTC for ephem calculation.
        sunrise_utc = sunrise - datetime.timedelta(hours=5, minutes=30)
        observer.date = ephem.Date(sunrise_utc)
        sun.compute(observer)
        moon.compute(observer)

        sun_trop = math.degrees(sun.hlon)
        moon_trop = math.degrees(moon.hlon)
        ayanamsha = 23.85 + (target_date.year - 2000) * (50.290966 / 3600.0)

        sun_lon = (sun_trop - ayanamsha) % 360
        moon_lon = (moon_trop - ayanamsha) % 360

        diff = (moon_lon - sun_lon) % 360
        tithi_idx = int(diff / 12) % 30
        nakshatra_idx = int(moon_lon / (360 / 27)) % 27
        yoga_idx = int((moon_lon + sun_lon) % 360 / (360 / 27)) % 27

        # Karana
        karana_idx = int(diff / 6) % 60
        KARANAS_GU = ["બવ (Bava)", "બાલવ (Balava)", "કૌલવ (Kaulava)", "તૈતિલ (Taitila)", "ગરજ (Garaja)", "વણિજ (Vanija)", "વિષ્ટિ (Bhadra)", "શકુનિ (Shakuni)", "ચતુષ્પાદ (Chatushpada)", "નાગ (Naga)", "કિંસ્તુઘ્ન (Kimstughna)"]
        if karana_idx == 0: k_val = KARANAS_GU[10]
        elif karana_idx >= 57: k_val = KARANAS_GU[karana_idx - 50]
        else: k_val = KARANAS_GU[(karana_idx - 1) % 7]

        seq_idx = (weekday_idx + 1) % 7
        base_choghadiya = cls.DAY_CHOGHADIYA_GU[seq_idx]
        
        choghadiya_list = []
        for i in range(8):
            slot_start = sunrise + (part_len * i)
            slot_end = sunrise + (part_len * (i + 1))
            choghadiya_list.append(f"{base_choghadiya[i]}: {slot_start.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}")

        sunrise_str = sunrise.strftime("%I:%M %p")
        sunset_str = sunset.strftime("%I:%M %p")
        rahukaal_str = f"{rahukaal_start.strftime('%I:%M %p')} - {rahukaal_end.strftime('%I:%M %p')}"
        
        from app.services.ai_astrologer import AIAstrologerService
        panchang_data = {
            "date": target_date.strftime("%d %B %Y"),
            "weekday": target_date.strftime("%A"),
            "tithi": cls.TITHIS_GU[tithi_idx],
            "nakshatra": cls.NAKSHATRAS_GU[nakshatra_idx],
            "yoga": cls.YOGAS_GU[yoga_idx],
            "karana": k_val,
            "sunrise": sunrise_str,
            "sunset": sunset_str,
            "rahukaal": rahukaal_str,
            "day_choghadiya": choghadiya_list,
            "source": "Ephem Engine (Offline)"
        }
        
        panchang_data["ai_insight"] = "આજનો દિવસ શુભ અને માંગલિક કાર્યો માટે સાનુકૂળ છે."
        return panchang_data

