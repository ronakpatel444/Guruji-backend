import os
import google.generativeai as genai
import json

api_key = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.1-flash-lite')
class GeminiDataGenerator:
    @staticmethod
    def fetch_panchang(raw_data: dict, lang: str = "gu") -> dict:
        lang_map = {"gu": "Gujarati", "hi": "Hindi", "en": "English"}
        lang_name = lang_map.get(lang, "Gujarati")
        prompt = f"""
        You are an expert Vedic Astrologer. I have calculated the precise astronomical data for a Panchang.
        Here is the raw data: {json.dumps(raw_data, ensure_ascii=False)}
        
        Translate and format this entire data strictly into {lang_name} language. 
        You MUST return ONLY a valid JSON object (do not wrap in markdown or backticks). The JSON must have exactly these keys:
        - "date": The date from raw data
        - "weekday": The weekday from raw data translated to {lang_name}
        - "tithi": The tithi from raw data translated to {lang_name}
        - "nakshatra": The nakshatra from raw data translated to {lang_name}
        - "yoga": The yoga from raw data translated to {lang_name}
        - "karana": The karana from raw data translated to {lang_name}
        - "sunrise": The sunrise time
        - "sunset": The sunset time
        - "rahukaal": The rahukaal time
        - "day_choghadiya": The list of choghadiya from raw data translated to {lang_name}
        - "source": "Gemini 1.5 Flash (AI Enhanced)"
        """
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            return json.loads(text)
        except Exception as e:
            print(f'Error fetching Panchang from Gemini: {e}')
            return raw_data

    @staticmethod
    def fetch_kundli(raw_kundli: dict, name: str, lang: str = "gu") -> dict:
        lang_map = {"gu": "Gujarati", "hi": "Hindi", "en": "English"}
        lang_name = lang_map.get(lang, "Gujarati")
        prompt = f"""
        You are an expert Vedic Astrologer. Here is the mathematically calculated Kundli (Birth Chart) for {name}.
        Raw Data: {json.dumps(raw_kundli, ensure_ascii=False)}
        
        Based on these exact planetary positions, provide a detailed Life Analysis strictly in {lang_name} language. All values in the JSON (except the exact english house abbreviations) MUST be translated to {lang_name}.
        You MUST return ONLY a valid JSON object. The JSON must have exactly these keys:
        - "lagna": The ascendant sign translated to {lang_name}
        - "moon_sign": The moon sign translated to {lang_name}
        - "sun_sign": The sun sign translated to {lang_name}
        - "nakshatra": The nakshatra translated to {lang_name}
        - "current_dasha": The dasha translated to {lang_name}
        - "manglik_status": Is the person Manglik? Answer in {lang_name}.
        - "houses": The EXACT same "houses" array from the raw data. DO NOT CHANGE THIS ARRAY.
        - "life_analysis": An object with 4 keys ("love_life", "career", "property", "finance"), each containing a 2-sentence highly personalized astrological prediction based on this specific Kundli, written perfectly in {lang_name}.
        """

        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            return json.loads(text)
        except Exception as e:
            print(f'Error fetching Kundli from Gemini: {e}')
            return raw_kundli
