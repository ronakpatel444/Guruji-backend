from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form
from typing import List, Optional
import datetime

from app.models import (
    UserProfileRequest, UserProfileResponse,
    RashifalResponse, KundliResponse, NumerologyResponse, NumerologyChatRequest,
    PanditDetail, ChatMessageRequest, ChatMessageResponse, PanchangResponse
)
from app.services.gemini_service import GeminiAstrologyService
from app.services.rashifal_engine import RashifalEngine
from app.services.ai_astrologer import AIAstrologerService

router = APIRouter(prefix="/api/v1")

# --- AUTH & USER PROFILE ---
@router.post("/auth/guest-login")
def guest_login():
    return {
        "status": "success",
        "token": "guest_jwt_token_998877665544332211",
        "user_id": "usr_998877",
        "message": "Logged in successfully as guest"
    }

@router.post("/users/profile", response_model=UserProfileResponse)
def save_user_profile(req: UserProfileRequest):
    return UserProfileResponse(
        user_id="usr_998877",
        name=req.name,
        dob=req.dob,
        birth_place=req.birth_place,
        birth_time=req.birth_time,
        zodiac_sign_en="Leo",
        zodiac_sign_gu="સિંહ",
        zodiac_sign_hi="सिंह",
        zodiac_symbol="♌",
        destiny_number=7
    )

# --- GEMINI VISION AI PALM & FACE SCAN ---
@router.post("/scan/palm")
async def scan_palm_image(
    file: Optional[UploadFile] = File(None),
    lang: str = Form("gu")
):
    image_bytes = None
    if file:
        image_bytes = await file.read()
    return GeminiAstrologyService.analyze_palm(image_bytes=image_bytes, lang=lang)

@router.post("/scan/face")
async def scan_face_image(
    file: Optional[UploadFile] = File(None),
    lang: str = Form("gu")
):
    image_bytes = None
    if file:
        image_bytes = await file.read()
    return GeminiAstrologyService.analyze_face(image_bytes=image_bytes, lang=lang)

# --- RASHIFAL DAILY PREDICTIONS ---
@router.get("/rashifal/signs")
def get_all_zodiac_signs():
    return RashifalEngine.get_all_signs()

@router.get("/rashifal/{sign_id}", response_model=RashifalResponse)
def get_daily_rashifal(sign_id: str, lang: str = Query("gu")):
    return RashifalEngine.get_prediction(sign_id=sign_id, lang=lang)

# --- VEDIC KUNDLI CALCULATION VIA GEMINI ---
@router.post("/kundli/calculate", response_model=KundliResponse)
def calculate_kundli(req: UserProfileRequest):
    from app.services.kundli_engine import VedicKundliEngine
    
    # 1. Get raw astronomical data
    data = VedicKundliEngine.calculate_kundli(
        dob=req.dob,
        birth_time=req.birth_time,
        birth_place=req.birth_place
    )
    return KundliResponse(**data)

# --- GEMINI NUMEROLOGY ENGINE ---
@router.post("/numerology/calculate", response_model=NumerologyResponse)
def calculate_numerology(req: UserProfileRequest):
    from app.services.numerology_engine import NumerologyEngine
    data = NumerologyEngine.calculate_destiny(
        dob=req.dob,
        name=req.name
    )
    return NumerologyResponse(**data)

@router.post("/numerology/chat")
def chat_numerology(req: NumerologyChatRequest):
    from app.services.ai_astrologer import AIAstrologerService
    reply = AIAstrologerService.chat_numerology(req.numbers_data, req.message, req.language)
    return {"reply": reply}

