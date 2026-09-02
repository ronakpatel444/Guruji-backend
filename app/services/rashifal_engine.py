from typing import Dict, Any, List

class RashifalEngine:
    SIGNS = [
        {"id": "aries", "en": "Aries", "gu": "મેષ", "hi": "मेष", "symbol": "♈", "date_range": "Mar 21 - Apr 19"},
        {"id": "taurus", "en": "Taurus", "gu": "વૃષભ", "hi": "वृषभ", "symbol": "♉", "date_range": "Apr 20 - May 20"},
        {"id": "gemini", "en": "Gemini", "gu": "મિથુન", "hi": "मिथुन", "symbol": "♊", "date_range": "May 21 - Jun 20"},
        {"id": "cancer", "en": "Cancer", "gu": "કર્ક", "hi": "कर्क", "symbol": "♋", "date_range": "Jun 21 - Jul 22"},
        {"id": "leo", "en": "Leo", "gu": "સિંહ", "hi": "सिंह", "symbol": "♌", "date_range": "Jul 23 - Aug 22"},
        {"id": "virgo", "en": "Virgo", "gu": "કન્યા", "hi": "कन्या", "symbol": "♍", "date_range": "Aug 23 - Sep 22"},
        {"id": "libra", "en": "Libra", "gu": "તુલા", "hi": "तुला", "symbol": "♎", "date_range": "Sep 23 - Oct 22"},
        {"id": "scorpio", "en": "Scorpio", "gu": "વૃશ્ચિક", "hi": "वृश्चिक", "symbol": "♏", "date_range": "Oct 23 - Nov 21"},
        {"id": "sagittarius", "en": "Sagittarius", "gu": "ધન", "hi": "धनु", "symbol": "♐", "date_range": "Nov 22 - Dec 21"},
        {"id": "capricorn", "en": "Capricorn", "gu": "મકર", "hi": "मकर", "symbol": "♑", "date_range": "Dec 22 - Jan 19"},
        {"id": "aquarius", "en": "Aquarius", "gu": "કુંભ", "hi": "कुंभ", "symbol": "♒", "date_range": "Jan 20 - Feb 18"},
        {"id": "pisces", "en": "Pisces", "gu": "મીન", "hi": "मीन", "symbol": "♓", "date_range": "Feb 19 - Mar 20"},
    ]

    _cache = {}
    _cache_date = ""

    @classmethod
    def get_prediction(cls, sign_id: str, lang: str = "gu") -> Dict[str, Any]:
        from app.services.ai_astrologer import AIAstrologerService
        import datetime
        import random
        
        sign_info = next((s for s in cls.SIGNS if s["id"] == sign_id.lower() or s["en"].lower() == sign_id.lower()), cls.SIGNS[4])
        
        # Simple daily caching logic
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        if cls._cache_date != today_str:
            cls._cache.clear()
            cls._cache_date = today_str
            
        cache_key = f"{sign_info['id']}_{lang}"
        
        if cache_key in cls._cache:
            prediction_text = cls._cache[cache_key]
        else:
            # Get dynamic prediction from Gemini AI
            prediction_text = AIAstrologerService.generate_daily_rashifal(sign_info["en"], lang=lang)
            cls._cache[cache_key] = prediction_text
        
        # Make the scores dynamic based on the day and sign so they aren't static
        seed_value = int(datetime.datetime.now().strftime("%Y%m%d")) + sum(ord(c) for c in sign_info["id"])
        rng = random.Random(seed_value)


        return {
            "sign_id": sign_info["id"],
            "sign_en": sign_info["en"],
            "sign_gu": sign_info["gu"],
            "sign_hi": sign_info["hi"],
            "symbol": sign_info["symbol"],
            "date_range": sign_info["date_range"],
            "date": datetime.datetime.now().strftime("%d %B %Y"),
            "prediction_summary": prediction_text,
            "love_score": f"{rng.randint(70, 98)}%",
            "career_score": f"{rng.randint(70, 98)}%",
            "finance_score": f"{rng.randint(70, 98)}%",
            "family_score": f"{rng.randint(70, 98)}%",
            "health_score": f"{rng.randint(70, 98)}%",
            "travel_score": f"{rng.randint(60, 90)}%",
            "love_stars": rng.randint(3, 5),
            "career_stars": rng.randint(3, 5),
            "finance_stars": rng.randint(3, 5),
            "family_stars": rng.randint(3, 5),
            "health_stars": rng.randint(3, 5),
            "travel_stars": rng.randint(2, 5),
            "lucky_number": rng.randint(1, 9),
            "lucky_color": rng.choice(["Red", "Blue", "Green", "Yellow", "Orange", "White"]),
            "lucky_time": f"{rng.randint(8, 11)}:00 AM - {rng.randint(1, 5)}:00 PM"
        }

    @classmethod
    def get_all_signs(cls) -> List[Dict[str, Any]]:
        return cls.SIGNS
