import os
import google.generativeai as genai
import datetime
from typing import Dict, Any, Optional

# Configure Gemini with the user-provided API key
api_key = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)

# Using both models as requested
model_flash = genai.GenerativeModel('gemini-3.1-flash-lite') # For fast responses (e.g. Chat, Daily Rashifal)
model_pro = genai.GenerativeModel('gemini-3.1-flash-lite')     # For deep analysis (e.g. Kundli Milan Premium Report)

class AIAstrologerService:
    @staticmethod
    def generate_reply(question: str, pandit_name: str = "Pandit Aarav Ji", lang: str = "gu", kundli_data: Optional[Dict[str, Any]] = None) -> str:
        kundli_info = ""
        if kundli_data:
            kundli_info = f"\nUser's Kundli Data:\n{kundli_data}\nUse this data to answer questions about marriage, property, finance, career, etc."
            
        prompt = f"""
        You are an expert Vedic Astrologer named {pandit_name}. 
        Answer the following user question in the exact same language and script style as the user.
        If the user asks in Gujarati script (e.g. "લગ્ન ક્યારે થશે?"), reply in Gujarati script.
        If the user asks in English script but Gujarati language (e.g. "lagan kyare thase?"), reply in exactly that same English-script Gujarati (Gujlish).
        If the user mixes English and Gujarati, mix them similarly in your reply.
        Keep it under 3-4 sentences.
        Use astrology terms like planets, transits, and houses where appropriate.{kundli_info}
        
        CRITICAL RULE: You MUST ONLY answer questions related to astrology, Kundli, horoscopes, numerology, planetary positions, matchmaking, Vastu, or spirituality.
        If the user asks an off-topic question (e.g., about general knowledge, food, coding, daily tasks, weather, etc.), you MUST politely decline.
        Say something like: "ક્ષમા કરજો, હું માત્ર જ્યોતિષ અને કુંડળીને લગતા પ્રશ્નોના જ જવાબ આપી શકું છું." (Sorry, I can only answer questions related to astrology and Kundli) but match their language/script.
        
        Question: {question}
        """
        try:
            response = model_flash.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if lang == "gu":
                return "ક્ષમા કરજો, અત્યારે ગ્રહોની સ્થિતિ વાંચવામાં થોડી અડચણ છે. કૃપા કરીને થોડીવાર પછી પ્રયાસ કરો."
            return "Sorry, I am unable to read the stars at this moment. Please try again later."

    @staticmethod
    def generate_kundli_milan_report(boy_kundli: Dict[str, Any], girl_kundli: Dict[str, Any], lang: str = "gu") -> dict:
        prompt = f'''
        You are an expert Vedic Astrologer. I am providing you with the Kundli (birth chart) data of a boy and a girl.
        Please analyze their planetary compatibility for marriage.
        
        Boy Kundli:
        Lagna: {boy_kundli.get('lagna')}
        Moon Sign: {boy_kundli.get('moon_sign')}
        Sun Sign: {boy_kundli.get('sun_sign')}
        Manglik Status: {boy_kundli.get('manglik_status')}
        
        Girl Kundli:
        Lagna: {girl_kundli.get('lagna')}
        Moon Sign: {girl_kundli.get('moon_sign')}
        Sun Sign: {girl_kundli.get('sun_sign')}
        Manglik Status: {girl_kundli.get('manglik_status')}
        
        Write a premium compatibility report in the {lang} language.
        You MUST return ONLY a valid JSON object (do not wrap in markdown or backticks). The JSON must have exactly these keys:
        - "success_percentage": an integer between 0 and 100.
        - "success_reason": a detailed explanation of the overall compatibility and success percentage (3 to 4 sentences).
        - "growth": a detailed explanation of financial, career, and mutual growth post-marriage (3 to 4 sentences).
        - "child": a detailed explanation of child prospects and family harmony (3 to 4 sentences).
        - "dominance": a detailed explanation of relationship dynamics, mutual understanding, and dominance (3 to 4 sentences).
        - "remedies": a list of strings, each being a specific remedy.
        '''
        try:
            response = model_flash.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()
            import json
            return json.loads(text)
        except Exception as e:
            print('Error in generate_kundli_milan_report:', e)
            return {
                "success_percentage": 50,
                "success_reason": "ડેટા ઉપલબ્ધ નથી",
                "growth": "ડેટા ઉપલબ્ધ નથી",
                "child": "ડેટા ઉપલબ્ધ નથી",
                "dominance": "ડેટા ઉપલબ્ધ નથી",
                "remedies": ["પ્રાર્થના કરો", "શાંતિ રાખો"]
            }

    @staticmethod
    def generate_daily_rashifal(sign_en: str, lang: str = "gu") -> str:
        prompt = f"""
        You are an expert Vedic Astrologer. Write a daily horoscope prediction for the Zodiac sign {sign_en}.
        The language should be {lang}.
        Keep it to 3 or 4 sentences max.
        Mention what they should focus on today (e.g., career, health, or family) and one short remedy or lucky aspect.
        Do not use markdown formatting, just plain text with newlines.
        """
        try:
            response = model_flash.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if lang == "gu":
                return f"આજે {sign_en} રાશિ માટે ગ્રહોનું ભ્રમણ અનુકૂળ રહેશે. કરિયરમાં પ્રગતિ અને આર્થિક લાભના યોગ છે."
            elif lang == "hi":
                return f"आज {sign_en} राशि के लिए ग्रहों का गोचर अनुकूल रहेगा। करियर में प्रगति और आर्थिक लाभ होगा।"
            return f"Today planetary transits align favorably for {sign_en}."

    @staticmethod
    def chat_numerology(numbers_data: Dict[str, Any], user_message: str, lang: str = "gu") -> str:
        prompt = f"""
        You are an expert Numerologist. The user's numbers are:
        Mulank (Root Number): {numbers_data.get('mulank', {}).get('number')}
        Bhagyank (Life Path Number): {numbers_data.get('bhagyank', {}).get('number')}
        Namank (Destiny Number): {numbers_data.get('namank', {}).get('number')}
        
        The user has asked: "{user_message}"
        
        Respond to their query in the {lang} language based on their numbers. 
        Keep your response conversational, insightful, and under 5 sentences.
        Do not use markdown formatting, just plain text with newlines.
        """
        try:
            response = model_flash.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if lang == "gu":
                return "માફ કરજો, અત્યારે ચેટ સર્વર વ્યસ્ત છે. થોડીવાર પછી પ્રયાસ કરો."
            return "Sorry, chat server is busy right now. Please try again later."

    @staticmethod
    def generate_kundli_life_analysis(houses_data: list, lang: str = "gu") -> dict:
        prompt = f'''
        You are an expert Vedic Astrologer. I am providing you with the 12 houses data of a person's Kundli (Birth Chart).
        Data: {houses_data}
        
        Provide a detailed 3-4 sentence prediction for each of these 4 categories in {lang} language. Make the reading sound professional and personalized based on the planetary positions:
        - love_life
        - career
        - property
        - finance
        
        Return ONLY a valid JSON object with those 4 keys and the text as values. Do NOT include markdown code blocks like ```json.
        '''
        try:
            response = model_pro.generate_content(prompt)
            import json
            import re
            
            text = response.text.strip()
            # Remove any potential markdown json blocks
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            
            data = json.loads(text)
            return data
        except Exception as e:
            print('Error in generate_kundli_life_analysis:', e)
            if lang == "gu":
                return {
                    "love_life": "તમારા 7મા ભાવમાં ગ્રહોની સ્થિતિ અનુસાર તમારું પ્રેમ અને વૈવાહિક જીવન સારું રહેશે. જો કે, થોડી ધીરજ અને સમજદારી રાખવી જરૂરી છે, જેથી સંબંધોમાં મધુરતા જળવાઈ રહે.",
                    "career": "દસમા ભાવના સ્વામીની સ્થિતિ દર્શાવે છે કે તમારા કરિયરમાં પ્રગતિની ઉત્તમ તકો છે. મહેનત અને સાચા માર્ગદર્શનથી તમને નોકરી કે વ્યવસાયમાં ધારી સફળતા મળશે.",
                    "property": "ચોથા ભાવના ગ્રહો સૂચવે છે કે જમીન અને મકાન સંબંધિત બાબતોમાં તમને ભવિષ્યમાં સારા લાભ મળી શકે છે. કોઈ નવું રોકાણ કરતા પહેલા યોગ્ય સલાહ લેવી હિતાવહ છે.",
                    "finance": "તમારા બીજા અને અગિયારમા ભાવની સ્થિતિ આર્થિક બાબતોમાં મજબૂતી દર્શાવે છે. આવકના નવા સ્ત્રોત ઊભા થઈ શકે છે, પરંતુ બિનજરૂરી ખર્ચ પર નિયંત્રણ રાખવું પડશે."
                }
            return {
                "love_life": "Based on the planetary positions in your 7th house, your love and marital life will be favorable. However, patience and understanding are required to maintain harmony.",
                "career": "The lord of your 10th house indicates excellent opportunities for career progression. With hard work and right guidance, you will achieve desired success in your profession.",
                "property": "Planets in the 4th house suggest that you may get good benefits in matters related to land and property in the future. It is advisable to take proper advice before making any new investment.",
                "finance": "The position of your 2nd and 11th houses indicates strength in financial matters. New sources of income may arise, but you will need to control unnecessary expenses."
            }

    @staticmethod
    def generate_panchang_insight(panchang_data: dict, lang: str = "gu") -> str:
        prompt = f'''
        You are an expert Vedic Astrologer. I am providing you with today's Panchang data.
        Data: {panchang_data}
        
        Provide a short 2-3 sentence daily insight/prediction based on this specific Tithi, Nakshatra, and Yoga. 
        What should the person focus on today? What is the astrological energy of the day?
        Language: {lang}
        
        Return ONLY the plain text response. No markdown formatting.
        '''
        try:
            response = model_flash.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print('Error in generate_panchang_insight:', e)
            if lang == "gu":
                return "આજની ગ્રહસ્થિતિ મુજબ દિવસ શુભ અને ફળદાયી રહેશે. કોઈપણ નવું કાર્ય શરૂ કરવા માટે અનુકૂળ સમય છે."
            return "Today's planetary alignment is auspicious and fruitful. It is a good time to start new endeavors."

    @staticmethod
    def analyze_palm_image(image_bytes: bytes, is_left: bool, lang: str = "gu") -> dict:
        import json
        import re
        from PIL import Image
        import io
        
        palm_type = "Left Palm" if is_left else "Right Palm"
        prompt = f'''
        You are an expert Palmist. First, check if the provided image is actually a human palm.
        If it is NOT a human palm (e.g., a car, animal, random object, or blurry), return this EXACT JSON:
        {{
            "general_analysis": "ક્ષમા કરજો, આ ફોટો હથેળીનો લાગતો નથી. કૃપા કરીને સ્પષ્ટ હથેળીનો ફોટો અપલોડ કરો.",
            "heart_line": "",
            "head_line": "",
            "life_line": "",
            "fate_line": "",
            "sun_line": "",
            "special_symbols": ""
        }}
        
        If it IS a human palm, analyze the provided image of a {palm_type}.
        Provide a detailed reading in {lang} language.
        Return ONLY a JSON object (do not wrap in markdown or backticks) with exactly these keys:
        - "general_analysis": A paragraph (4-5 lines) giving an overall summary and future prediction.
        - "heart_line": Analysis of their emotional life and relationships.
        - "head_line": Analysis of their intellect and decision making.
        - "life_line": Analysis of their health, vitality, and longevity.
        - "fate_line": Analysis of their career and success.
        - "sun_line": Analysis of their fame and wealth.
        - "special_symbols": Analysis of any crosses, stars, or special symbols found on the palm.
        '''
        try:
            img = Image.open(io.BytesIO(image_bytes))
            response = model_flash.generate_content([prompt, img])
            text = response.text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            return json.loads(text)
        except Exception as e:
            print(f'Error in analyze_palm_image: {e}')
            return {
                "general_analysis": "Palm reading could not be processed completely. Please try again.",
                "heart_line": "",
                "head_line": "",
                "life_line": "",
                "fate_line": "",
                "sun_line": "",
                "special_symbols": ""
            }

    @staticmethod
    def analyze_face_image(image_bytes: bytes, lang: str = "gu") -> dict:
        import json
        import re
        from PIL import Image
        import io
        
        prompt = f'''
        You are an expert Face Reader (Physiognomist). First, check if the provided image is actually a human face.
        If it is NOT a human face (e.g., a car, animal, random object, or back of head), return this EXACT JSON:
        {{
            "general_analysis": "ક્ષમા કરજો, આ ફોટો ચહેરાનો લાગતો નથી. કૃપા કરીને સ્પષ્ટ ચહેરાનો ફોટો અપલોડ કરો.",
            "forehead": "",
            "eyes": "",
            "nose": "",
            "lips_jaw": ""
        }}
        
        If it IS a human face, analyze the provided image of a human face.
        Provide a detailed reading in {lang} language.
        Return ONLY a JSON object (do not wrap in markdown or backticks) with exactly these keys:
        - "general_analysis": A paragraph (4-5 lines) giving an overall summary of their personality and destiny.
        - "forehead": Analysis of their intellect, youth, and wisdom.
        - "eyes": Analysis of their emotional nature and intuition.
        - "nose": Analysis of their career, wealth, and drive.
        - "lips_jaw": Analysis of their communication skills, relationships, and willpower.
        '''
        try:
            img = Image.open(io.BytesIO(image_bytes))
            response = model_flash.generate_content([prompt, img])
            text = response.text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            return json.loads(text)
        except Exception as e:
            print(f'Error in analyze_face_image: {e}')
            return {
                "general_analysis": "Face reading could not be processed completely. Please try again.",
                "forehead": "Data unavailable",
                "eyes": "Data unavailable",
                "nose": "Data unavailable",
                "lips_jaw": "Data unavailable"
            }