# --- PANDITS DIRECTORY & CONSULTATION ---
@router.get("/pandits", response_model=List[PanditDetail])
def get_pandits_list():
    return [
        PanditDetail(
            id="1",
            name="Pandit Aarav Ji",
            specialty="Vedic Astrology Expert",
            category="Jyotish Shastra",
            rating=4.8,
            consultations="15K+",
            is_online=True,
            expertise_list=["Jyotish Shastra", "Kundli Analysis", "Love & Marriage", "Career Guidance", "Doshas & Remedies"]
        ),
        PanditDetail(
            id="2",
            name="Pandit Meera Ji",
            specialty="Love & Relationship Spec.",
            category="Astrology",
            rating=4.9,
            consultations="12K+",
            is_online=True,
            expertise_list=["Love Compatibility", "Marriage Timing", "Relationship Healing"]
        ),
        PanditDetail(
            id="3",
            name="Pandit Dev Ji",
            specialty="Numerology & Name Expert",
            category="Numerology",
            rating=4.7,
            consultations="9K+",
            is_online=True,
            expertise_list=["Destiny Numbers", "Name Correction", "Business Numerology"]
        ),
        PanditDetail(
            id="4",
            name="Pandit Rudra Ji",
            specialty="Palmistry & Vastu Expert",
            category="Palmistry",
            rating=4.7,
            consultations="18K+",
            is_online=True,
            expertise_list=["Palm Lines Reading", "Vastu Dosha Remedy", "Gemstone Guide"]
        ),
    ]

# --- AI ASTROLOGER CHAT ---
@router.post("/chat/send", response_model=ChatMessageResponse)
def send_chat_message(req: ChatMessageRequest):
    reply_text = AIAstrologerService.generate_reply(
        question=req.question,
        pandit_name=req.pandit_name,
        lang=req.language,
        kundli_data=req.kundli_data
    )
    now_time = datetime.datetime.now().strftime("%I:%M %p")
    return ChatMessageResponse(
        reply=reply_text,
        timestamp=now_time,
        sender=req.pandit_name
    )

from app.services.navamsha_service import NavamshaAstrologyService
from app.services.panchang_engine import VedicPanchangEngine
from app.services.milan_engine import VedicKundliMilanEngine

# --- PANCHANG & CHOGHADIYA API ---
CITY_COORDS = {
    "surat": ("21.1702", "72.8311"),
    "ahmedabad": ("23.0225", "72.5714"),
    "rajkot": ("22.3039", "70.8022"),
    "vadodara": ("22.3072", "73.1812"),
    "bhavnagar": ("21.7645", "72.1519"),
    "junagadh": ("21.5222", "70.4579"),
    "jamnagar": ("22.4707", "70.0577"),
    "gandhinagar": ("23.2156", "72.6369"),
    "bhuj": ("23.2420", "69.6669"),
    "mumbai": ("19.0760", "72.8777"),
    "delhi": ("28.7041", "77.1025"),
}

def get_lat_lon(place: str):
    clean_place = place.split(',')[0].split('(')[0].strip().lower()
    return CITY_COORDS.get(clean_place, ("23.0225", "72.5714")) # Default Ahmedabad

_panchang_cache = {}

@router.get("/panchang/today")
def get_today_panchang(lang: str = Query("gu"), place: str = Query("Ahmedabad")):
    from app.services.gemini_data_generator import GeminiDataGenerator
    from app.services.panchang_engine import VedicPanchangEngine
    import datetime
    
    today_date = datetime.date.today()
    cache_key = f"{today_date}_{lang}_{place}"
    
    if cache_key in _panchang_cache:
        return _panchang_cache[cache_key]
        
    lat, lon = get_lat_lon(place)
    raw_data = VedicPanchangEngine.calculate_panchang_for_date(today_date, lat, lon)
    panchang_data = GeminiDataGenerator.fetch_panchang(raw_data, lang)
    
    _panchang_cache[cache_key] = panchang_data
    return panchang_data

@router.get("/panchang/date/{date_str}")
def get_panchang_for_specific_date(date_str: str, lang: str = Query("gu"), place: str = Query("Ahmedabad")):
    from app.services.gemini_data_generator import GeminiDataGenerator
    from app.services.panchang_engine import VedicPanchangEngine
    import datetime
    
    lat, lon = get_lat_lon(place)
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        dt = datetime.date.today()
        
    raw_data = VedicPanchangEngine.calculate_panchang_for_date(dt, lat, lon)
    return GeminiDataGenerator.fetch_panchang(raw_data, lang)

# --- KUNDLI MILAN MATCHMAKING API ---
@router.post("/kundli/calculate")
def calculate_kundli(payload: dict):
    from app.services.gemini_data_generator import GeminiDataGenerator
    from app.services.kundli_engine import VedicKundliEngine
    
    name = payload.get("name", "User")
    dob = payload.get("dob", "1998-01-01")
    time = payload.get("birth_time", "12:00 PM")
    place = payload.get("birth_place", "Ahmedabad")
    lang = payload.get("language", "gu")
    
    raw_kundli = VedicKundliEngine.calculate_kundli(dob, time, place)
    return GeminiDataGenerator.fetch_kundli(raw_kundli, name, lang)

# --- KUNDLI MILAN MATCHMAKING API ---
@router.post("/kundli/milan")
def calculate_gun_milan(
    boy_name: str = Query("Arav"),
    boy_dob: str = Query("1998-05-16"),
    boy_time: str = Query("08:30"),
    girl_name: str = Query("Ananya"),
    girl_dob: str = Query("1999-08-20"),
    girl_time: str = Query("14:15"),
    is_premium: bool = Query(False),
    lang: str = Query("gu")
):
    from app.services.kundli_engine import VedicKundliEngine
    from app.services.ai_astrologer import AIAstrologerService
    import random
    
    boy_kundli = VedicKundliEngine.calculate_kundli(boy_dob, boy_time, "Ahmedabad")
    girl_kundli = VedicKundliEngine.calculate_kundli(girl_dob, girl_time, "Surat")
    
    # Calculate basic Ashtakoot score offline (Mocked randomly based on names for now, can use milan_engine later)
    # Using deterministic mock score based on names to ensure consistent but varied results
    base_score = 18 + (len(boy_name) + len(girl_name)) % 18
    
    response_data = {
        "boy_rashi": boy_kundli["moon_sign"],
        "girl_rashi": girl_kundli["moon_sign"],
        "boy_nakshatra": boy_kundli["nakshatra"],
        "girl_nakshatra": girl_kundli["nakshatra"],
        "boy_manglik": boy_kundli["manglik_dosh"],
        "girl_manglik": girl_kundli["manglik_dosh"],
        "total_score": base_score,
        "is_premium": is_premium
    }
    
    if is_premium:
        premium_report = AIAstrologerService.generate_kundli_milan_report(boy_kundli, girl_kundli, lang)
        response_data["ai_report"] = premium_report
    else:
        if lang == "gu":
            response_data["basic_report"] = f"મિલાનનો કુલ સ્કોર {base_score}/36 છે. વિગતવાર એનાલિસિસ અને ઉપાય માટે પ્રીમિયમ પ્લાન એક્ટિવેટ કરો."
        else:
            response_data["basic_report"] = f"Total matching score is {base_score}/36. Upgrade to Premium for detailed AI analysis and remedies."
            
    return response_data

# --- IMAGE ANALYSIS API (Palm & Face) ---
@router.post("/analyze/palm")
async def analyze_palm(
    image: UploadFile = File(...),
    is_left: bool = Form(True),
    lang: str = Form("gu")
):
    image_bytes = await image.read()
    result = AIAstrologerService.analyze_palm_image(image_bytes, is_left, lang)
    return {"status": "success", "data": result}

@router.post("/analyze/face")
async def analyze_face(
    image: UploadFile = File(...),
    lang: str = Form("gu")
):
    image_bytes = await image.read()
    result = AIAstrologerService.analyze_face_image(image_bytes, lang)
    return {"status": "success", "data": result}

